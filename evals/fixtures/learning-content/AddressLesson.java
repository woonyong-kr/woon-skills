public class AddressLesson {
    private static final class MutableAddress {
        private String city;

        private MutableAddress(String city) {
            this.city = city;
        }

        private void moveTo(String city) {
            this.city = city;
        }
    }

    private static final class Address {
        private final String city;

        private Address(String city) {
            this.city = city;
        }

        private Address moveTo(String city) {
            return new Address(city);
        }
    }

    public static void main(String[] args) {
        MutableAddress sharedAddress = new MutableAddress("서울");
        MutableAddress memberA = sharedAddress;
        MutableAddress memberB = sharedAddress;
        memberB.moveTo("부산");
        System.out.println(
                "문제: memberA=" + memberA.city + ", memberB=" + memberB.city);

        Address addressA = new Address("서울");
        Address addressB = addressA.moveTo("부산");
        System.out.println(
                "개선: memberA=" + addressA.city + ", memberB=" + addressB.city);
    }
}
