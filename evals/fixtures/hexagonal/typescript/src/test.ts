import { VendorPaymentAdapter, type VendorClient } from "./adapter";
import { CreateOrder } from "./application";

function assertEqual(actual: unknown, expected: unknown): void {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`Expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

async function main(): Promise<void> {
  const calls: Array<readonly [number, string]> = [];
  const client: VendorClient = {
    async charge(amount, requestKey) {
      calls.push([amount, requestKey]);
      return { providerId: "payment-1" };
    },
  };

  const receipt = await new CreateOrder(new VendorPaymentAdapter(client)).execute(
    "order-1",
    1500,
  );

  assertEqual(receipt, { paymentId: "payment-1" });
  assertEqual(calls, [[1500, "create-order:order-1"]]);
}

void main();
