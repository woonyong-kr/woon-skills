#ifndef WOON_LANGUAGE_FIXTURE_INVOICE_H_
#define WOON_LANGUAGE_FIXTURE_INVOICE_H_

#include <stdbool.h>
#include <stddef.h>

bool invoice_total_cents(
    const int *amounts_cents,
    size_t amount_count,
    int *total_cents);

#endif
