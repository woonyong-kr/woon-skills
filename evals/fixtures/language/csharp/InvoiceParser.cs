using System;
using System.Threading;
using System.Threading.Tasks;

namespace Woon.LanguageFixture;

public sealed class InvoiceParser {
  private readonly Func<string, CancellationToken, Task<string>> _loader;

  public InvoiceParser(Func<string, CancellationToken, Task<string>> loader) {
    _loader = loader;
  }

  public async Task<string> LoadAsync(
      string invoiceId,
      CancellationToken cancellationToken) {
    ArgumentException.ThrowIfNullOrEmpty(invoiceId);
    return await _loader(invoiceId, cancellationToken).ConfigureAwait(false);
  }
}
