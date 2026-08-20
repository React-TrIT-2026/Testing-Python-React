from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from studio.domain.models import Booking, ClassOccupancy, Member


class MemberOut(BaseModel):
    id: int
    name: str
    email: str
    plan: str
    level: str
    credits: int
    dues_paid: bool
    blocked_until: datetime | None = None

    @classmethod
    def from_domain(cls, member: Member) -> MemberOut:
        return cls(
            id=member.id,
            name=member.name,
            email=member.email,
            plan=member.plan.value,
            level=member.level.value,
            credits=member.credits,
            dues_paid=member.dues_paid,
            blocked_until=member.blocked_until,
        )


class ClassOut(BaseModel):
    id: int
    name: str
    discipline: str
    starts_at: datetime
    ends_at: datetime
    duration_min: int
    capacity: int
    room: str
    min_level: str
    price_cents: int
    instructor: str
    confirmed: int
    waitlisted: int
    seats_left: int
    full: bool

    @classmethod
    def from_occupancy(cls, occupancy: ClassOccupancy) -> ClassOut:
        s = occupancy.session
        return cls(
            id=s.id,
            name=s.name,
            discipline=s.discipline,
            starts_at=s.starts_at,
            ends_at=s.ends_at,
            duration_min=s.duration_min,
            capacity=s.capacity,
            room=s.room,
            min_level=s.min_level.value,
            price_cents=s.price_cents,
            instructor=s.instructor,
            confirmed=occupancy.confirmed,
            waitlisted=occupancy.waitlisted,
            seats_left=occupancy.seats_left,
            full=occupancy.full,
        )


class BookingOut(BaseModel):
    id: int
    member_id: int
    class_id: int
    status: str
    created_at: datetime
    waitlist_position: int | None = None

    @classmethod
    def from_domain(cls, booking: Booking) -> BookingOut:
        return cls(
            id=booking.id,
            member_id=booking.member_id,
            class_id=booking.class_id,
            status=booking.status.value,
            created_at=booking.created_at,
            waitlist_position=booking.waitlist_position,
        )


class CreateBookingIn(BaseModel):
    member_id: int = Field(gt=0)
    class_id: int = Field(gt=0)


class BookingResponse(BaseModel):
    booking: BookingOut
    waitlisted: bool
    position: int | None = None
    charged_cents: int = 0
    credits_left: int | None = None


class CancellationResponse(BaseModel):
    booking: BookingOut
    band: str
    credit_refunded: bool
    penalty: int
    payment_refunded: bool
    promoted: BookingOut | None = None


class AttendanceIn(BaseModel):
    attended: bool


class ReminderDispatchOut(BaseModel):
    window_hours: int
    sent: int
    failed: int
    recipients: list[str]


class ResetIn(BaseModel):
    now: datetime | None = None
