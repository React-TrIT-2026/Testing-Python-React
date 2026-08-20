from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from fastapi.testclient import TestClient

from studio.api import dependencies
from studio.api.app import create_app
from studio.api.dependencies import Repositories
from studio.infrastructure.clock import FixedClock
from studio.infrastructure.in_memory import (
    InMemoryBookingRepository,
    InMemoryClassRepository,
    InMemoryMemberRepository,
)
from studio.infrastructure.payments import FakePaymentGateway
from studio.infrastructure.seed import DEMO_MEMBERS, demo_classes

CONTRACTS = Path(__file__).resolve().parents[2] / "contracts"
FIXED_NOW = datetime(2026, 3, 11, 10, 0)  # noqa: DTZ001


def build_client() -> TestClient:
    app = create_app()
    clock = FixedClock(FIXED_NOW)
    repositories = Repositories(
        members=InMemoryMemberRepository(list(DEMO_MEMBERS)),
        classes=InMemoryClassRepository(demo_classes(FIXED_NOW)),
        bookings=InMemoryBookingRepository(),
    )
    app.dependency_overrides[dependencies.get_repositories] = lambda: repositories
    app.dependency_overrides[dependencies.get_clock] = lambda: clock
    gateway = FakePaymentGateway()
    app.dependency_overrides[dependencies.get_payment_gateway] = lambda: gateway
    return TestClient(app)


def main() -> None:
    CONTRACTS.mkdir(exist_ok=True)
    client = build_client()

    classes = client.get("/api/classes").json()
    members = client.get("/api/members").json()
    booking = client.post(
        "/api/bookings", json={"member_id": 2, "class_id": classes[0]["id"]}
    ).json()
    cancellation = client.delete(f"/api/bookings/{booking['booking']['id']}").json()

    examples = {
        "generatedAt": FIXED_NOW.isoformat(),
        "getClasses": classes,
        "getMembers": members,
        "postBooking": booking,
        "deleteBooking": cancellation,
        "errorNotFound": client.get("/api/members/999").json(),
    }
    (CONTRACTS / "api-examples.json").write_text(
        json.dumps(examples, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    openapi = create_app().openapi()
    shape = {
        "paths": {
            path: sorted(methods)
            for path, methods in sorted((p, list(m)) for p, m in openapi["paths"].items())
        },
        "schemas": {
            name: sorted(schema.get("properties", {}))
            for name, schema in sorted(openapi["components"]["schemas"].items())
        },
    }
    (CONTRACTS / "openapi-shape.json").write_text(
        json.dumps(shape, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"contracts written to {CONTRACTS}")


if __name__ == "__main__":
    main()
