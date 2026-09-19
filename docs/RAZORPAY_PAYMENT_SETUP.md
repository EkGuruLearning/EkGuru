# EkGuru — Razorpay Multi-Currency API & Webhook Production Setup Guide

## 1. System Overview & Final Architecture

EkGuru uses server-side Razorpay API order creation and standard checkout with real-time multi-currency support, signature verification, webhook synchronization, and an automated private Google Sheets ledger.

```
Customer
   │
   ▼
EkGuru Support UI (/support/)
   │  (Currency, Amount, Name, Email, Phone, Country, Support Message, Opt-in)
   ▼
Secure Backend Order Endpoint (POST /api/payments/razorpay/order)
   │  (Validates currency registry, amount bounds, sanitizes metadata)
   ▼
Razorpay Orders API (Server-to-Server)
   │
   ▼
Razorpay Standard Checkout (Client Modal)
   │  (Pre-filled customer info, card/UPI/international payment processing)
   ▼
Server-Side Verification (POST /api/payments/razorpay/verify)
   │  (Validates HMAC-SHA256 signature, matches internal order record)
   ▼
Razorpay Webhook (POST /api/payments/razorpay/webhook)
   │  (HMAC verification over raw body, idempotency check via event_id)
   ▼
Operational Mirror Sync (Google Apps Script -> Google Sheets)
   │  (Payments, Customers, Refunds, WebhookEvents, PublicSupport)
   ▼
Sanitized Public Support API (GET /api/support/recent)
   │  (Cached 60–300s, zero private data)
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
5. Store them strictly in backend environment variables (`RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`).
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
3. Once enabled, Razorpay allows accepting 100+ ISO 4217 currencies (USD, EUR, GBP, AED, CAD, AUD, SGD, JPY, CNY, CHF, SEK, NOK, DKK, NZD, etc.).
4. Minor-unit decimal exponents are automatically handled by the EkGuru backend engine (`server/amount-util.js` and `server/currencies.js`):
   - **Zero-decimal currencies** (e.g., JPY, KRW, VND): integer amounts without decimal fractions.
   - **Two-decimal currencies** (e.g., INR, USD, EUR, GBP): multiplied by 100 into cents/paise.
   - **Three-decimal currencies** (e.g., KWD, BHD, OMR): multiplied by 1000 into precision subunits.

---

## 4. Webhook Setup & Security

1. In the Razorpay Dashboard, go to **Account & Settings** $\to$ **Webhooks**.
2. Click **Add New Webhook**.
3. Enter the Webhook URL:
   `https://api.ekguru.shop/api/payments/razorpay/webhook`
4. Enter a strong random string (32+ alphanumeric characters) for the **Secret**.
5. Save this secret in your backend/Worker environment as `RAZORPAY_WEBHOOK_SECRET`.
6. Select the following **Active Events**:
   - `payment.authorized`
   - `payment.captured`
   - `payment.failed`
   - `order.paid`
   - `refund.created`
   - `refund.processed`
7. Click **Create Webhook**.

### Webhook Verification Rules
- The backend verifies the HMAC-SHA256 signature using `RAZORPAY_WEBHOOK_SECRET` over the **raw unparsed request body**.
- If the signature does not match `x-razorpay-signature`, the request is rejected with HTTP 400.
- All events are deduplicated by `event_id` to guarantee **idempotency**.

---

## 5. Secret Handling & Rotation

### Required Environment Variable Names (Backend Only)
| Variable Name | Purpose | Scope |
|---|---|---|
| `RAZORPAY_KEY_ID` | Public Key ID (`rzp_live_...` or `rzp_test_...`) | Backend / Worker |
| `RAZORPAY_KEY_SECRET` | Private API Secret | Backend / Worker (Secret) |
| `RAZORPAY_WEBHOOK_SECRET` | Webhook HMAC verification secret | Backend / Worker (Secret) |
| `SHEETS_INGEST_TOKEN` | Shared secret token for Google Apps Script write authentication | Backend / Worker (Secret) |
| `GOOGLE_SHEETS_ENDPOINT` | Web App `/exec` URL of the deployed Apps Script | Backend / Worker (Secret) |
| `GOOGLE_SPREADSHEET_ID` | Google Spreadsheet ID (`1u5Jkbe_...`) | Backend / Worker (Config) |

### Secret Rotation Procedure
1. If any secret is suspected of exposure:
   - In Razorpay Dashboard, generate a new Key Secret with an overlap window (e.g., 24 hours).
   - Update `RAZORPAY_KEY_SECRET` in Cloudflare Worker secrets via `wrangler secret put RAZORPAY_KEY_SECRET`.
   - Update `SHEETS_INGEST_TOKEN` in Google Apps Script Script Properties and Worker secrets.
   - Deactivate the old keys in Razorpay Dashboard after confirming health.

---

## 6. Cloudflare Worker Deployment (`ekguru-payment-api`)

The payment API runs as a high-performance, serverless edge service on Cloudflare Workers.

### Step 1: Configure Custom Domain
1. In the Cloudflare Dashboard for `ekguru.shop`, navigate to **Workers & Pages** $\to$ **ekguru-payment-api** $\to$ **Settings** $\to$ **Domains & Routes**.
2. Add Custom Domain: `api.ekguru.shop`.
3. Cloudflare will automatically provision SSL certificates and DNS routing without interrupting GitHub Pages (`ekguru.shop`).

### Step 2: Set Worker Secrets
Run the following commands using the Cloudflare Wrangler CLI:
```bash
wrangler secret put RAZORPAY_KEY_ID
wrangler secret put RAZORPAY_KEY_SECRET
wrangler secret put RAZORPAY_WEBHOOK_SECRET
wrangler secret put SHEETS_INGEST_TOKEN
wrangler secret put GOOGLE_SHEETS_ENDPOINT
```

### Step 3: Deploy Worker
```bash
wrangler deploy
```

---

## 7. Operational Testing & Verification

1. Verify endpoint health:
   ```bash
   curl -i https://api.ekguru.shop/api/payments/health
   ```
2. Verify supported currencies:
   ```bash
   curl -i https://api.ekguru.shop/api/payments/razorpay/currencies
   ```
3. Verify sanitized recent supporters:
   ```bash
   curl -i https://api.ekguru.shop/api/support/recent
   ```
4. Run repository automated test suite:
   ```bash
   npm test
   ```

---

## 8. Rollback Strategy

If rollback to offline / static configuration is needed:
1. In `support/index.html`, the offline cards (UPI, crypto) remain functional.
2. The payment form gracefully shows: `"Support options are being set up. Please check back soon."` if backend API is unreachable.
3. No customer payment data or sensitive credentials are ever held in client-side state.
