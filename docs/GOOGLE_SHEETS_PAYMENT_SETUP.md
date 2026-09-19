# EkGuru — Google Apps Script Secure Payment Backend & Ledger Setup Guide

## 1. Overview & Architecture

**PRODUCTION PAYMENT BACKEND**: Google Apps Script Web App  
(Cloudflare Worker has been retired; Google Apps Script directly serves the payment API, talks to Razorpay, verifies payments, and manages the Google Sheets ledger).

```
GitHub Pages Frontend (ekguru.shop)
        │
        ▼ (POST ?action=create-order, POST ?action=verify-payment)
Google Apps Script Web App (https://script.google.com/macros/s/.../exec)
        │
        ├──> Razorpay Orders API (https://api.razorpay.com/v1/orders)
        ▼
Private Google Sheet (ID: 1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI)
  ├── 1. Payments        (Private transaction ledger)
  ├── 2. Customers       (Lifetime profiles & multi-currency totals)
  ├── 3. Refunds         (Webhook-synchronized refund ledger)
  ├── 4. WebhookEvents   (Idempotent event processing logs)
  └── 5. PublicSupport   (Sanitized records for opt-in supporters only)

Razorpay Gateway Webhooks:
Razorpay Gateway -> Google Apps Script Web App (?action=webhook)
                 -> HMAC-SHA256 signature verification over raw body
                 -> reconcileVerifiedPayment_() central reconciliation
                 -> Synchronizes Payments, Customers, PublicSupport, and Refunds
```

---

## 2. Google Spreadsheet Configuration

### Spreadsheet Identification
- **Spreadsheet ID**: `1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI`
- **Access Rule**: Keep this spreadsheet **PRIVATE** (restricted to authorized EkGuru administrators). Do NOT share publicly.
- **Safety Guarantee**: `apps-script/Code.gs` opens this specific ID via `SpreadsheetApp.openById(id)`. Fallback to `getActiveSpreadsheet()` is disabled, preventing accidental writes to any other sheet.

### Automated Tab Creation & Headers
The Google Apps Script automatically validates, creates, and safely repairs header rows without erasing existing transaction data:

1. **Payments Tab** (Production Transaction Ledger — 23 Columns):
   - Col 1: `Created At` (ISO timestamp of order creation)
   - Col 2: `Updated At` (ISO timestamp of latest state change)
   - Col 3: `Payment ID` (Razorpay payment ID `pay_*`, empty until payment attempt)
   - Col 4: `Order ID` (Authoritative Razorpay order ID `order_*`)
   - Col 5: `Status` (Gateway technical status: `created`, `authorized`, `captured`, `failed`, `cancelled`)
   - Col 6: `Amount` (Major currency units, e.g. `500.00`)
   - Col 7: `Currency` (ISO 4217 code, e.g. `INR`, `USD`, `EUR`, `GBP`)
   - Col 8: `International` (Boolean `true`/`false`)
   - Col 9: `Payment Method` (`card`, `upi`, `netbanking`, `wallet`)
   - Col 10: `Customer Name` (Sanitized patron name)
   - Col 11: `Customer Email` (Patron email address)
   - Col 12: `Customer Phone` (Patron phone number, if provided)
   - Col 13: `Country` (Patron country)
   - Col 14: `Support Message` (Optional contribution note)
   - Col 15: `Razorpay Fee` (Gateway processing fee, if captured)
   - Col 16: `Tax` (GST or tax on fee, if captured)
   - Col 17: `Refund Status` (`none`, `partial`, `refunded`)
   - Col 18: `Internal Reference` (`ekg_sup_*` idempotent reference)
   - Col 19: `Verified` (Cryptographic verification flag: `true`/`false`)
   - Col 20: `Sheet Sync Status` (`created`, `synced`, `failed`)
   - Col 21: `Payment Result` (High-level ledger state: `SUCCESS`, `PENDING`, `FAILED`, `AUTHORIZED`, `REFUNDED`, `CANCELLED`)
   - Col 22: `Payment Completed At` (Formatted timestamp `YYYY-MM-DD HH:MM:SS` when payment was captured; strictly blank for pending/failed/cancelled)
   - Col 23: `Failure Reason` (Descriptive error explanation when status is failed or cancelled; empty for success)

2. **PaymentSummary Tab** (Real-Time Executive Operations Dashboard):
   `Metric`, `Value`, `Notes`
   - Real-time counters: Successful Payments, Pending Payments, Failed Payments, Authorized Payments, Refunded Payments, Cancelled Payments.
   - Segregated multi-currency totals: Currency amounts are strictly maintained per-currency (e.g. `INR 1,500.00, USD 75.00, EUR 30.00`) and **never numerically summed across different currencies**.
   - Auto-updated whenever an order is created, verified, failed, refunded, or cancelled.

3. **Customers Tab**:
   `Customer ID`, `Name`, `Email`, `Phone`, `Country`, `First Payment`, `Last Payment`, `Total Payments`, `Total Supported Amount`, `Currencies Used`
   *(Note: `Total Supported Amount` preserves totals strictly per currency, e.g. `INR 500.00, USD 25.00`. Numerical cross-currency addition is prohibited)*
4. **Refunds Tab**:
   `Created At`, `Refund ID`, `Payment ID`, `Order ID`, `Amount`, `Currency`, `Status`, `Reason`
5. **WebhookEvents Tab**:
   `Received At`, `Event ID`, `Event Type`, `Payment ID`, `Order ID`, `Processed`, `Processing Result`
6. **PublicSupport Tab**:
   `Created At`, `Display Name`, `Country`, `Amount`, `Currency`, `Message`, `Public`, `Payment Date`, `Internal Reference`

### Conditional Formatting for Payment Result (Column 21)
The Google Apps Script automatically installs conditional formatting rules on column 21 (`Payment Result`):
- **`SUCCESS`**: Background `#d1fae5` (Soft Emerald), Text `#065f46` (Dark Green)
- **`PENDING`**: Background `#fef3c7` (Soft Amber), Text `#92400e` (Dark Yellow/Brown)
- **`FAILED`**: Background `#fee2e2` (Soft Rose), Text `#991b1b` (Dark Red)
- **`AUTHORIZED`**: Background `#dbeafe` (Soft Blue), Text `#1e40af` (Dark Blue)
- **`REFUNDED`**: Background `#f3e8ff` (Soft Purple), Text `#6b21a8` (Dark Purple)
- **`CANCELLED`**: Background `#f1f5f9` (Soft Slate Gray), Text `#475569` (Dark Slate)

### Non-Destructive Table Migration
When migrating existing spreadsheets with 20 columns, `apps-script/Code.gs` executes `migratePaymentsTableIfNeeded_(sheet)`:
- Detects whether `Payment Result` exists in the header row.
- Appends the 3 new columns (`Payment Result`, `Payment Completed At`, `Failure Reason`) preserving indices 0 to 19 without shifting existing column positions.
- Backfills existing rows based on their historical `status` and `verified` flags:
  - Rows with `captured` or `verified=true` $\to$ `SUCCESS`, `Payment Completed At` set to `Updated At`.
  - Rows with `failed` $\to$ `FAILED`, `Failure Reason` set to `Payment failed`.
  - Rows with `authorized` $\to$ `AUTHORIZED`.
  - Rows with `refunded` $\to$ `REFUNDED`.
  - Rows with `created` $\to$ `PENDING`, `Payment Completed At` and `Failure Reason` left blank.
- Recalculates and populates the `PaymentSummary` tab immediately.

---

## 3. Google Apps Script Deployment

### Step 1: Open Apps Script Project
1. Open the Google Spreadsheet in your browser:
   `https://docs.google.com/spreadsheets/d/1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI/edit`
2. In the top menu, navigate to **Extensions** $\to$ **Apps Script**.

### Step 2: Paste Implementation
1. In the Apps Script code editor, delete any placeholder code in `Code.gs`.
2. Copy the entire contents of `apps-script/Code.gs` from this repository and paste it into the editor.
3. Click **Save** (disk icon or Ctrl+S / Cmd+S).

### Step 3: Configure Script Properties
1. In the left navigation bar of Apps Script, click on **Project Settings** (gear icon).
2. Scroll to the **Script Properties** section and click **Edit script properties** $\to$ **Add script property**.
3. Add the following properties:
   - **Property**: `RAZORPAY_MODE`
   - **Value**: `TEST` (switch to `LIVE` only after end-to-end testing)
   - **Property**: `RAZORPAY_KEY_ID`
   - **Value**: Your Razorpay Key ID (e.g. `rzp_test_...` or `rzp_live_...`)
   - **Property**: `RAZORPAY_KEY_SECRET`
   - **Value**: Your private Razorpay Key Secret
   - **Property**: `RAZORPAY_WEBHOOK_SECRET`
   - **Value**: Your Razorpay Webhook Secret configured in the Razorpay Dashboard
   - (Optional) **Property**: `SPREADSHEET_ID`
   - **Value**: `1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI`
4. Click **Save script properties**.

*Note: No separate `SHEETS_INGEST_TOKEN` is needed because Google Apps Script directly accesses the private spreadsheet internally.*

### Step 4: Deploy as Web App
1. In the top right corner, click **Deploy** $\to$ **Manage deployments** (or **New deployment**).
2. If updating an existing deployment: Click edit (pencil icon), set version to **New version**, and click **Deploy**.
3. Configuration:
   - **Execute as**: `Me (your Google account)`
   - **Who has access**: `Anyone` *(Note: Public actions are strictly restricted to create-order, verify-payment, webhook, and recent-support; sheet access is completely guarded server-side)*
4. Copy the Web App URL:
   `https://script.google.com/macros/s/AKfycbz8u_rBr2o4VPgmQgaweswLWKdYb-MMGrsa7WfckTCruLP-ZEasWnpkqJrZHux5Y8_4zA/exec`

---

## 4. Controlled Public Operations

The Web App exposes only safe, controlled operations:

| Method | Action | Description | Public / Private |
|---|---|---|---|
| `POST` / `GET` (JSONP) | `?action=create-order` | Server-side Razorpay order creation via UrlFetchApp. Validates currency & amounts. Returns order_id & key_id. | Public input -> Safe checkout metadata |
| `POST` / `GET` (JSONP) | `?action=verify-payment` | Server-side HMAC-SHA256 payment verification against Razorpay secret. Calls central reconciler. | Public input -> Payment success/failure |
| `POST` | `?action=webhook` | Gateway webhook handling. Verifies HMAC over raw body before updating payments/refunds. | Razorpay Gateway -> Ledger update |
| `GET` (JSON / JSONP) | `?action=recent-support` | Retrieves latest 10 sanitized opted-in supporters. Cached via CacheService. | Public read |
| `GET` (JSON / JSONP) | `?action=health` | Service health, mode, and security booleans. | Public read |
| `GET` (JSON / JSONP) | `?action=diagnostics` | Safe deployment diagnostics and sheet connectivity check. | Public read |
| `GET` (JSON / JSONP) | `?action=currencies` | Returns all 128 verified supported currencies with exponents. | Public read |

*Note on Browser Cross-Origin Resilience:*
Browser requests to Google Apps Script Web App (`/exec`) undergo an HTTP 302 redirect from `script.google.com` to `script.googleusercontent.com`. Google does not emit CORS headers on the 302 redirect response, which blocks standard cross-origin `fetch()` in many browsers. To provide 100% resilience without freezing the UI, both `create-order` and `verify-payment` support JSONP callbacks (`callback=...`) served with `ContentService.MimeType.JAVASCRIPT`. Script tags follow 302 redirects natively in all browsers without CORS restrictions.

---

## 5. Single Payment Reconciler (`reconcileVerifiedPayment_`)

All payment state mutations flow through `reconcileVerifiedPayment_()`:
- Reconciles both `verify-payment` (browser callback) and `webhook` (`payment.captured`, `order.paid`).
- Idempotency guarantees that duplicate webhooks or dual execution do NOT double-count customer payments.
- Recovers full patron details and opt-in intent from server-side order context cache.
- Updates `Customers` tab per-currency totals strictly once per verified transaction.
- Updates `PublicSupport` tab strictly once only when `publicDisplayOptIn === true`.
