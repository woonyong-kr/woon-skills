#include "invoice.h"

#include <limits.h>

static bool add_without_overflow(int left, int right, int *sum) {
  if (right > 0 && left > INT_MAX - right) {
    return false;
  }
  if (right < 0 && left < INT_MIN - right) {
    return false;
  }
  *sum = left + right;
  return true;
}

bool invoice_total_cents(
    const int *amounts_cents,
    size_t amount_count,
    int *total_cents) {
  if (amounts_cents == NULL || total_cents == NULL) {
    return false;
  }

  int total = 0;
  for (size_t index = 0; index < amount_count; ++index) {
    if (!add_without_overflow(total, amounts_cents[index], &total)) {
      return false;
    }
  }
  *total_cents = total;
  return true;
}
