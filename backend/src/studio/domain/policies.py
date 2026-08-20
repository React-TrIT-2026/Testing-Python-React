from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from studio.domain.models import ClassSession, Level, Plan

FREE_CANCELLATION_HOURS = 12
NO_REFUND_HOURS = 2
MAX_BOOKING_DAYS_AHEAD = 14
MAX_NO_SHOWS = 3
NO_SHOW_WINDOW_DAYS = 30
BLOCK_DURATION_DAYS = 7


@dataclass(frozen=True, slots=True)
class CancellationOutcome:
    refunds_credit: bool
    credit_penalty: int
    band: str

    def __post_init__(self) -> None:
        if self.credit_penalty < 0:
            raise ValueError("Credit penalty cannot be negative")


def hours_until(starts_at: datetime, now: datetime) -> float:
    return (starts_at - now).total_seconds() / 3600


def cancellation_outcome(starts_at: datetime, now: datetime) -> CancellationOutcome:
    margin = hours_until(starts_at, now)

    if margin >= FREE_CANCELLATION_HOURS:
        return CancellationOutcome(refunds_credit=True, credit_penalty=0, band="free")
    if margin >= NO_REFUND_HOURS:
        return CancellationOutcome(refunds_credit=True, credit_penalty=1, band="late")
    return CancellationOutcome(refunds_credit=False, credit_penalty=1, band="no_refund")


def within_booking_window(starts_at: datetime, now: datetime) -> bool:
    if starts_at <= now:
        return False
    return starts_at - now <= timedelta(days=MAX_BOOKING_DAYS_AHEAD)


def spends_credit(plan: Plan) -> bool:
    return plan is Plan.TEN_PASS


def requires_payment(plan: Plan) -> bool:
    return plan is Plan.PAY_PER_CLASS


def level_is_enough(member_level: Level, min_level: Level) -> bool:
    return member_level.rank >= min_level.rank


def overlap(a: ClassSession, b: ClassSession) -> bool:
    if a.id == b.id:
        return True
    return a.starts_at < b.ends_at and b.starts_at < a.ends_at


def no_shows_in_window(
    no_shows: list[datetime], now: datetime, days: int = NO_SHOW_WINDOW_DAYS
) -> int:
    since = now - timedelta(days=days)
    return sum(1 for date in no_shows if since <= date <= now)


def block_for_no_shows(no_shows: list[datetime], now: datetime) -> datetime | None:
    if no_shows_in_window(no_shows, now) >= MAX_NO_SHOWS:
        return now + timedelta(days=BLOCK_DURATION_DAYS)
    return None


def is_blocked(blocked_until: datetime | None, now: datetime) -> bool:
    if blocked_until is None:
        return False
    return now < blocked_until
