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
Google Apps Script Web App (POST ?action=create-order)
   │  (Validates 128 currencies, amount bounds, sanitizes metadata)
   ▼
Razorpay Orders API (Server-to-Server via UrlFetchApp)
   │
   ▼
Razorpay Standard Checkout (Client Modal)
   │  (Pre-filled customer info, card/UPI/international payment processing)
   ▼
Google Apps Script Verification (POST ?action=verify-payment)
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
| Property Name | Purpose | Scope |
|---|---|---|
| `RAZORPAY_KEY_ID` | Public Key ID (`rzp_live_...` or `rzp_test_...`) | Apps Script Script Property |
| `RAZORPAY_KEY_SECRET` | Private API Secret | Apps Script Script Property (Secret) |
| `RAZORPAY_WEBHOOK_SECRET` | Webhook HMAC verification secret | Apps Script Script Property (Secret) |
| `SPREADSHEET_ID` | Target Google Spreadsheet ID (`1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI`) | Apps Script Script Property |

*Note: No `SHEETS_INGEST_TOKEN` is needed because Apps Script executes inside the Google environment with direct access to the Spreadsheet.*

---

## 6. Operational Testing & Verification

1. Verify endpoint health:
   ```bash
   curl -i "https://script.google.com/macros/s/AKfycbz8u_rBr2o4VPgmQgaweswLWKdYb-MMGrsa7WfckTCruLP-ZEasWnpkqJrZHux5Y8_4zA/exec?action=health"
   ```
2. Verify supported currencies:
   ```bash
   curl -i "https://script.google.com/macros/s/AKfycbz8u_rBr2o4VPgmQgaweswLWKdYb-MMGrsa7WfckTCruLP-ZEasWnpkqJrZHux5Y8_4zA/exec?action=currencies"
   ```
3. Verify sanitized recent supporters:
   ```bash
   curl -i "https://script.google.com/macros/s/AKfycbz8u_rBr2o4VPgmQgaweswLWKdYb-MMGrsa7WfckTCruLP-ZEasWnpkqJrZHux5Y8_4zA/exec?action=recent-support"
   ```
4. Run repository automated test suite:
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
