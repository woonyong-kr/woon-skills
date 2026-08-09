from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class PaymentRequest:
    order_id: str
    amount_minor: int
    idempotency_key: str


@dataclass(frozen=True)
class PaymentReceipt:
    payment_id: str


class PaymentAuthorizer(Protocol):
    def authorize(self, request: PaymentRequest) -> PaymentReceipt: ...


class CreateOrder:
    def __init__(self, payments: PaymentAuthorizer) -> None:
        self._payments = payments

    def execute(self, order_id: str, amount_minor: int) -> PaymentReceipt:
        return self._payments.authorize(
            PaymentRequest(order_id, amount_minor, f"create-order:{order_id}")
        )
