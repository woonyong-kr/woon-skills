package fixture;

import fixture.adapter.VendorPaymentAdapter;
import fixture.application.CreateOrder;
import fixture.application.PaymentReceipt;
import java.util.ArrayList;
import java.util.List;

public final class HexagonalFixtureTest {
    public static void main(String[] args) {
        var calls = new ArrayList<String>();
        VendorPaymentAdapter.VendorClient client = (amount, key) -> {
            calls.add(amount + ":" + key);
            return new VendorPaymentAdapter.VendorCharge("payment-1");
        };
        var useCase = new CreateOrder(new VendorPaymentAdapter(client));

        var receipt = useCase.execute("order-1", 1500);

        assert receipt.equals(new PaymentReceipt("payment-1"));
        assert calls.equals(List.of("1500:create-order:order-1"));
    }
}
