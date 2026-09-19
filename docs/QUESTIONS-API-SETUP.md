# The questions API — one learner's flag, every learner's screen

Prakash: *"practice questions mai API use karo — jo ek user ne flag ya like
kiya, wo doosre user ko bhi dikhna chahiye."*

This is that. It is one small Apps Script Web App and one small script on the
page, and it takes about five minutes to switch on. **Until you switch it on,
nothing is broken**: votes are recorded on the learner's own device, the badge
appears, and the UI says *"saved on this device; community sync is off"*.

---

## 1. What it does

| Where | What the learner sees |
|---|---|
| After answering a question | **★ Helpful** and **⚑ Flag a problem** |
| ⚑ | a menu of five reasons (wrong answer, typo, confusing wording, duplicate, not in the lesson) |
| Under the quiz | **Flagged by other learners** — the five most-flagged questions in this bank, with their counts |
| Offline | the vote is kept, queued and shown; it is sent when the network returns |

A flag is **a signal for you to review**, never an automatic delete. Nothing
is removed from a bank by a vote.

---

## 2. Five minutes of setup

1. Make a Google Sheet (any name, e.g. *EkGuru questions*). Copy its id from
   the URL — the long string between `/d/` and `/edit`.
2. From that sheet: **Extensions → Apps Script**. This gives you the separate
   project the API needs (it must NOT share a project with the mail relay:
   two `doPost()` functions in one project is a redeclaration error, and you do
   not want a mail bug to be able to break voting).
3. Delete the sample code and paste **all of `tools/apps-script-questions.gs`**.
4. **Project Settings → Script properties → Add**:
   * `QUESTIONS_SHEET_ID` = the id you copied
   * `QUESTIONS_SALT` = any long random word (it salts the device hashes; if
     you ever change it, old votes stop matching new ones)
5. **Deploy → New deployment → Web app**:
   * Execute as: **Me**
   * Who has access: **Anyone**
   Copy the `/exec` URL it gives you.
6. Paste it into `js/site-config.js`:

   ```js
   api: {
     questions: "https://script.google.com/macros/s/AKfy…/exec"
   }
   ```

7. Open any quiz page, answer a question, press ⚑, and watch the row appear in
   the sheet's `votes` tab. Then open the same page in another browser — the
   question shows "1 learner flagged this".

Run `node tools/test-question-api.mjs` any time (32 checks, no network needed)
to prove the client and the server still agree on the contract.

---

## 3. What is stored, and what is not

One row per vote: `at`, `bank`, `question`, `action`, `reason`, `clientHash`,
`day`.

* `clientHash` is a **salted SHA-256 of a random id the browser made**. The
  sheet never holds the id itself, and the id identifies a *device*, not a
  person. It exists so one device counts once per question.
* **No names, no emails, no IP addresses, no free text.** The reason is
  checked against the five-item menu; anything else is stored empty.
* A device may cast 60 votes a day in total (`MAX_PER_DAY`), which is what
  stops the endpoint from being a free spam target if the URL leaks.
* Deleting the sheet deletes the votes. Nothing else depends on it, and the
  site keeps working (it just goes back to local-only badges).

The cookies/privacy story is on `/cookie-policy/`, and the API follows the
same rule as the rest of the site: the visitor's data goes to EkGuru's own
endpoint, not to an advertising or analytics third party.

---

## 4. Limits, honestly

* Free Apps Script quotas are real: this shape of code is comfortable for
  **hundreds of active voters a day**, not millions. If the site ever gets
  that big, the same contract moves to a real database without touching
  `js/question-api.js`.
* Counts are cached on the device for **six hours** (`TTL` in
  `js/question-api.js`); a learner's own votes always show immediately.
* A POST that fails (network, quota, deployment redeployed) stays in the queue
  and is retried on the next vote, the next load, or the next `online` event.
  It is never silently dropped.

---

## 5. The files

| File | Role |
|---|---|
| `js/question-api.js` | the client: votes, queue, cache, badges |
| `tools/apps-script-questions.gs` | the server: one row per vote, counts back |
| `tools/inject-questions-api.py` | puts the client on all 73 question pages (`--check` in the build loop) |
| `tools/test-question-api.mjs` | 32 checks — contract, offline, sync, community |
| `js/hindi-tools.js` | the quiz UI: the ⚑ and ★ row and the community block |
| `js/site-config.js` | `api.questions` — the one place the endpoint is set |
