export interface Invoice {
  readonly id: string;
  readonly amountCents: number;
}

export type ParseResult =
  | { readonly kind: "ok"; readonly invoice: Invoice }
  | { readonly kind: "error"; readonly message: string };

export function parseInvoice(input: unknown): ParseResult {
  if (!isRecord(input) || typeof input.id !== "string") {
    return { kind: "error", message: "invalid invoice id" };
  }
  if (typeof input.amountCents !== "number") {
    return { kind: "error", message: "invalid invoice amount" };
  }
  return {
    kind: "ok",
    invoice: { id: input.id, amountCents: input.amountCents },
  };
}

function isRecord(input: unknown): input is Record<string, unknown> {
  return typeof input === "object" && input !== null;
}
