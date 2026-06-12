# Changelog

## 0.7.0 — 2026-06-12

### Added
- **Slack**: send messages to connected workspace channels, list channels, poll inbound messages (scopes `slack:read` / `slack:send`).
- **Socials**: list connected social accounts, publish posts (X, LinkedIn, Instagram, and more) with media and scheduling, check per-platform results (scopes `social:read` / `social:write`). Accounts are connected in the console (Integrations page).

## 0.6.2
Initial release as `mailgent-sdk` — the Mailgent buyer + identity SDK:
mail, vault, calendar, DID/identity, logs, and buyer-side x402 payments
(pay x402-priced URLs in USDC on Base under mandate caps). Forked from the
prior loomal SDK; seller/paywall functionality is not part of this package.
