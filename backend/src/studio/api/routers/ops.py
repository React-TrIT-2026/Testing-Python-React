from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from studio.api.dependencies import send_reminders_use_case
from studio.api.schemas import ReminderDispatchOut
from studio.application.send_reminders import REMINDER_WINDOW_HOURS, SendReminders

router = APIRouter(prefix="/ops", tags=["ops"])


@router.post("/reminders", response_model=ReminderDispatchOut)
async def send_reminders(
    reminders: Annotated[SendReminders, Depends(send_reminders_use_case)],
    window_hours: int = Query(REMINDER_WINDOW_HOURS, ge=1, le=336),
) -> ReminderDispatchOut:
    summary = await reminders.execute(window_hours)
    return ReminderDispatchOut(
        window_hours=window_hours,
        sent=summary.report.sent,
        failed=summary.report.failed,
        recipients=[r.email for r in summary.reminders],
    )
