from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from studio.application.get_schedule import GetSchedule

COLUMNS = ("day", "time", "class", "room", "instructor", "level", "confirmed", "capacity")


@dataclass(frozen=True, slots=True)
class ExportReport:
    path: Path
    rows: int


class ExportSchedule:
    def __init__(self, schedule: GetSchedule) -> None:
        self.schedule = schedule

    def to_csv(self, destination: Path) -> ExportReport:
        occupancies = self.schedule.execute()
        destination.parent.mkdir(parents=True, exist_ok=True)

        with destination.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter=";")
            writer.writerow(COLUMNS)
            for occupancy in occupancies:
                session = occupancy.session
                writer.writerow(
                    [
                        f"{session.starts_at:%Y-%m-%d}",
                        f"{session.starts_at:%H:%M}",
                        session.name,
                        session.room,
                        session.instructor,
                        session.min_level.value,
                        occupancy.confirmed,
                        session.capacity,
                    ]
                )

        return ExportReport(path=destination, rows=len(occupancies))
