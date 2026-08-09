package fixture.application;

public interface PaymentAuthorizer {
    PaymentReceipt authorize(PaymentRequest request);
}
