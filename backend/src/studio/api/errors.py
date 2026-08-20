from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from studio.domain import errors

HTTP_STATUS: dict[type[errors.DomainError], int] = {
    errors.MemberNotFound: 404,
    errors.ClassNotFound: 404,
    errors.BookingNotFound: 404,
    errors.DuesUnpaid: 402,
    errors.PaymentDeclined: 402,
    errors.MemberBlocked: 403,
    errors.LevelTooLow: 403,
    errors.OverlappingBooking: 409,
    errors.DuplicateBooking: 409,
    errors.BookingAlreadyCancelled: 409,
    errors.OutsideBookingWindow: 422,
    errors.ClassAlreadyStarted: 422,
    errors.NoCreditsLeft: 422,
}


def status_for(error: errors.DomainError) -> int:
    return HTTP_STATUS.get(type(error), 400)


def register_handlers(app: FastAPI) -> None:
    @app.exception_handler(errors.DomainError)
    async def _handle_domain_error(_: Request, error: errors.DomainError) -> JSONResponse:
        return JSONResponse(
            status_code=status_for(error),
            content={"code": error.code, "detail": str(error)},
        )
