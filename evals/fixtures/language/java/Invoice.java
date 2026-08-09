import java.util.Objects;

public final class Invoice {
  private final String id;
  private final long amountCents;

  public Invoice(String id, long amountCents) {
    this.id = Objects.requireNonNull(id);
    if (amountCents < 0) {
      throw new IllegalArgumentException("amountCents must be non-negative");
    }
    this.amountCents = amountCents;
  }

  public String id() {
    return id;
  }

  public long amountCents() {
    return amountCents;
  }
}
