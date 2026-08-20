from __future__ import annotations

from datetime import datetime

from studio.application.results import BookingResult
from studio.domain import capacity, errors, policies
from studio.domain.models import Booking, BookingStatus, ClassSession, Member
from studio.ports import (
    BookingRepository,
    ClassRepository,
    Clock,
    MemberRepository,
    Notifier,
    PaymentGateway,
)


class BookClass:
    def __init__(
        self,
        members: MemberRepository,
        classes: ClassRepository,
        bookings: BookingRepository,
        payments: PaymentGateway,
        notifier: Notifier,
        clock: Clock,
    ) -> None:
        self.members = members
        self.classes = classes
        self.bookings = bookings
        self.payments = payments
        self.notifier = notifier
        self.clock = clock

    def execute(self, member_id: int, class_id: int) -> BookingResult:
        now = self.clock.now()

        member = self.members.get(member_id)
        if member is None:
            raise errors.MemberNotFound()

        session = self.classes.get(class_id)
        if session is None:
            raise errors.ClassNotFound()

        self._check_member(member, now)
        self._check_class(member, session, now)
        self._check_agenda(member, session)

        class_bookings = self.bookings.for_class(session.id)
        gets_seat = capacity.has_room(session.capacity, class_bookings)

        charged = 0
        charge_ref = None
        if gets_seat and policies.requires_payment(member.plan):
            charge = self.payments.charge(member, session.price_cents, f"Class {session.name}")
            if not charge.successful:
                raise errors.PaymentDeclined(charge.reason or None)
            charged = charge.amount_cents
            charge_ref = charge.reference

        credit_spent = False
        credits_left = None
        if gets_seat and policies.spends_credit(member.plan):
            if member.credits <= 0:
                raise errors.NoCreditsLeft()
            member = self.members.save(member.with_credits(member.credits - 1))
            credit_spent = True
            credits_left = member.credits

        position = None if gets_seat else capacity.next_waitlist_position(class_bookings)
        booking = self.bookings.add(
            Booking(
                id=0,
                member_id=member.id,
                class_id=session.id,
                status=BookingStatus.CONFIRMED if gets_seat else BookingStatus.WAITLISTED,
                created_at=now,
                waitlist_position=position,
                charge_ref=charge_ref,
                credit_spent=credit_spent,
            )
        )

        if gets_seat:
            self.notifier.booking_confirmed(member, session)
        else:
            self.notifier.waitlisted(member, session, position or 0)

        return BookingResult(
            booking=booking,
            waitlisted=not gets_seat,
            position=position,
            charged_cents=charged,
            credits_left=credits_left,
        )

    def _check_member(self, member: Member, now: datetime) -> None:
        if not member.dues_paid:
            raise errors.DuesUnpaid()
        if policies.is_blocked(member.blocked_until, now):
            raise errors.MemberBlocked()

    def _check_class(self, member: Member, session: ClassSession, now: datetime) -> None:
        if not policies.level_is_enough(member.level, session.min_level):
            raise errors.LevelTooLow(
                f"'{session.name}' requires {session.min_level} and member is {member.level}"
            )
        if session.starts_at <= now:
            raise errors.ClassAlreadyStarted()
        if not policies.within_booking_window(session.starts_at, now):
            raise errors.OutsideBookingWindow()

    def _check_agenda(self, member: Member, session: ClassSession) -> None:
        for booking in self.bookings.for_member(member.id):
            if not booking.status.is_active:
                continue
            if booking.class_id == session.id:
                raise errors.DuplicateBooking()
            other = self.classes.get(booking.class_id)
            if other is not None and policies.overlap(other, session):
                raise errors.OverlappingBooking(
                    f"Overlaps '{other.name}' at {other.starts_at:%H:%M}"
                )
