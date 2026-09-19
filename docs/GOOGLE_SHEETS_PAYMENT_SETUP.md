# EkGuru — Google Sheets Automated Private Payment Ledger Setup Guide

## 1. Overview & Architecture

This guide details the setup and configuration of the automated Google Sheets private payment ledger for **EkGuru Support**.

The Google Sheet acts as an operational mirror and historical reporting database. Razorpay remains the primary financial source of truth.

```
Razorpay API / Webhooks
        │
        ▼
Cloudflare Worker / Backend API
        │  (Authenticated with SHEETS_INGEST_TOKEN)
        ▼
Google Apps Script (Web App /exec)
        │
        ▼
Google Spreadsheet (ID: 1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI)
  ├── 1. Payments (Comprehensive private transaction ledger)
  ├── 2. Customers (Aggregate patron profiles & lifetime stats)
  ├── 3. Refunds (Refund synchronization from webhooks)
  ├── 4. WebhookEvents (Audit trail & event-level idempotency)
  └── 5. PublicSupport (Sanitized records for opted-in supporters only)
```

---

## 2. Google Spreadsheet Configuration

### Spreadsheet Identification
- **Spreadsheet ID**: `1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI`
- **Access Rule**: Keep this spreadsheet **PRIVATE** (restricted to authorized EkGuru administrators). Do NOT share publicly.

### Automated Tab Creation & Headers
The Google Apps Script (`apps-script/Code.gs`) automatically detects, creates, and repairs all required sheets and header columns upon deployment or first run:

1. **Payments Tab**:
   `Created At`, `Updated At`, `Payment ID`, `Order ID`, `Status`, `Amount`, `Currency`, `International`, `Payment Method`, `Customer Name`, `Customer Email`, `Customer Phone`, `Country`, `Support Message`, `Razorpay Fee`, `Tax`, `Refund Status`, `Internal Reference`, `Verified`, `Sheet Sync Status`
2. **Customers Tab**:
   `Customer ID`, `Name`, `Email`, `Phone`, `Country`, `First Payment`, `Last Payment`, `Total Payments`, `Total Supported Amount`, `Currencies Used`
3. **Refunds Tab**:
   `Created At`, `Refund ID`, `Payment ID`, `Order ID`, `Amount`, `Currency`, `Status`, `Reason`
4. **WebhookEvents Tab**:
   `Received At`, `Event ID`, `Event Type`, `Payment ID`, `Order ID`, `Processed`, `Processing Result`
5. **PublicSupport Tab**:
   `Created At`, `Display Name`, `Country`, `Amount`, `Currency`, `Message`, `Public`, `Payment Date`

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
3. Add the following property:
   - **Property**: `SHEETS_INGEST_TOKEN`
   - **Value**: A strong, cryptographically generated random string (e.g., 32+ characters).
4. (Optional) Add:
   - **Property**: `SPREADSHEET_ID`
   - **Value**: `1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI`
5. Click **Save script properties**.

### Step 4: Deploy as Web App
1. In the top right corner, click **Deploy** $\to$ **New deployment**.
2. Click the gear icon next to "Select type" and choose **Web app**.
3. Fill in the deployment details:
   - **Description**: `EkGuru Payment Ledger Webhook v1`
   - **Execute as**: `Me (your Google account)`
   - **Who has access**: `Anyone` *(Note: Write requests are authenticated via SHEETS_INGEST_TOKEN; unauthenticated requests are strictly rejected)*
4. Click **Deploy**.
5. Copy the generated **Web App URL** (ends in `/exec`).
6. Set this URL as the backend environment variable: `GOOGLE_SHEETS_ENDPOINT`.

---

## 4. Privacy & Public Support Ingest Rules

- **Default Privacy**: All payments, customer profiles, emails, and phone numbers are private.
- **Opt-In Requirement**: A supporter's record is added to the `PublicSupport` tab **only if** `publicDisplayOptIn === true`.
- **Public Query Endpoint (`doGet`)**:
  - The Web App `doGet` function responds **only** to `?action=recent-support`.
  - It returns a maximum of 10 latest sanitized records containing:
    `displayName`, `country`, `amount`, `currency`, `message`, `date`.
  - It **never** returns email, phone, payment ID, order ID, or private customer identifiers.
  - Access to `Payments`, `Customers`, `Refunds`, or `WebhookEvents` via `doGet` is strictly forbidden and returns 403.

---

## 5. Resilience & Failure Handling

- If Google Apps Script experiences a temporary timeout or service outage, **customer payments on Razorpay are NOT failed**.
- The backend records `sheet_sync_status: "failed"` and automatically enqueues the payload in its retry queue.
- Subsequent retry operations match by `internal_id` or `payment_id`, ensuring no duplicate rows are created when service resumes.
