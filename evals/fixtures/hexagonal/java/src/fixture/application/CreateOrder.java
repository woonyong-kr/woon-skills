package fixture.application;

public final class CreateOrder {
    private final PaymentAuthorizer payments;

    public CreateOrder(PaymentAuthorizer payments) {
        this.payments = payments;
    }

    public PaymentReceipt execute(String orderId, long amountMinor) {
        return payments.authorize(
                new PaymentRequest(orderId, amountMinor, "create-order:" + orderId));
    }
}
