from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from studio.domain.models import (
    Booking,
    BookingStatus,
    ClassSession,
    Level,
    Member,
    NoShow,
    Plan,
)


class Base(DeclarativeBase):
    pass


class MemberRow(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    plan: Mapped[str] = mapped_column(String(40), nullable=False)
    level: Mapped[str] = mapped_column(String(20), default=Level.BEGINNER.value)
    credits: Mapped[int] = mapped_column(Integer, default=0)
    dues_paid: Mapped[bool] = mapped_column(Boolean, default=True)
    blocked_until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def to_domain(self) -> Member:
        return Member(
            id=self.id,
            name=self.name,
            email=self.email,
            plan=Plan(self.plan),
            level=Level(self.level),
            credits=self.credits,
            dues_paid=self.dues_paid,
            blocked_until=self.blocked_until,
        )

    @classmethod
    def from_domain(cls, member: Member) -> MemberRow:
        return cls(
            id=member.id or None,
            name=member.name,
            email=member.email,
            plan=member.plan.value,
            level=member.level.value,
            credits=member.credits,
            dues_paid=member.dues_paid,
            blocked_until=member.blocked_until,
        )


class ClassRow(Base):
    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    discipline: Mapped[str] = mapped_column(String(60), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_min: Mapped[int] = mapped_column(Integer, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    room: Mapped[str] = mapped_column(String(60), nullable=False)
    min_level: Mapped[str] = mapped_column(String(20), default=Level.BEGINNER.value)
    price_cents: Mapped[int] = mapped_column(Integer, default=1200)
    instructor: Mapped[str] = mapped_column(String(120), default="Studio team")

    def to_domain(self) -> ClassSession:
        return ClassSession(
            id=self.id,
            name=self.name,
            discipline=self.discipline,
            starts_at=self.starts_at,
            duration_min=self.duration_min,
            capacity=self.capacity,
            room=self.room,
            min_level=Level(self.min_level),
            price_cents=self.price_cents,
            instructor=self.instructor,
        )

    @classmethod
    def from_domain(cls, session: ClassSession) -> ClassRow:
        return cls(
            id=session.id or None,
            name=session.name,
            discipline=session.discipline,
            starts_at=session.starts_at,
            duration_min=session.duration_min,
            capacity=session.capacity,
            room=session.room,
            min_level=session.min_level.value,
            price_cents=session.price_cents,
            instructor=session.instructor,
        )


class BookingRow(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), nullable=False)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    waitlist_position: Mapped[int | None] = mapped_column(Integer, nullable=True)
    charge_ref: Mapped[str | None] = mapped_column(String(60), nullable=True)
    credit_spent: Mapped[bool] = mapped_column(Boolean, default=False)

    def to_domain(self) -> Booking:
        return Booking(
            id=self.id,
            member_id=self.member_id,
            class_id=self.class_id,
            status=BookingStatus(self.status),
            created_at=self.created_at,
            waitlist_position=self.waitlist_position,
            charge_ref=self.charge_ref,
            credit_spent=self.credit_spent,
        )


class NoShowRow(Base):
    __tablename__ = "no_shows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), nullable=False)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    happened_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def to_domain(self) -> NoShow:
        return NoShow(
            member_id=self.member_id, class_id=self.class_id, happened_at=self.happened_at
        )
