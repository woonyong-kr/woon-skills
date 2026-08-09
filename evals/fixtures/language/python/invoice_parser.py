from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Invoice:
    id: str
    amount_cents: int


def parse_invoice(values: Mapping[str, object] | None = None) -> Invoice:
    source = {} if values is None else values
    invoice_id = source.get("id")
    amount_cents = source.get("amount_cents")
    if not isinstance(invoice_id, str) or not isinstance(amount_cents, int):
        raise ValueError("invalid invoice")
    return Invoice(id=invoice_id, amount_cents=amount_cents)


def main() -> None:
    print(parse_invoice({"id": "fixture", "amount_cents": 100}))


if __name__ == "__main__":
    main()
