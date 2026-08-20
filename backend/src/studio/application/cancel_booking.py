from __future__ import annotations

from studio.application.results import CancellationResult
from studio.domain import capacity, errors, policies
from studio.domain.models import Booking, BookingStatus, ClassSession
from studio.ports import (
    BookingRepository,
    ClassRepository,
    Clock,
    MemberRepository,
    Notifier,
    PaymentGateway,
)


class CancelBooking:
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

    def execute(self, booking_id: int) -> CancellationResult:
        now = self.clock.now()

        booking = self.bookings.get(booking_id)
        if booking is None:
            raise errors.BookingNotFound()
        if booking.status is BookingStatus.CANCELLED:
            raise errors.BookingAlreadyCancelled()

        member = self.members.get(booking.member_id)
        session = self.classes.get(booking.class_id)
        if member is None:
            raise errors.MemberNotFound()
        if session is None:
            raise errors.ClassNotFound()

        held_seat = booking.status.takes_seat

        if held_seat:
            outcome = policies.cancellation_outcome(session.starts_at, now)
        else:
            outcome = policies.CancellationOutcome(
                refunds_credit=False, credit_penalty=0, band="waitlist"
            )

        cancelled = self.bookings.save(
            booking.with_status(BookingStatus.CANCELLED).with_waitlist_position(None)
        )

        credit_refunded = False
        if outcome.refunds_credit and booking.credit_spent:
            member = self.members.save(member.with_credits(member.credits + 1))
            credit_refunded = True

        if outcome.credit_penalty and member.credits > 0:
            member = self.members.save(
                member.with_credits(max(0, member.credits - outcome.credit_penalty))
            )

        payment_refunded = False
        if outcome.refunds_credit and booking.charge_ref:
            payment_refunded = self.payments.refund(booking.charge_ref)

        promoted = None
        if held_seat:
            promoted = self._promote_from_waitlist(session)
        else:
            self._renumber_waitlist(session)

        self.notifier.booking_cancelled(member, session, outcome.band)

        return CancellationResult(
            booking=cancelled,
            band=outcome.band,
            credit_refunded=credit_refunded,
            penalty=outcome.credit_penalty,
            promoted=promoted,
            payment_refunded=payment_refunded,
        )

    def _promote_from_waitlist(self, session: ClassSession) -> Booking | None:
        remaining = self.bookings.for_class(session.id)
        candidate = capacity.first_in_line(remaining)
        if candidate is None:
            return None
        if not capacity.has_room(session.capacity, remaining):
            return None

        promoted = self.bookings.save(
            candidate.with_status(BookingStatus.CONFIRMED).with_waitlist_position(None)
        )
        for moved in capacity.renumber(self.bookings.for_class(session.id)):
            self.bookings.save(moved)

        promoted_member = self.members.get(promoted.member_id)
        if promoted_member is not None:
            self.notifier.seat_released(promoted_member, session)
        return promoted

    def _renumber_waitlist(self, session: ClassSession) -> None:
        for moved in capacity.renumber(self.bookings.for_class(session.id)):
            self.bookings.save(moved)
