# EkGuru — Razorpay Multi-Currency API & Webhook Production Setup Guide

## 1. System Overview & Architecture

**PRODUCTION PAYMENT BACKEND**: Google Apps Script Web App (NOT Cloudflare Worker)

EkGuru uses server-side Razorpay API order creation and standard checkout with real-time multi-currency support, signature verification, webhook synchronization, and an automated private Google Sheets ledger running directly in Google Apps Script.

```
Customer
   │
   ▼
EkGuru Support UI (/support/)
   │  (Currency, Amount, Name, Email, Phone, Country, Support Message, Opt-in)
   ▼
Google Apps Script Web App (POST or GET/JSONP ?action=create-order)
   │  (Validates 128 currencies, amount bounds, sanitizes metadata, dual-path CORS resilience)
   ▼
Razorpay Orders API (Server-to-Server via UrlFetchApp)
   │
   ▼
Razorpay Standard Checkout (Client Modal)
   │  (Pre-filled customer info, card/UPI/international payment processing)
   ▼
Google Apps Script Verification (POST or GET/JSONP ?action=verify-payment)
   │  (Validates HMAC-SHA256 signature, records to private Google Sheet)
   ▼
Razorpay Webhook (POST ?action=webhook)
   │  (HMAC verification over raw body, idempotency check via event_id)
   ▼
Operational Mirror Sync (Direct Google Sheet write: Payments, Customers, Refunds, WebhookEvents)
   │
   ▼
Sanitized Public Support Endpoint (GET ?action=recent-support)
   │  (Cached via CacheService, zero private data)
   ▼
Recent Supporters UI
```

---

## 2. Razorpay Account Setup: Test & Live Modes

### A. Test Mode First
1. Log in to the [Razorpay Dashboard](https://dashboard.razorpay.com).
2. Toggle to **Test Mode** (switch in top navigation).
3. Navigate to **Account & Settings** $\to$ **API Keys**.
4. Generate a Test Key pair. Note the `Key ID` (starts with `rzp_test_`) and `Key Secret`.
5. Store them strictly in Google Apps Script Script Properties (`RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`).
6. Run the integration test suite (`npm test`).

### B. Live Mode Configuration
1. Complete Razorpay account KYC and activation.
2. Toggle to **Live Mode**.
3. Navigate to **Account & Settings** $\to$ **API Keys** $\to$ **Generate Key**.
4. Note the newly generated Live Key ID (starts with `rzp_live_`) and Live Key Secret.
5. **Never mix Test and Live keys in the same environment.**
6. **Never commit Live Key Secret to Git, HTML, JS, or documentation.**

---

## 3. International Multi-Currency Activation

1. In the Razorpay Dashboard, navigate to **Account & Settings** $\to$ **International Payments**.
2. Click **Request Activation** and provide required business registration/export details.
3. Once enabled, Razorpay allows accepting 128 ISO 4217 currencies (USD, EUR, GBP, AED, CAD, AUD, SGD, JPY, CNY, CHF, SEK, NOK, DKK, NZD, etc.).
4. Minor-unit decimal exponents are strictly handled by `apps-script/Code.gs` and `server/currencies.js`:
   - **Zero-decimal currencies** (16 currencies, e.g. JPY, KRW, VND, BIF, CLP, DJF, GNF, ISK, KMF, PYG, RWF, UGX, VUV, XAF, XOF, XPF): integer amounts without decimal fractions.
   - **Two-decimal currencies** (106 currencies, e.g. INR, USD, EUR, GBP, AUD, CAD, SGD): multiplied by 100 into cents/paise.
   - **Three-decimal currencies** (6 currencies: BHD, IQD, JOD, KWD, OMR, TND): multiplied by 1000 into precision subunits.

---

## 4. Webhook Setup & Security

1. In the Razorpay Dashboard, go to **Account & Settings** $\to$ **Webhooks**.
2. Click **Add New Webhook**.
3. Enter the Webhook URL:
   `https://script.google.com/macros/s/AKfycbz8u_rBr2o4VPgmQgaweswLWKdYb-MMGrsa7WfckTCruLP-ZEasWnpkqJrZHux5Y8_4zA/exec?action=webhook`
4. Enter a strong random string (32+ alphanumeric characters) for the **Secret**.
5. Save this secret in Google Apps Script Script Properties as `RAZORPAY_WEBHOOK_SECRET`.
6. Select the following **Active Events**:
   - `payment.authorized`
   - `payment.captured`
   - `payment.failed`
   - `order.paid`
   - `refund.created`
   - `refund.processed`
7. Click **Create Webhook**.

### Webhook Verification Rules
- Google Apps Script verifies the HMAC-SHA256 signature using `Utilities.computeHmacSha256Signature` over the **raw unparsed request body**.
- If the signature does not match `x-razorpay-signature`, the request is rejected with HTTP 400.
- All events are deduplicated by `event_id` in the `WebhookEvents` sheet tab to guarantee **idempotency**.

---

## 5. Secret Handling & Configuration

### Required Script Properties (Apps Script Project Settings)
| Property Name | Purpose | Scope | Allowed Values |
|---|---|---|---|
| `RAZORPAY_MODE` | Runtime environment flag | Apps Script Script Property | `TEST` or `LIVE` |
| `RAZORPAY_KEY_ID` | Public Key ID (`rzp_live_...` or `rzp_test_...`) | Apps Script Script Property | Key ID |
| `RAZORPAY_KEY_SECRET` | Private API Secret | Apps Script Script Property (Secret) | Key Secret |
| `RAZORPAY_WEBHOOK_SECRET` | Webhook HMAC verification secret | Apps Script Script Property (Secret) | Webhook Secret |
| `SPREADSHEET_ID` | Target Google Spreadsheet ID | Apps Script Script Property | `1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI` |

*Note: No `SHEETS_INGEST_TOKEN` is needed because Apps Script executes inside the Google environment with direct access to the Spreadsheet.*

---

## 6. Operational Testing & Verification

1. Verify endpoint health:
   ```bash
   curl -i "https://script.google.com/macros/s/AKfycbz8u_rBr2o4VPgmQgaweswLWKdYb-MMGrsa7WfckTCruLP-ZEasWnpkqJrZHux5Y8_4zA/exec?action=health"
   ```
2. Verify diagnostics & sheet connectivity:
   ```bash
   curl -i "https://script.google.com/macros/s/AKfycbz8u_rBr2o4VPgmQgaweswLWKdYb-MMGrsa7WfckTCruLP-ZEasWnpkqJrZHux5Y8_4zA/exec?action=diagnostics"
   ```
3. Verify supported currencies:
   ```bash
   curl -i "https://script.google.com/macros/s/AKfycbz8u_rBr2o4VPgmQgaweswLWKdYb-MMGrsa7WfckTCruLP-ZEasWnpkqJrZHux5Y8_4zA/exec?action=currencies"
   ```
4. Verify sanitized recent supporters:
   ```bash
   curl -i "https://script.google.com/macros/s/AKfycbz8u_rBr2o4VPgmQgaweswLWKdYb-MMGrsa7WfckTCruLP-ZEasWnpkqJrZHux5Y8_4zA/exec?action=recent-support"
   ```
5. Run repository automated test suite:
   ```bash
   npm test
   ```

---

## 7. Local Node Development Server (Optional)

For local offline development and test mock runs, the repository provides `server/server.js` and `server/api.js`. The local server runs on port 3000 and can be started via:
```bash
npm run server
```
The local server supports both REST paths and `?action=...` queries for unified integration testing. In production, requests go directly to the Google Apps Script Web App.

---

## 8. Production Payment Modes & Gateway Onboarding Lifecycle

While custom Razorpay API credentials and international payment approvals are undergoing onboarding review with Razorpay, the platform enforces a fail-safe dual-track architecture:

### A. Current Production Mode (`PAYMENT_MODE = "COMING_SOON"`)
- **Default State**: Defined in `js/site-config.js` (`window.PAYMENT_MODE = "COMING_SOON"`).
- **Custom Checkout API UI**: Form submit button is marked non-actionable (`disabled`, `aria-disabled="true"`) and labeled `"Coming Soon"`. Form submissions are intercepted without making backend order creation calls or displaying broken checkout modals.
- **Global Payment CTA Guard**: Automatically prevents simulated or test payments on any generic payment trigger across the website.
- **Active Hosted Razorpay Options** (the user-facing payment on `/support/`):
  1. **Official Razorpay Payment Page embed** (primary): the exact owner-supplied
     `div.razorpay-embed-btn` block pointing at
     `https://pages.razorpay.com/pl_TdvVT9QL3k7cSY/view`, with its single
     `razorpay-embed-btn-js` loader (`https://cdn.razorpay.com/static/embed_btn/bundle.js`).
     The page must contain exactly ONE embed and ONE loader — Razorpay's
     bundle self-initializes; EkGuru JS does not drive the button.
  2. **Direct Razorpay Payment Link** (fallback): `#razorpay-payment-page-link`
     → `https://rzp.io/rzp/EkGuru`, opened in a secure new tab
     (`target="_blank" rel="noopener noreferrer"`), labelled
     "Open Razorpay Payment Page".
- **Simulation isolation**: the local test-mode modal in
  `js/support-razorpay.js` is hard-blocked on production hosts
  (`isProductionHost()`), independent of mode or payload.
- **Recent Supporters Section**: Operates fully independently of the payment
  section (loaded in `init()` before the form check), fetching verified
  contributors via direct JSON or resilient JSONP fallback.

### B. Activating Full Custom API Mode (`PAYMENT_MODE = "LIVE_API"`)
Once Razorpay completes account approval:
1. Populate live `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` in Google Apps Script Script Properties.
2. In `js/site-config.js`, update the flag:
   ```javascript
   window.PAYMENT_MODE = "LIVE_API";
   ```
3. The custom multi-currency checkout form will instantly activate:
   - Button text switches to `"Support EkGuru"`.
   - Full order creation, currency decimal scaling, prefill metadata, and client-side modal checkout run through the production Apps Script backend.
   - All backend Google Sheet ledgers (`Payments`, `Customers`, `Refunds`, `WebhookEvents`, `PublicSupport`, `PaymentSummary`) will record transactions in real time.
