import unittest

from hex_fixture.adapter import VendorCharge, VendorPaymentAdapter
from hex_fixture.application import CreateOrder, PaymentReceipt, PaymentRequest


class RecordingVendorClient:
    def __init__(self) -> None:
        self.calls: list[tuple[int, str]] = []

    def charge(self, amount: int, request_key: str) -> VendorCharge:
        self.calls.append((amount, request_key))
        return VendorCharge("payment-1")


class HexagonalFixtureTest(unittest.TestCase):
    def test_use_case_accepts_a_consumer_owned_fake(self) -> None:
        class FakePayments:
            def authorize(self, request: PaymentRequest) -> PaymentReceipt:
                self.request = request
                return PaymentReceipt("fake-1")

        payments = FakePayments()
        receipt = CreateOrder(payments).execute("order-1", 1500)

        self.assertEqual(receipt, PaymentReceipt("fake-1"))
        self.assertEqual(payments.request.idempotency_key, "create-order:order-1")

    def test_adapter_maps_the_internal_contract_to_the_vendor(self) -> None:
        client = RecordingVendorClient()
        adapter = VendorPaymentAdapter(client)

        receipt = adapter.authorize(PaymentRequest("order-1", 1500, "intent-1"))

        self.assertEqual(receipt, PaymentReceipt("payment-1"))
        self.assertEqual(client.calls, [(1500, "intent-1")])


if __name__ == "__main__":
    unittest.main()
