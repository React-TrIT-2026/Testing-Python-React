from __future__ import annotations

from datetime import datetime, timedelta


class SystemClock:
    def now(self) -> datetime:
        return datetime.now()  # noqa: DTZ005


class FixedClock:
    def __init__(self, instant: datetime) -> None:
        self._instant = instant

    def now(self) -> datetime:
        return self._instant

    def advance(self, **delta: int) -> None:
        self._instant += timedelta(**delta)

    def move_to(self, instant: datetime) -> None:
        self._instant = instant
