from __future__ import annotations

from studio.application.results import AttendanceResult
from studio.domain import errors, policies
from studio.domain.models import BookingStatus, NoShow
from studio.ports import (
    BookingRepository,
    ClassRepository,
    Clock,
    MemberRepository,
    Notifier,
)


class RecordAttendance:
    def __init__(
        self,
        members: MemberRepository,
        classes: ClassRepository,
        bookings: BookingRepository,
        notifier: Notifier,
        clock: Clock,
    ) -> None:
        self.members = members
        self.classes = classes
        self.bookings = bookings
        self.notifier = notifier
        self.clock = clock

    def execute(self, booking_id: int, *, attended: bool) -> AttendanceResult:
        now = self.clock.now()

        booking = self.bookings.get(booking_id)
        if booking is None:
            raise errors.BookingNotFound()
        if booking.status is not BookingStatus.CONFIRMED:
            raise errors.DomainError(
                f"Attendance only applies to confirmed bookings (this one is '{booking.status}')"
            )

        member = self.members.get(booking.member_id)
        session = self.classes.get(booking.class_id)
        if member is None:
            raise errors.MemberNotFound()
        if session is None:
            raise errors.ClassNotFound()

        new_status = BookingStatus.ATTENDED if attended else BookingStatus.NO_SHOW
        updated = self.bookings.save(booking.with_status(new_status))

        block_applied = False
        if not attended:
            self.bookings.record_no_show(
                NoShow(member_id=member.id, class_id=session.id, happened_at=now)
            )
            dates = [n.happened_at for n in self.bookings.no_shows_of(member.id)]
            until = policies.block_for_no_shows(dates, now)
            if until is not None and not policies.is_blocked(member.blocked_until, now):
                member = self.members.save(member.blocked(until))
                self.notifier.member_blocked(member, until)
                block_applied = True

        return AttendanceResult(
            booking=updated, member=member, session=session, block_applied=block_applied
        )
