from __future__ import annotations

from itertools import count

import httpx
import requests

from studio.domain.models import Charge, Member

HTTP_BAD_REQUEST = 400
DEFAULT_TIMEOUT_SECONDS = 5.0


class RequestsPaymentGateway:
    def __init__(
        self, base_url: str, api_key: str, timeout: float = DEFAULT_TIMEOUT_SECONDS
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def charge(self, member: Member, amount_cents: int, concept: str) -> Charge:
        response = requests.post(
            f"{self.base_url}/charges",
            json={"email": member.email, "amount_cents": amount_cents, "concept": concept},
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=self.timeout,
        )
        if response.status_code >= HTTP_BAD_REQUEST:
            return Charge(
                reference="",
                amount_cents=amount_cents,
                successful=False,
                reason=f"Gateway responded {response.status_code}",
            )
        data = response.json()
        return Charge(
            reference=data["reference"],
            amount_cents=data.get("amount_cents", amount_cents),
            successful=data.get("status") == "charged",
            reason=data.get("reason", ""),
        )

    def refund(self, reference: str) -> bool:
        response = requests.post(
            f"{self.base_url}/charges/{reference}/refund",
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=self.timeout,
        )
        return response.status_code < HTTP_BAD_REQUEST


class FakePaymentGateway:
    def __init__(self, *, approve: bool = True, decline_reason: str = "Card declined") -> None:
        self.approve = approve
        self.decline_reason = decline_reason
        self.charges: list[Charge] = []
        self.refunds: list[str] = []
        self._references = count(1)

    def charge(self, member: Member, amount_cents: int, concept: str) -> Charge:
        del member, concept
        if not self.approve:
            declined = Charge(
                reference="",
                amount_cents=amount_cents,
                successful=False,
                reason=self.decline_reason,
            )
            self.charges.append(declined)
            return declined
        charge = Charge(
            reference=f"chg_{next(self._references):06d}",
            amount_cents=amount_cents,
            successful=True,
        )
        self.charges.append(charge)
        return charge

    def refund(self, reference: str) -> bool:
        self.refunds.append(reference)
        return True


class HttpxPaymentGateway:
    def __init__(
        self, base_url: str, api_key: str, timeout: float = DEFAULT_TIMEOUT_SECONDS
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    @property
    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    def charge(self, member: Member, amount_cents: int, concept: str) -> Charge:
        response = httpx.post(
            f"{self.base_url}/charges",
            json={"email": member.email, "amount_cents": amount_cents, "concept": concept},
            headers=self._headers,
            timeout=self.timeout,
        )
        if response.status_code >= HTTP_BAD_REQUEST:
            return Charge(
                reference="",
                amount_cents=amount_cents,
                successful=False,
                reason=f"Gateway responded {response.status_code}",
            )
        data = response.json()
        return Charge(
            reference=data["reference"],
            amount_cents=data.get("amount_cents", amount_cents),
            successful=data.get("status") == "charged",
            reason=data.get("reason", ""),
        )

    def refund(self, reference: str) -> bool:
        response = httpx.post(
            f"{self.base_url}/charges/{reference}/refund",
            headers=self._headers,
            timeout=self.timeout,
        )
        return response.status_code < HTTP_BAD_REQUEST
