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

1. **Payments Tab**:
   `Created At`, `Updated At`, `Payment ID`, `Order ID`, `Status`, `Amount`, `Currency`, `International`, `Payment Method`, `Customer Name`, `Customer Email`, `Customer Phone`, `Country`, `Support Message`, `Razorpay Fee`, `Tax`, `Refund Status`, `Internal Reference`, `Verified`, `Sheet Sync Status`
2. **Customers Tab**:
   `Customer ID`, `Name`, `Email`, `Phone`, `Country`, `First Payment`, `Last Payment`, `Total Payments`, `Total Supported Amount`, `Currencies Used`
   *(Note: `Total Supported Amount` preserves totals strictly per currency, e.g. `INR 500.00, USD 25.00`. Numerical cross-currency addition is prohibited)*
3. **Refunds Tab**:
   `Created At`, `Refund ID`, `Payment ID`, `Order ID`, `Amount`, `Currency`, `Status`, `Reason`
4. **WebhookEvents Tab**:
   `Received At`, `Event ID`, `Event Type`, `Payment ID`, `Order ID`, `Processed`, `Processing Result`
5. **PublicSupport Tab**:
   `Created At`, `Display Name`, `Country`, `Amount`, `Currency`, `Message`, `Public`, `Payment Date`, `Internal Reference`

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
