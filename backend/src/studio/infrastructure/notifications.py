from __future__ import annotations

import logging
from datetime import datetime

from studio.domain.models import ClassSession, Member

log = logging.getLogger("studio.notifications")


class LoggingNotifier:
    def booking_confirmed(self, member: Member, session: ClassSession) -> None:
        log.info("Booking confirmed: %s -> %s (%s)", member.email, session.name, session.starts_at)

    def waitlisted(self, member: Member, session: ClassSession, position: int) -> None:
        log.info("Waitlist #%s: %s -> %s", position, member.email, session.name)

    def seat_released(self, member: Member, session: ClassSession) -> None:
        log.info("Seat released for %s in %s", member.email, session.name)

    def booking_cancelled(self, member: Member, session: ClassSession, band: str) -> None:
        log.info("Cancellation %s: %s in %s", band, member.email, session.name)

    def member_blocked(self, member: Member, until: datetime) -> None:
        log.warning("Member %s blocked until %s", member.email, until)


class RecordingNotifier:
    def __init__(self) -> None:
        self.notices: list[tuple[str, str]] = []

    def _record(self, event: str, member: Member) -> None:
        self.notices.append((event, member.email))

    def events(self) -> list[str]:
        return [event for event, _ in self.notices]

    def booking_confirmed(self, member: Member, session: ClassSession) -> None:
        del session
        self._record("booking_confirmed", member)

    def waitlisted(self, member: Member, session: ClassSession, position: int) -> None:
        del session, position
        self._record("waitlisted", member)

    def seat_released(self, member: Member, session: ClassSession) -> None:
        del session
        self._record("seat_released", member)

    def booking_cancelled(self, member: Member, session: ClassSession, band: str) -> None:
        del session, band
        self._record("booking_cancelled", member)

    def member_blocked(self, member: Member, until: datetime) -> None:
        del until
        self._record("member_blocked", member)
