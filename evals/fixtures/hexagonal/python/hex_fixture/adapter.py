from dataclasses import dataclass
from typing import Protocol

from hex_fixture.application import PaymentReceipt, PaymentRequest


@dataclass(frozen=True)
class VendorCharge:
    provider_id: str


class VendorClient(Protocol):
    def charge(self, amount: int, request_key: str) -> VendorCharge: ...


class VendorPaymentAdapter:
    def __init__(self, client: VendorClient) -> None:
        self._client = client

    def authorize(self, request: PaymentRequest) -> PaymentReceipt:
        charge = self._client.charge(request.amount_minor, request.idempotency_key)
        return PaymentReceipt(charge.provider_id)
