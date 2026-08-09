export type PaymentRequest = Readonly<{
  orderId: string;
  amountMinor: number;
  idempotencyKey: string;
}>;

export type PaymentReceipt = Readonly<{ paymentId: string }>;

export interface PaymentAuthorizer {
  authorize(request: PaymentRequest): Promise<PaymentReceipt>;
}

export class CreateOrder {
  constructor(private readonly payments: PaymentAuthorizer) {}

  execute(orderId: string, amountMinor: number): Promise<PaymentReceipt> {
    return this.payments.authorize({
      orderId,
      amountMinor,
      idempotencyKey: `create-order:${orderId}`,
    });
  }
}
