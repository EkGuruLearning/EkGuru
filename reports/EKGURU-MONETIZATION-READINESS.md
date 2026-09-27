# EkGuru monetization readiness

Recorded: 2026-09-27T16:12:54Z
Start SHA: `f22ed8bf5e2d4d038648405453c227697b2d11d1`

## What is true now

- `ads.txt` contains exactly `google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0`.
- AdSense runtime is **off**. `ADS_RUNTIME_ENABLED` is false. The ad policy test found 0 pages authorized to load the loader.
- The local privacy banner is not a Google-certified CMP. Advertising consent cannot be granted by that banner.
- No affiliate identifier is active.
- Optional support payments go to Razorpay's hosted page. They do not buy a lesson.
- Tutor profiles list tutor-stated prices. A booking form sends an enquiry. It is not a confirmed payment and not a published commission.

## What this is not

This is not AdSense approval. Publisher ID presence, ads.txt, and a content library are readiness factors. Google decides approval.

## Owner actions still required

- Associate the site in the AdSense account and complete identity, address and tax there.
- Install a Google-certified CMP with IAB TCF before any personalised ads for EEA/UK/CH.
- Confirm that `support@ekguru.shop` receives mail. The form delivers to `EkGuruLearning@gmail.com`, which is the inbox the code monitors.
- Merge this branch to `main` so GitHub Pages serves the roster gate. Until then production can still inject Sheet-only tutors.
