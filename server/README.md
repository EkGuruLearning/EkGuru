# server/

Small Node server for payments and the order store. It is not part of the
static site; GitHub Pages does not run it.

| File | Job |
|---|---|
| `server.js` | Entry point (`npm start`) |
| `api.js` | HTTP routes |
| `razorpay-service.js`, `currencies.js`, `amount-util.js` | Razorpay orders and amount handling |
| `payment-store.js`, `sheets-client.js` | Order store and Google Sheets ledger |

Setup: `docs/RAZORPAY_PAYMENT_SETUP.md`, `docs/RAZORPAY_INTERNATIONAL_API.md`,
`docs/GOOGLE_SHEETS_PAYMENT_SETUP.md`.

## Rules

- Keys and tokens come from the environment, never from a committed file.
- Amounts are validated on the server (`amount-util.js`).
- Tests: `npm run test:payments`, `test:e2e`, `test:contract`.
