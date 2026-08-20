from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from studio.api.dependencies import (
    book_class_use_case,
    cancel_booking_use_case,
    record_attendance_use_case,
)
from studio.api.schemas import (
    AttendanceIn,
    BookingOut,
    BookingResponse,
    CancellationResponse,
    CreateBookingIn,
)
from studio.application.book_class import BookClass
from studio.application.cancel_booking import CancelBooking
from studio.application.record_attendance import RecordAttendance

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    payload: CreateBookingIn,
    book: Annotated[BookClass, Depends(book_class_use_case)],
) -> BookingResponse:
    result = book.execute(payload.member_id, payload.class_id)
    return BookingResponse(
        booking=BookingOut.from_domain(result.booking),
        waitlisted=result.waitlisted,
        position=result.position,
        charged_cents=result.charged_cents,
        credits_left=result.credits_left,
    )


@router.delete("/{booking_id}", response_model=CancellationResponse)
def cancel_booking(
    booking_id: int,
    cancel: Annotated[CancelBooking, Depends(cancel_booking_use_case)],
) -> CancellationResponse:
    result = cancel.execute(booking_id)
    return CancellationResponse(
        booking=BookingOut.from_domain(result.booking),
        band=result.band,
        credit_refunded=result.credit_refunded,
        penalty=result.penalty,
        payment_refunded=result.payment_refunded,
        promoted=BookingOut.from_domain(result.promoted) if result.promoted else None,
    )


@router.post("/{booking_id}/attendance", response_model=BookingOut)
def record_attendance(
    booking_id: int,
    payload: AttendanceIn,
    attendance: Annotated[RecordAttendance, Depends(record_attendance_use_case)],
) -> BookingOut:
    result = attendance.execute(booking_id, attended=payload.attended)
    return BookingOut.from_domain(result.booking)
