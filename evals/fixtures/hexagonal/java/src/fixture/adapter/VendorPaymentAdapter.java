package fixture.adapter;

import fixture.application.PaymentAuthorizer;
import fixture.application.PaymentReceipt;
import fixture.application.PaymentRequest;

public final class VendorPaymentAdapter implements PaymentAuthorizer {
    public record VendorCharge(String providerId) {}

    public interface VendorClient {
        VendorCharge charge(long amountMinor, String requestKey);
    }

    private final VendorClient client;

    public VendorPaymentAdapter(VendorClient client) {
        this.client = client;
    }

    @Override
    public PaymentReceipt authorize(PaymentRequest request) {
        var charge = client.charge(request.amountMinor(), request.idempotencyKey());
        return new PaymentReceipt(charge.providerId());
    }
}
