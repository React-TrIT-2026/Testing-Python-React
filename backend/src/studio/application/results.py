from __future__ import annotations

from dataclasses import dataclass

from studio.domain.models import Booking, ClassSession, Member


@dataclass(frozen=True, slots=True)
class BookingResult:
    booking: Booking
    waitlisted: bool
    position: int | None
    charged_cents: int = 0
    credits_left: int | None = None


@dataclass(frozen=True, slots=True)
class CancellationResult:
    booking: Booking
    band: str
    credit_refunded: bool
    penalty: int
    promoted: Booking | None = None
    payment_refunded: bool = False


@dataclass(frozen=True, slots=True)
class AttendanceResult:
    booking: Booking
    member: Member
    session: ClassSession
    block_applied: bool = False
