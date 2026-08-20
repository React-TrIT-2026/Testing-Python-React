from __future__ import annotations

from studio.domain.models import Booking, BookingStatus


def seats_taken(bookings: list[Booking]) -> int:
    return sum(1 for b in bookings if b.status.takes_seat)


def has_room(capacity: int, bookings: list[Booking]) -> bool:
    return seats_taken(bookings) < capacity


def waitlist(bookings: list[Booking]) -> list[Booking]:
    queued = [b for b in bookings if b.status is BookingStatus.WAITLISTED]
    return sorted(queued, key=lambda b: (b.waitlist_position or 0, b.id))


def next_waitlist_position(bookings: list[Booking]) -> int:
    return len(waitlist(bookings)) + 1


def first_in_line(bookings: list[Booking]) -> Booking | None:
    queued = waitlist(bookings)
    return queued[0] if queued else None


def renumber(bookings: list[Booking]) -> list[Booking]:
    moved = []
    for position, booking in enumerate(waitlist(bookings), start=1):
        if booking.waitlist_position != position:
            moved.append(booking.with_waitlist_position(position))
    return moved
