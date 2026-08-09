#include "invoice.h"

#include <stdexcept>
#include <utility>

Invoice::Invoice(std::string id, int amount_cents)
    : id_(std::move(id)), amount_cents_(amount_cents) {
  if (amount_cents < 0) {
    throw std::invalid_argument("amount_cents must be non-negative");
  }
}

const std::string& Invoice::id() const { return id_; }

int Invoice::amount_cents() const { return amount_cents_; }
