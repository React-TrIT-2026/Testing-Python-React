from __future__ import annotations

import asyncio
from dataclasses import dataclass

import httpx

HTTP_BAD_REQUEST = 400


@dataclass(frozen=True, slots=True)
class Reminder:
    email: str
    subject: str
    body: str


@dataclass(frozen=True, slots=True)
class DispatchReport:
    sent: int
    failed: int

    @property
    def total(self) -> int:
        return self.sent + self.failed


class AsyncHttpReminderSender:
    def __init__(self, base_url: str, timeout: float = 5.0, max_concurrency: int = 8) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_concurrency = max_concurrency

    async def send_all(self, reminders: list[Reminder]) -> DispatchReport:
        if not reminders:
            return DispatchReport(0, 0)

        limit = asyncio.Semaphore(self.max_concurrency)

        async with httpx.AsyncClient(timeout=self.timeout) as client:

            async def send_one(reminder: Reminder) -> bool:
                async with limit:
                    try:
                        response = await client.post(
                            f"{self.base_url}/send",
                            json={
                                "email": reminder.email,
                                "subject": reminder.subject,
                                "body": reminder.body,
                            },
                        )
                    except httpx.HTTPError:
                        return False
                    return response.status_code < HTTP_BAD_REQUEST

            outcomes = await asyncio.gather(*(send_one(r) for r in reminders))

        sent = sum(1 for ok in outcomes if ok)
        return DispatchReport(sent=sent, failed=len(outcomes) - sent)


class RecordingReminderSender:
    def __init__(self, fail_for: set[str] | None = None) -> None:
        self.fail_for = fail_for or set()
        self.sent: list[Reminder] = []

    async def send_all(self, reminders: list[Reminder]) -> DispatchReport:
        failed = 0
        for reminder in reminders:
            if reminder.email in self.fail_for:
                failed += 1
                continue
            self.sent.append(reminder)
        return DispatchReport(sent=len(reminders) - failed, failed=failed)
