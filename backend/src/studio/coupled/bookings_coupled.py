from __future__ import annotations

import os
from datetime import datetime, timedelta

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from studio.infrastructure.db_models import Base, BookingRow, ClassRow, MemberRow

DATABASE_URL = os.getenv("STUDIO_COUPLED_DATABASE_URL", "sqlite:///./studio_coupled.db")
_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(_engine)
_SessionFactory = sessionmaker(bind=_engine)

PAYMENTS_URL = os.getenv("STUDIO_PAYMENTS_URL", "https://payments.example.com")
NOTIFICATIONS_URL = os.getenv("STUDIO_NOTIFICATIONS_URL", "https://notifications.example.com")


def book_class(member_id: int, class_id: int) -> dict:
    session = _SessionFactory()
    try:
        member = session.get(MemberRow, member_id)
        if member is None:
            return {"ok": False, "error": "member not found"}
        row = session.get(ClassRow, class_id)
        if row is None:
            return {"ok": False, "error": "class not found"}

        now = datetime.now()

        if not member.dues_paid:
            return {"ok": False, "error": "dues unpaid"}
        if member.blocked_until is not None and now < member.blocked_until:
            return {"ok": False, "error": "member blocked"}
        if row.starts_at <= now:
            return {"ok": False, "error": "class already started"}
        if row.starts_at - now > timedelta(days=14):
            return {"ok": False, "error": "outside booking window"}

        ranks = {"beginner": 0, "intermediate": 1, "advanced": 2}
        if ranks[member.level] < ranks[row.min_level]:
            return {"ok": False, "error": "level too low"}

        taken = (
            session.query(BookingRow)
            .filter(
                BookingRow.class_id == class_id, BookingRow.status.in_(["confirmed", "attended"])
            )
            .count()
        )
        gets_seat = taken < row.capacity

        charge_ref = None
        if gets_seat and member.plan == "pay_per_class":
            response = requests.post(
                f"{PAYMENTS_URL}/charges",
                json={"email": member.email, "amount_cents": row.price_cents},
                timeout=5,
            )
            if response.status_code >= 400:
                return {"ok": False, "error": "payment declined"}
            charge_ref = response.json()["reference"]

        credit_spent = False
        if gets_seat and member.plan == "ten_pass":
            if member.credits <= 0:
                return {"ok": False, "error": "no credits left"}
            member.credits -= 1
            credit_spent = True

        position = None
        if not gets_seat:
            position = (
                session.query(BookingRow)
                .filter(BookingRow.class_id == class_id, BookingRow.status == "waitlisted")
                .count()
                + 1
            )

        booking = BookingRow(
            member_id=member_id,
            class_id=class_id,
            status="confirmed" if gets_seat else "waitlisted",
            created_at=now,
            waitlist_position=position,
            charge_ref=charge_ref,
            credit_spent=credit_spent,
        )
        session.add(booking)
        session.commit()

        requests.post(
            f"{NOTIFICATIONS_URL}/send",
            json={
                "email": member.email,
                "subject": "Booking confirmed" if gets_seat else "You are on the waitlist",
            },
            timeout=5,
        )

        return {
            "ok": True,
            "booking_id": booking.id,
            "status": booking.status,
            "position": position,
            "credits_left": member.credits,
        }
    finally:
        session.close()


def cancel_booking(booking_id: int) -> dict:
    session = _SessionFactory()
    try:
        booking = session.get(BookingRow, booking_id)
        if booking is None:
            return {"ok": False, "error": "booking not found"}
        if booking.status == "cancelled":
            return {"ok": False, "error": "already cancelled"}

        member = session.get(MemberRow, booking.member_id)
        row = session.get(ClassRow, booking.class_id)

        now = datetime.now()
        hours = (row.starts_at - now).total_seconds() / 3600
        held_seat = booking.status in ("confirmed", "attended")

        if not held_seat:
            refunds, penalty, band = False, 0, "waitlist"
        elif hours >= 12:
            refunds, penalty, band = True, 0, "free"
        elif hours >= 2:
            refunds, penalty, band = True, 1, "late"
        else:
            refunds, penalty, band = False, 1, "no_refund"

        credit_spent = booking.credit_spent
        booking.status = "cancelled"
        booking.waitlist_position = None

        if refunds and credit_spent:
            member.credits += 1
        if penalty and member.credits > 0:
            member.credits = max(0, member.credits - penalty)

        payment_refunded = False
        if refunds and booking.charge_ref:
            response = requests.post(
                f"{PAYMENTS_URL}/charges/{booking.charge_ref}/refund", timeout=5
            )
            payment_refunded = response.status_code < 400

        promoted_id = None
        if held_seat:
            taken = (
                session.query(BookingRow)
                .filter(
                    BookingRow.class_id == row.id,
                    BookingRow.status.in_(["confirmed", "attended"]),
                )
                .count()
            )
            if taken < row.capacity:
                next_up = (
                    session.query(BookingRow)
                    .filter(BookingRow.class_id == row.id, BookingRow.status == "waitlisted")
                    .order_by(BookingRow.waitlist_position)
                    .first()
                )
                if next_up is not None:
                    next_up.status = "confirmed"
                    next_up.waitlist_position = None
                    promoted_id = next_up.id
                    promoted_member = session.get(MemberRow, next_up.member_id)
                    requests.post(
                        f"{NOTIFICATIONS_URL}/send",
                        json={"email": promoted_member.email, "subject": "A seat opened up"},
                        timeout=5,
                    )
                    rest = (
                        session.query(BookingRow)
                        .filter(BookingRow.class_id == row.id, BookingRow.status == "waitlisted")
                        .order_by(BookingRow.waitlist_position)
                        .all()
                    )
                    for index, item in enumerate(rest, start=1):
                        item.waitlist_position = index

        requests.post(
            f"{NOTIFICATIONS_URL}/send",
            json={"email": member.email, "subject": f"Cancellation {band}"},
            timeout=5,
        )
        session.commit()

        return {
            "ok": True,
            "band": band,
            "credit_refunded": refunds and credit_spent,
            "penalty": penalty,
            "payment_refunded": payment_refunded,
            "promoted_id": promoted_id,
            "credits_left": member.credits,
        }
    finally:
        session.close()
