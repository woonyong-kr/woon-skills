package fixture.application;

public record PaymentRequest(String orderId, long amountMinor, String idempotencyKey) {}
