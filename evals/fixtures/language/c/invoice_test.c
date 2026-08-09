#include "invoice.h"

int main(void) {
  const int amounts[] = {100, 250};
  int total = 0;
  return invoice_total_cents(amounts, 2, &total) && total == 350 ? 0 : 1;
}
