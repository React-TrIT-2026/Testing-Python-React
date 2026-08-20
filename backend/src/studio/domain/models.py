from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from enum import StrEnum


class Level(StrEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

    @property
    def rank(self) -> int:
        return {"beginner": 0, "intermediate": 1, "advanced": 2}[self.value]


class Plan(StrEnum):
    UNLIMITED = "unlimited"
    TEN_PASS = "ten_pass"  # noqa: S105
    PAY_PER_CLASS = "pay_per_class"


class BookingStatus(StrEnum):
    CONFIRMED = "confirmed"
    WAITLISTED = "waitlisted"
    CANCELLED = "cancelled"
    ATTENDED = "attended"
    NO_SHOW = "no_show"

    @property
    def takes_seat(self) -> bool:
        return self in (BookingStatus.CONFIRMED, BookingStatus.ATTENDED)

    @property
    def is_active(self) -> bool:
        return self in (
            BookingStatus.CONFIRMED,
            BookingStatus.WAITLISTED,
            BookingStatus.ATTENDED,
        )


@dataclass(frozen=True, slots=True)
class Member:
    id: int
    name: str
    email: str
    plan: Plan
    level: Level = Level.BEGINNER
    credits: int = 0
    dues_paid: bool = True
    blocked_until: datetime | None = None

    def with_credits(self, credits: int) -> Member:  # noqa: A002
        return replace(self, credits=credits)

    def blocked(self, until: datetime | None) -> Member:
        return replace(self, blocked_until=until)


@dataclass(frozen=True, slots=True)
class ClassSession:
    id: int
    name: str
    discipline: str
    starts_at: datetime
    duration_min: int
    capacity: int
    room: str
    min_level: Level = Level.BEGINNER
    price_cents: int = 1200
    instructor: str = "Studio team"

    @property
    def ends_at(self) -> datetime:
        return self.starts_at + timedelta(minutes=self.duration_min)


@dataclass(frozen=True, slots=True)
class Booking:
    id: int
    member_id: int
    class_id: int
    status: BookingStatus
    created_at: datetime
    waitlist_position: int | None = None
    charge_ref: str | None = None
    credit_spent: bool = False

    def with_status(self, status: BookingStatus) -> Booking:
        return replace(self, status=status)

    def with_waitlist_position(self, position: int | None) -> Booking:
        return replace(self, waitlist_position=position)


@dataclass(frozen=True, slots=True)
class NoShow:
    member_id: int
    class_id: int
    happened_at: datetime


@dataclass(slots=True)
class Charge:
    reference: str
    amount_cents: int
    successful: bool
    reason: str = ""


@dataclass(slots=True)
class ClassOccupancy:
    session: ClassSession
    confirmed: int
    waitlisted: int

    @property
    def seats_left(self) -> int:
        return max(0, self.session.capacity - self.confirmed)

    @property
    def full(self) -> bool:
        return self.seats_left == 0
