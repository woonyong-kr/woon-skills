import type {
  PaymentAuthorizer,
  PaymentReceipt,
  PaymentRequest,
} from "./application";

export type VendorCharge = Readonly<{ providerId: string }>;

export interface VendorClient {
  charge(amount: number, requestKey: string): Promise<VendorCharge>;
}

export class VendorPaymentAdapter implements PaymentAuthorizer {
  constructor(private readonly client: VendorClient) {}

  async authorize(request: PaymentRequest): Promise<PaymentReceipt> {
    const charge = await this.client.charge(
      request.amountMinor,
      request.idempotencyKey,
    );
    return { paymentId: charge.providerId };
  }
}
