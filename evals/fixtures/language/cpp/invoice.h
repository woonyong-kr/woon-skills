#ifndef WOON_LANGUAGE_FIXTURE_CPP_INVOICE_H_
#define WOON_LANGUAGE_FIXTURE_CPP_INVOICE_H_

#include <string>

class Invoice {
 public:
  Invoice(std::string id, int amount_cents);

  const std::string& id() const;
  int amount_cents() const;

 private:
  std::string id_;
  int amount_cents_;
};

#endif
