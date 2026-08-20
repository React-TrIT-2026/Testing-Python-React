from __future__ import annotations

import argparse
import sys
from pathlib import Path

from studio.application.export_schedule import ExportSchedule
from studio.application.get_schedule import GetSchedule
from studio.domain.models import ClassOccupancy
from studio.infrastructure.clock import SystemClock
from studio.infrastructure.in_memory import (
    InMemoryBookingRepository,
    InMemoryClassRepository,
)
from studio.infrastructure.seed import demo_classes
from studio.ports import BookingRepository, ClassRepository, Clock

FULL_LABEL = "COMPLETA"


def build_schedule(
    classes: ClassRepository | None = None,
    bookings: BookingRepository | None = None,
    clock: Clock | None = None,
) -> GetSchedule:
    resolved_clock = clock or SystemClock()
    resolved_classes = classes or InMemoryClassRepository(demo_classes(resolved_clock.now()))
    resolved_bookings = bookings or InMemoryBookingRepository()
    return GetSchedule(resolved_classes, resolved_bookings, resolved_clock)


def format_row(occupancy: ClassOccupancy) -> str:
    session = occupancy.session
    seats = FULL_LABEL if occupancy.full else f"{occupancy.seats_left} libres"
    return f"{session.starts_at:%d/%m %H:%M}  {session.name:<20} {session.room:<12} {seats:>10}"


def render(occupancies: list[ClassOccupancy]) -> str:
    if not occupancies:
        return "No hay clases programadas."
    header = f"{'CUANDO':<13} {'CLASE':<20} {'SALA':<12} {'PLAZAS':>10}"
    lines = [header, "-" * len(header)]
    lines.extend(format_row(occupancy) for occupancy in occupancies)
    lines.append(f"\n{len(occupancies)} clases en el cuadrante.")
    return "\n".join(lines)


def main(argv: list[str] | None = None, schedule: GetSchedule | None = None) -> int:
    parser = argparse.ArgumentParser(prog="studio", description="Cuadrante de clases")
    parser.add_argument("--export", type=Path, help="Guarda el cuadrante en un CSV")
    args = parser.parse_args(argv)

    resolved = schedule or build_schedule()

    if args.export:
        report = ExportSchedule(resolved).to_csv(args.export)
        print(f"{report.rows} clases exportadas a {report.path}")
        return 0

    print(render(resolved.execute()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
