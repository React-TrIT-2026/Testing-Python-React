from __future__ import annotations

from studio.domain.models import BookingStatus, ClassOccupancy
from studio.ports import BookingRepository, ClassRepository, Clock


class GetSchedule:
    def __init__(self, classes: ClassRepository, bookings: BookingRepository, clock: Clock) -> None:
        self.classes = classes
        self.bookings = bookings
        self.clock = clock

    def execute(self) -> list[ClassOccupancy]:
        now = self.clock.now()
        schedule = []
        for session in self.classes.list_all(since=now):
            bookings = self.bookings.for_class(session.id)
            schedule.append(
                ClassOccupancy(
                    session=session,
                    confirmed=sum(1 for b in bookings if b.status.takes_seat),
                    waitlisted=sum(1 for b in bookings if b.status is BookingStatus.WAITLISTED),
                )
            )
        return schedule
