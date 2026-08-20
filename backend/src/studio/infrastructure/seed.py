from __future__ import annotations

from datetime import datetime, timedelta

from studio.domain.models import ClassSession, Level, Member, Plan

DEMO_MEMBERS = [
    Member(1, "Ana Beltran", "ana@example.com", Plan.TEN_PASS, Level.INTERMEDIATE, credits=6),
    Member(2, "Luis Ferrer", "luis@example.com", Plan.UNLIMITED, Level.ADVANCED),
    Member(3, "Uxia Nogueira", "uxia@example.com", Plan.PAY_PER_CLASS, Level.BEGINNER),
    Member(4, "Marc Oliva", "marc@example.com", Plan.TEN_PASS, Level.BEGINNER, credits=0),
    Member(
        5, "Sara Quintana", "sara@example.com", Plan.UNLIMITED, Level.INTERMEDIATE, dues_paid=False
    ),
]

CLASS_TEMPLATE = [
    (0, 19, 0, "Body Pump", "strength", 55, 20, "Studio 1", Level.BEGINNER, 1200, "Ana Ruiz"),
    (
        0,
        20,
        30,
        "Night Cycling",
        "cycling",
        45,
        16,
        "Cycle Room",
        Level.INTERMEDIATE,
        1000,
        "Jon Aramendi",
    ),
    (
        1,
        7,
        0,
        "Cross Training",
        "functional",
        60,
        12,
        "The Box",
        Level.ADVANCED,
        1500,
        "Nerea Diaz",
    ),
    (1, 10, 0, "Mat Pilates", "mind-body", 50, 14, "Studio 2", Level.BEGINNER, 1100, "Clara Vidal"),
    (1, 19, 0, "Zumba", "dance", 55, 25, "Studio 1", Level.BEGINNER, 900, "Paula Serra"),
    (
        2,
        8,
        0,
        "HIIT Express",
        "functional",
        30,
        10,
        "The Box",
        Level.INTERMEDIATE,
        1000,
        "Nerea Diaz",
    ),
    (
        2,
        18,
        0,
        "Restorative Yoga",
        "mind-body",
        60,
        18,
        "Studio 2",
        Level.BEGINNER,
        1100,
        "Clara Vidal",
    ),
    (3, 19, 0, "Body Pump", "strength", 55, 20, "Studio 1", Level.BEGINNER, 1200, "Ana Ruiz"),
    (
        4,
        7,
        0,
        "Cross Training",
        "functional",
        60,
        12,
        "The Box",
        Level.ADVANCED,
        1500,
        "Nerea Diaz",
    ),
    (
        5,
        11,
        0,
        "Cycling Marathon",
        "cycling",
        90,
        16,
        "Cycle Room",
        Level.INTERMEDIATE,
        1800,
        "Jon Aramendi",
    ),
    (8, 19, 0, "Body Pump", "strength", 55, 20, "Studio 1", Level.BEGINNER, 1200, "Ana Ruiz"),
    (
        10,
        10,
        0,
        "Mat Pilates",
        "mind-body",
        50,
        14,
        "Studio 2",
        Level.BEGINNER,
        1100,
        "Clara Vidal",
    ),
]


def demo_classes(now: datetime) -> list[ClassSession]:
    sessions = []
    for index, (
        days,
        hour,
        minute,
        name,
        discipline,
        duration,
        cap,
        room,
        level,
        price,
        instructor,
    ) in enumerate(CLASS_TEMPLATE, start=1):
        starts_at = (now + timedelta(days=days)).replace(
            hour=hour, minute=minute, second=0, microsecond=0
        )
        if starts_at <= now:
            starts_at += timedelta(days=1)
        sessions.append(
            ClassSession(
                id=index,
                name=name,
                discipline=discipline,
                starts_at=starts_at,
                duration_min=duration,
                capacity=cap,
                room=room,
                min_level=level,
                price_cents=price,
                instructor=instructor,
            )
        )
    return sorted(sessions, key=lambda s: s.starts_at)
