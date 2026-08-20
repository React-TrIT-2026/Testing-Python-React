from __future__ import annotations

import os
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from studio.application.book_class import BookClass
from studio.application.cancel_booking import CancelBooking
from studio.application.get_schedule import GetSchedule
from studio.application.record_attendance import RecordAttendance
from studio.application.send_reminders import SendReminders
from studio.infrastructure.async_notifications import (
    AsyncHttpReminderSender,
    RecordingReminderSender,
)
from studio.infrastructure.clock import FixedClock, SystemClock
from studio.infrastructure.in_memory import (
    InMemoryBookingRepository,
    InMemoryClassRepository,
    InMemoryMemberRepository,
)
from studio.infrastructure.notifications import LoggingNotifier
from studio.infrastructure.payments import FakePaymentGateway, HttpxPaymentGateway
from studio.infrastructure.seed import DEMO_MEMBERS, demo_classes
from studio.infrastructure.sql_repositories import (
    SqlBookingRepository,
    SqlClassRepository,
    SqlMemberRepository,
)
from studio.ports import (
    BookingRepository,
    ClassRepository,
    Clock,
    MemberRepository,
    Notifier,
    PaymentGateway,
    ReminderSender,
)

DATABASE_URL = os.getenv("STUDIO_DATABASE_URL", "sqlite:///./studio.db")
STORAGE = os.getenv("STUDIO_STORAGE", "memory")


@dataclass(frozen=True, slots=True)
class Repositories:
    members: MemberRepository
    classes: ClassRepository
    bookings: BookingRepository


class ClockOverride:
    instant: datetime | None = None


def get_clock() -> Clock:
    if ClockOverride.instant is not None:
        return FixedClock(ClockOverride.instant)
    return SystemClock()


def force_clock(instant: datetime | None) -> None:
    ClockOverride.instant = instant
    _memory_storage.cache_clear()


def get_notifier() -> LoggingNotifier:
    return LoggingNotifier()


def get_reminder_sender() -> ReminderSender:
    base_url = os.getenv("STUDIO_NOTIFICATIONS_URL")
    if base_url:
        return AsyncHttpReminderSender(base_url)
    return RecordingReminderSender()


def get_payment_gateway() -> PaymentGateway:
    api_key = os.getenv("STUDIO_PAYMENTS_API_KEY")
    base_url = os.getenv("STUDIO_PAYMENTS_URL")
    if api_key and base_url:
        return HttpxPaymentGateway(base_url, api_key)
    return FakePaymentGateway()


@lru_cache(maxsize=1)
def _memory_storage() -> Repositories:
    now = ClockOverride.instant or datetime.now()  # noqa: DTZ005
    return Repositories(
        members=InMemoryMemberRepository(list(DEMO_MEMBERS)),
        classes=InMemoryClassRepository(demo_classes(now)),
        bookings=InMemoryBookingRepository(),
    )


def reset_memory_storage() -> None:
    _memory_storage.cache_clear()
    _memory_storage()


@lru_cache(maxsize=1)
def _session_factory() -> sessionmaker[Session]:
    from studio.infrastructure.db_models import Base  # noqa: PLC0415

    connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_session() -> Iterator[Session | None]:
    if STORAGE == "memory":
        yield None
        return

    factory = _session_factory()
    session: Session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_repositories(
    session: Annotated[Session | None, Depends(get_session)],
) -> Repositories:
    if session is None:
        return _memory_storage()
    return Repositories(
        members=SqlMemberRepository(session),
        classes=SqlClassRepository(session),
        bookings=SqlBookingRepository(session),
    )


RepositoriesDep = Annotated[Repositories, Depends(get_repositories)]


def book_class_use_case(
    repos: RepositoriesDep,
    clock: Clock = Depends(get_clock),
    payments: PaymentGateway = Depends(get_payment_gateway),
    notifier: Notifier = Depends(get_notifier),
) -> BookClass:
    return BookClass(repos.members, repos.classes, repos.bookings, payments, notifier, clock)


def cancel_booking_use_case(
    repos: RepositoriesDep,
    clock: Clock = Depends(get_clock),
    payments: PaymentGateway = Depends(get_payment_gateway),
    notifier: Notifier = Depends(get_notifier),
) -> CancelBooking:
    return CancelBooking(repos.members, repos.classes, repos.bookings, payments, notifier, clock)


def record_attendance_use_case(
    repos: RepositoriesDep,
    clock: Clock = Depends(get_clock),
    notifier: Notifier = Depends(get_notifier),
) -> RecordAttendance:
    return RecordAttendance(repos.members, repos.classes, repos.bookings, notifier, clock)


def get_schedule_use_case(repos: RepositoriesDep, clock: Clock = Depends(get_clock)) -> GetSchedule:
    return GetSchedule(repos.classes, repos.bookings, clock)


def send_reminders_use_case(
    repos: RepositoriesDep,
    clock: Clock = Depends(get_clock),
    sender: ReminderSender = Depends(get_reminder_sender),
) -> SendReminders:
    return SendReminders(repos.members, repos.classes, repos.bookings, sender, clock)
