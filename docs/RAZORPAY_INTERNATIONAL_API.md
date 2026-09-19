# EkGuru — Razorpay International Multi-Currency API Integration

## 1. Overview & Architecture

This document describes the secure, server-side Razorpay API integration for **Support EkGuru**, replacing the legacy link/payment-button flow with an end-to-end multi-currency payment system.

### Architectural Flow

```
[ Visitor / Supporter ]
         │
         ▼
[ EkGuru Support UI (/support/) ]
  ├── Dynamic Currency Selector (128 verified ISO currencies)
  ├── Smart Minor-Unit Decimal Formatter (0, 2, 3 decimals)
  └── Amount Input & Quick-Select Pills
         │
         │ POST /api/payments/razorpay/order
         ▼
[ Secure Backend / Serverless Function ]
  ├── Validates currency against Verified Supported-Currency Registry
  ├── Validates & converts amount into currency subunits (integer paise/cents/subunits)
  ├── Attaches unique internal audit reference (internal_id)
  ├── Creates Razorpay Order via authenticated server-side API call
  └── Returns safe checkout payload (key_id, order_id, amount, currency)
         │
         ▼
[ Browser / Razorpay Checkout Modal ]
  ├── Opens modal with key_id, order_id, amount, currency
  └── Collects payment via card, UPI, or regional international rails
         │
         │ Success Callback { razorpay_order_id, razorpay_payment_id, razorpay_signature }
         ▼
[ POST /api/payments/razorpay/verify ]
  ├── Fetches stored order by order_id
  ├── Verifies order belongs to EkGuru and matches original purpose
  ├── Verifies HMAC-SHA256 signature using RAZORPAY_KEY_SECRET
  ├── Verifies amount and currency against server record (never trusting client values)
  ├── Prevents duplicate processing (idempotency check)
  └── Updates Payment Record to "captured" & "verified"
         │
         ▼
[ UI Final State ]
  ├── Success: "Payment received. Thank you for supporting EkGuru."
  └── Failure: "Payment could not be completed. No payment was marked successful by EkGuru."

[ Razorpay Webhook Event ]
         │
         │ POST /api/payments/razorpay/webhook
         ▼
[ Webhook Handler ]
  ├── Verifies HMAC-SHA256 signature using RAZORPAY_WEBHOOK_SECRET over raw request body
  ├── Enforces idempotency via event_id
  └── Updates state (captured, authorized, failed, refunded) without secret leakage
```

---

## 2. Supported Currency Strategy & Source

Razorpay supports international card transactions for Indian businesses across **128 verified currencies**, covering:
- **0-decimal currencies (16)**: `BIF`, `CLP`, `DJF`, `GNF`, `ISK`, `JPY`, `KMF`, `KRW`, `PYG`, `RWF`, `UGX`, `VND`, `VUV`, `XAF`, `XOF`, `XPF`. (Multiplier: 1; no fractions permitted).
- **2-decimal currencies (106)**: Standard currencies including `INR`, `USD`, `EUR`, `GBP`, `AED`, `CAD`, `AUD`, `SGD`, `CNY`, `CHF`, etc. (Multiplier: 100).
- **3-decimal currencies (6)**: `BHD`, `IQD`, `JOD`, `KWD`, `OMR`, `TND`. (Multiplier: 1000; last decimal 0 as per Razorpay payment gateway guidelines).

### Source of Truth
The registry is defined in `server/currencies.js` and validated against official Razorpay documentation:
`https://razorpay.com/docs/payments/payments/international-payments/#supported-currencies`

### Policy
- Never claim "all world currencies" — only verified currencies supported by the merchant configuration are offered.
- Unsupported currencies (e.g. `XYZ`, cryptocurrencies) are strictly rejected with:
  `"Currency not available for this payment method."`
- The system **never silently converts** foreign currencies to INR in frontend display or backend order creation.

---

## 3. Environment Variables

The backend relies strictly on server-side environment variables. **No secret is ever exposed in client-side code, git, or static pages.**

| Variable Name | Purpose | Scope | Required |
|---|---|---|---|
| `RAZORPAY_KEY_ID` | Razorpay API Key ID (public key identifier, e.g. `rzp_live_...` or `rzp_test_...`) | Server / Worker | Yes |
| `RAZORPAY_KEY_SECRET` | Razorpay API Key Secret used for Basic Auth order creation & signature verification | Server / Worker (Private) | Yes |
| `RAZORPAY_WEBHOOK_SECRET` | Razorpay Webhook secret configured in Dashboard for payload verification | Server / Worker (Private) | Yes |
| `PORT` | Local server port (defaults to `3000`) | Server | No |
| `NODE_ENV` | Environment mode (`production`, `development`, `test`) | Server | No |

*Note: If replacing compromised or previously exposed live keys, regenerate the secret in the Razorpay Dashboard under Account & Settings -> API Keys.*

---

## 4. API Endpoints

### 4.1 GET `/api/payments/razorpay/currencies`
Returns all verified supported currencies with their display symbols, names, and decimal exponents.

**Response (200 OK):**
```json
{
  "success": true,
  "count": 128,
  "currencies": [
    { "code": "INR", "name": "Indian Rupee", "symbol": "₹", "exponent": 2, "popular": true },
    { "code": "USD", "name": "United States Dollar", "symbol": "$", "exponent": 2, "popular": true },
    { "code": "EUR", "name": "Euro", "symbol": "€", "exponent": 2, "popular": true },
    { "code": "JPY", "name": "Japanese Yen", "symbol": "¥", exponent: 0, "popular": true }
  ]
}
```

### 4.2 POST `/api/payments/razorpay/order`
Creates a Razorpay order from the server. Never returns secret keys.

**Request Payload:**
```json
{
  "amount": "10.00",
  "currency": "USD",
  "purpose": "ekguru_support",
  "customer_email": "supporter@example.com"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "key_id": "rzp_live_...",
  "order_id": "order_XXXXX",
  "amount": 1000,
  "currency": "USD",
  "internal_id": "ekg_sup_1726718400000_a1b2c3",
  "display_amount": 10.0,
  "notes": {
    "purpose": "ekguru_support",
    "internal_id": "ekg_sup_1726718400000_a1b2c3"
  }
}
```

### 4.3 POST `/api/payments/razorpay/verify`
Verifies checkout payment signatures server-side.

**Request Payload:**
```json
{
  "razorpay_order_id": "order_XXXXX",
  "razorpay_payment_id": "pay_YYYYY",
  "razorpay_signature": "hex_hmac_sha256_signature",
  "internal_id": "ekg_sup_1726718400000_a1b2c3"
}
```

**Verification Method:**
```javascript
const expectedSignature = crypto
  .createHmac("sha256", process.env.RAZORPAY_KEY_SECRET)
  .update(`${razorpay_order_id}|${razorpay_payment_id}`)
  .digest("hex");
```
Compared using timing-safe comparison.

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Payment received. Thank you for supporting EkGuru.",
  "internal_id": "ekg_sup_1726718400000_a1b2c3",
  "razorpay_payment_id": "pay_YYYYY",
  "currency": "USD",
  "amount_minor": 1000,
  "status": "captured"
}
```

### 4.4 POST `/api/payments/razorpay/webhook`
Receives asynchronous Razorpay lifecycle webhook notifications.

**Signature Header:** `x-razorpay-signature`

**Verification Method:**
```javascript
const expected = crypto
  .createHmac("sha256", process.env.RAZORPAY_WEBHOOK_SECRET)
  .update(rawRequestBodyString)
  .digest("hex");
```

**Supported Events:**
- `payment.captured` / `order.paid`
- `payment.authorized`
- `payment.failed`
- `refund.created` / `refund.processed` / `payment.refunded`

The handler is strictly idempotent and prevents duplicate payment updates.

---

## 5. Payment Record Model

EkGuru persists a minimal payment audit record adhering to strict data minimization:

| Field | Type | Description |
|---|---|---|
| `internal_id` | String | Unique internal EkGuru tracking reference (`ekg_sup_...`) |
| `razorpay_order_id` | String | Gateway order ID |
| `razorpay_payment_id` | String | Gateway payment ID |
| `currency` | String | ISO 3-letter currency code |
| `amount_minor` | Integer | Subunit amount (paise, cents) |
| `status` | String | `created` \| `authorized` \| `captured` \| `failed` \| `refunded` |
| `purpose` | String | Neutral label: `"ekguru_support"` |
| `customer_email` | String? | Supporter email if provided |
| `customer_name` | String? | Supporter name if provided |
| `created_at` | String | ISO 8601 creation timestamp |
| `updated_at` | String | ISO 8601 update timestamp |
| `source` | String | `checkout` \| `webhook` |
| `webhook_verified` | Boolean | Webhook signature verified |
| `verification_status` | String | `pending` \| `verified` \| `failed` |

**Security Note:** Credit card numbers, CVVs, expiry dates, banking credentials, and secret keys are **never stored**.

---

## 6. Support Purpose & Legal Clarity

All user-facing language is neutral:
- **Title:** Support EkGuru
- **Description:** "Help us keep EkGuru's learning resources accessible and continuously improving."
- **Note:** "Support EkGuru's free learning platform. Contributions directly cover server bills, lesson development, and open language resources."

**Compliance Rules:**
- Do not describe payments as "charitable donations" or "tax-deductible".
- EkGuru is not an 80G registered NGO.
- Course purchases and voluntary platform support contributions remain strictly separate.

---

## 7. Local Development & Testing

### Running the Server Locally
```bash
# Set environment variables
export RAZORPAY_KEY_ID="rzp_test_..."
export RAZORPAY_KEY_SECRET="<YOUR_KEY_SECRET>"
export RAZORPAY_WEBHOOK_SECRET="<YOUR_WEBHOOK_SECRET>"

# Start the combined static + API dev server
npm start
# or: node server/server.js
```
The server will listen at `http://0.0.0.0:3000`. Open `http://localhost:3000/support/` in your browser.

### Running Automated Test Gates
```bash
npm test
```
Runs:
1. `tools/test-razorpay-api.mjs` (20 API and security gates)
2. `tools/test-browser-qa.mjs` (Responsive viewports at 320, 360, 390, 430, 768, 1024, 1440px)

---

## 8. Production Deployment

### Static Frontend (GitHub Pages / CDN)
- The static HTML (`support/index.html`), CSS (`css/support-razorpay.css`), and JS (`js/support-razorpay.js`) are hosted on GitHub Pages or any static CDN.
- In `js/site-config.js`, configure the serverless API URL if hosted on a separate domain:
  ```javascript
  api: {
    payments: "https://payments.ekguru.shop" // or leave empty if same origin
  }
  ```

### Production Backend (Google Apps Script Web App)
The production backend runs as a Google Apps Script Web App:
- **Web App URL**: `https://script.google.com/macros/s/AKfycbz8u_rBr2o4VPgmQgaweswLWKdYb-MMGrsa7WfckTCruLP-ZEasWnpkqJrZHux5Y8_4zA/exec`
- Direct serverless order creation via `POST ?action=create-order`
- Direct HMAC verification via `POST ?action=verify-payment`
- Direct webhook processing via `POST ?action=webhook`
- Script Properties: `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_WEBHOOK_SECRET`, `SPREADSHEET_ID`
- Direct automated private Google Sheets ledger recording

### Node.js Dev Server (Local Development / Testing)
Run `node server/server.js` or `npm test` locally for automated gate verification. The local server provides a mock API compatible with both REST paths and `?action=...` query parameters.

---

## 9. Rollback Artifacts & Procedure

If rollback to link-based payment is ever required:
1. The legacy link-based support card was `#m-razorpay`.
2. A backup of the static button card:
   ```html
   <div class="m-card off" id="m-razorpay">
     <div class="m-top"><span aria-hidden="true" class="m-ic">💳</span><h2>Razorpay</h2></div>
     <p class="who">India · UPI, cards &amp; netbanking on a secure page</p>
     <div class="m-go">
       <div class="m-row">
         <a class="btn btn-primary" data-go="" href="#" rel="noopener" target="_blank">Pay with Razorpay</a>
       </div>
     </div>
   </div>
   ```
3. To restore: uncomment `#m-razorpay` in `support/index.html` and add `"razorpay"` back into `METHODS` in `js/support.js`.

---

## 10. Security Invariants (Hard Rules)

1. **NEVER** expose `RAZORPAY_KEY_SECRET` in frontend files, client-side JS, Git commits, documentation, or logs.
2. Verify all payment signatures server-side using timing-safe comparisons.
3. Verify all webhook signatures using `RAZORPAY_WEBHOOK_SECRET` over raw unparsed request bytes.
4. **NEVER** trust client-supplied amounts, currencies, or order identifiers.
5. All operations must be idempotent to prevent double-capturing or record forgery.
