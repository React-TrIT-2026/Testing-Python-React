from __future__ import annotations


class DomainError(Exception):
    code = "domain_error"
    message = "The operation breaks a business rule"

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.message)


class MemberNotFound(DomainError):
    code = "member_not_found"
    message = "Member does not exist"


class ClassNotFound(DomainError):
    code = "class_not_found"
    message = "Class does not exist"


class BookingNotFound(DomainError):
    code = "booking_not_found"
    message = "Booking does not exist"


class DuesUnpaid(DomainError):
    code = "dues_unpaid"
    message = "Member has outstanding dues"


class MemberBlocked(DomainError):
    code = "member_blocked"
    message = "Member is temporarily blocked for repeated no-shows"


class LevelTooLow(DomainError):
    code = "level_too_low"
    message = "Member level is below the class requirement"


class OverlappingBooking(DomainError):
    code = "overlapping_booking"
    message = "Member already has a booking that overlaps this time slot"


class DuplicateBooking(DomainError):
    code = "duplicate_booking"
    message = "Member already has an active booking for this class"


class OutsideBookingWindow(DomainError):
    code = "outside_booking_window"
    message = "Classes open for booking 14 days in advance at most"


class ClassAlreadyStarted(DomainError):
    code = "class_already_started"
    message = "The class has already started"


class NoCreditsLeft(DomainError):
    code = "no_credits_left"
    message = "Member has no credits left on the pass"


class BookingAlreadyCancelled(DomainError):
    code = "booking_already_cancelled"
    message = "Booking was already cancelled"


class PaymentDeclined(DomainError):
    code = "payment_declined"
    message = "The payment gateway declined the charge"
