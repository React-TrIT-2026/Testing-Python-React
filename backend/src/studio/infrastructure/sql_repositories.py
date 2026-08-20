from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from studio.domain.models import Booking, ClassSession, Member, NoShow
from studio.infrastructure.db_models import BookingRow, ClassRow, MemberRow, NoShowRow


class SqlMemberRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, member_id: int) -> Member | None:
        row = self.session.get(MemberRow, member_id)
        return row.to_domain() if row else None

    def save(self, member: Member) -> Member:
        row = self.session.get(MemberRow, member.id) if member.id else None
        if row is None:
            row = MemberRow.from_domain(member)
            self.session.add(row)
        else:
            row.name = member.name
            row.email = member.email
            row.plan = member.plan.value
            row.level = member.level.value
            row.credits = member.credits
            row.dues_paid = member.dues_paid
            row.blocked_until = member.blocked_until
        self.session.flush()
        return row.to_domain()

    def list_all(self) -> list[Member]:
        rows = self.session.scalars(select(MemberRow).order_by(MemberRow.id)).all()
        return [r.to_domain() for r in rows]


class SqlClassRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, class_id: int) -> ClassSession | None:
        row = self.session.get(ClassRow, class_id)
        return row.to_domain() if row else None

    def save(self, session: ClassSession) -> ClassSession:
        row = ClassRow.from_domain(session)
        self.session.add(row)
        self.session.flush()
        return row.to_domain()

    def list_all(self, since: datetime | None = None) -> list[ClassSession]:
        query = select(ClassRow).order_by(ClassRow.starts_at)
        if since is not None:
            query = query.where(ClassRow.starts_at >= since)
        return [r.to_domain() for r in self.session.scalars(query).all()]


class SqlBookingRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, booking_id: int) -> Booking | None:
        row = self.session.get(BookingRow, booking_id)
        return row.to_domain() if row else None

    def add(self, booking: Booking) -> Booking:
        row = BookingRow(
            member_id=booking.member_id,
            class_id=booking.class_id,
            status=booking.status.value,
            created_at=booking.created_at,
            waitlist_position=booking.waitlist_position,
            charge_ref=booking.charge_ref,
            credit_spent=booking.credit_spent,
        )
        self.session.add(row)
        self.session.flush()
        return row.to_domain()

    def save(self, booking: Booking) -> Booking:
        row = self.session.get(BookingRow, booking.id)
        if row is None:
            return self.add(booking)
        row.status = booking.status.value
        row.waitlist_position = booking.waitlist_position
        row.charge_ref = booking.charge_ref
        row.credit_spent = booking.credit_spent
        self.session.flush()
        return row.to_domain()

    def for_class(self, class_id: int) -> list[Booking]:
        rows = self.session.scalars(
            select(BookingRow).where(BookingRow.class_id == class_id).order_by(BookingRow.id)
        ).all()
        return [r.to_domain() for r in rows]

    def for_member(self, member_id: int) -> list[Booking]:
        rows = self.session.scalars(
            select(BookingRow).where(BookingRow.member_id == member_id).order_by(BookingRow.id)
        ).all()
        return [r.to_domain() for r in rows]

    def no_shows_of(self, member_id: int) -> list[NoShow]:
        rows = self.session.scalars(select(NoShowRow).where(NoShowRow.member_id == member_id)).all()
        return [r.to_domain() for r in rows]

    def record_no_show(self, no_show: NoShow) -> None:
        self.session.add(
            NoShowRow(
                member_id=no_show.member_id,
                class_id=no_show.class_id,
                happened_at=no_show.happened_at,
            )
        )
        self.session.flush()
