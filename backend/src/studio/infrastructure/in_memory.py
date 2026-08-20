from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from itertools import count

from studio.domain.models import Booking, ClassSession, Member, NoShow


class InMemoryMemberRepository:
    def __init__(self, members: list[Member] | None = None) -> None:
        self._members: dict[int, Member] = {m.id: m for m in (members or [])}
        self._next_id = count(max(self._members, default=0) + 1)

    def get(self, member_id: int) -> Member | None:
        return self._members.get(member_id)

    def save(self, member: Member) -> Member:
        if member.id == 0:
            member = replace(member, id=next(self._next_id))
        self._members[member.id] = member
        return member

    def list_all(self) -> list[Member]:
        return sorted(self._members.values(), key=lambda m: m.id)


class InMemoryClassRepository:
    def __init__(self, sessions: list[ClassSession] | None = None) -> None:
        self._sessions: dict[int, ClassSession] = {s.id: s for s in (sessions or [])}

    def get(self, class_id: int) -> ClassSession | None:
        return self._sessions.get(class_id)

    def save(self, session: ClassSession) -> ClassSession:
        self._sessions[session.id] = session
        return session

    def list_all(self, since: datetime | None = None) -> list[ClassSession]:
        sessions = sorted(self._sessions.values(), key=lambda s: s.starts_at)
        if since is None:
            return sessions
        return [s for s in sessions if s.starts_at >= since]


class InMemoryBookingRepository:
    def __init__(self) -> None:
        self._bookings: dict[int, Booking] = {}
        self._no_shows: list[NoShow] = []
        self._next_id = count(1)

    def get(self, booking_id: int) -> Booking | None:
        return self._bookings.get(booking_id)

    def add(self, booking: Booking) -> Booking:
        created = replace(booking, id=next(self._next_id))
        self._bookings[created.id] = created
        return created

    def save(self, booking: Booking) -> Booking:
        self._bookings[booking.id] = booking
        return booking

    def for_class(self, class_id: int) -> list[Booking]:
        return sorted(
            (b for b in self._bookings.values() if b.class_id == class_id), key=lambda b: b.id
        )

    def for_member(self, member_id: int) -> list[Booking]:
        return sorted(
            (b for b in self._bookings.values() if b.member_id == member_id), key=lambda b: b.id
        )

    def no_shows_of(self, member_id: int) -> list[NoShow]:
        return [n for n in self._no_shows if n.member_id == member_id]

    def record_no_show(self, no_show: NoShow) -> None:
        self._no_shows.append(no_show)
