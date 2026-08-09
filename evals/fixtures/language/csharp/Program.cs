using System.Threading;
using System.Threading.Tasks;

using Woon.LanguageFixture;

var parser = new InvoiceParser(
    (invoiceId, cancellationToken) => Task.FromResult(invoiceId));
var result = await parser.LoadAsync("fixture", CancellationToken.None);
return result == "fixture" ? 0 : 1;
