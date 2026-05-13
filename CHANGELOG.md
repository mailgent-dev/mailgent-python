# Changelog

All notable changes to `loomal-sdk` are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] — 2026-05-13

### Added
- `loomal.payments` resource on `Loomal` and `AsyncLoomal`. Methods:
  - `challenge(amount, resource=None, description=None, network="base")` —
    `POST /v0/payments/challenge`, returns the x402 402-body dict.
  - `redeem(payment_header, resource, amount, network="base",
    description=None)` — `POST /v0/payments/redeem`, verifies + settles.
  - `list(limit=None)` — `GET /v0/payments`, returns
    `{"payments": [PaymentSummary, ...], "count": int}`.
  - `get(payment_id)` — `GET /v0/payments/:id`, returns `PaymentDetail`
    with the full Ed25519-signed receipt.
- `PaymentSummary`, `PaymentDetail`, `PaymentReceipt`, `PaymentReceiptBody`,
  `PaymentEndpointSummary` dataclasses exported from `loomal`.

## [0.4.1] — 2026-05-07

### Added
- `loomal.webhook.verify_webhook(raw_body, signature, secret)` — HMAC-SHA256
  verifier matching Loomal's `X-Loomal-Signature: sha256=<hex>` header.
  Returns `bool`, accepts `str` or `bytes` body, rejects empty secret as a
  fail-closed guard. Stdlib `hmac` + `hashlib` only — no extra deps.

### Tests
- Added `tests/test_webhook.py` (7 tests) — happy path, signature mismatch,
  missing header, missing `sha256=` prefix, empty secret, bytes body,
  non-hex signature.

## [0.4.0] — 2026-05-06

### Added
- Paywall middleware for sellers, exported under `loomal.paywall`. Wrap a
  FastAPI route with `Depends(require_payment(amount=...))` and Loomal
  handles the x402 challenge → verify → settle dance against Base mainnet.
- Lower-level `build_challenge_async`, `verify_and_settle_async`,
  `PaywallConfig`, `PaywallRouteOptions` for non-FastAPI frameworks.

[0.5.0]: https://github.com/loomal-ai/loomal-python/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/loomal-ai/loomal-python/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/loomal-ai/loomal-python/releases/tag/v0.4.0
