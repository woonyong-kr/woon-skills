#include "invoice.h"

int main() {
  const Invoice invoice("fixture", 350);
  return invoice.id() == "fixture" && invoice.amount_cents() == 350 ? 0 : 1;
}
