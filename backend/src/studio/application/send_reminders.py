from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from studio.domain.models import BookingStatus
from studio.infrastructure.async_notifications import DispatchReport, Reminder
from studio.ports import BookingRepository, ClassRepository, Clock, MemberRepository, ReminderSender

REMINDER_WINDOW_HOURS = 24


@dataclass(frozen=True, slots=True)
class ReminderSummary:
    reminders: list[Reminder]
    report: DispatchReport


class SendReminders:
    def __init__(
        self,
        members: MemberRepository,
        classes: ClassRepository,
        bookings: BookingRepository,
        sender: ReminderSender,
        clock: Clock,
    ) -> None:
        self.members = members
        self.classes = classes
        self.bookings = bookings
        self.sender = sender
        self.clock = clock

    def build_reminders(self, window_hours: int = REMINDER_WINDOW_HOURS) -> list[Reminder]:
        now = self.clock.now()
        deadline = now + timedelta(hours=window_hours)

        reminders = []
        for session in self.classes.list_all(since=now):
            if session.starts_at > deadline:
                continue
            for booking in self.bookings.for_class(session.id):
                if booking.status is not BookingStatus.CONFIRMED:
                    continue
                member = self.members.get(booking.member_id)
                if member is None:
                    continue
                reminders.append(
                    Reminder(
                        email=member.email,
                        subject=f"Recordatorio: {session.name}",
                        body=(
                            f"Hola {member.name}, te esperamos en {session.name} "
                            f"el {session.starts_at:%d/%m a las %H:%M} en {session.room}."
                        ),
                    )
                )
        return reminders

    async def execute(self, window_hours: int = REMINDER_WINDOW_HOURS) -> ReminderSummary:
        reminders = self.build_reminders(window_hours)
        report = await self.sender.send_all(reminders)
        return ReminderSummary(reminders=reminders, report=report)
