# Google Ad Manager Scale Plan

## Decision

Do not migrate now. AdSense is simpler for the current website. Adopt Ad Manager only when EkGuru has direct advertiser agreements, multiple demand sources, material inventory segmentation, forecasting needs, or ad-operations capacity.

## Adoption gates

All are required: stable AdSense/content-policy standing; certified CMP coverage; named ad-operations owner; documented inventory taxonomy; direct/third-party demand contract; creative review and incident process; reporting reconciliation; tested performance and accessibility budgets.

## Future inventory

Use semantic units rather than page-count farming: `guide/in_article`, `guide/rail`, and carefully reviewed `learning/between_modules`. Exclude account, admin, checkout, forms, quiz/test, speaking, answer, and accessibility-control zones. Key-values may describe page class, language and level but must not expose personal or sensitive learner data.

## Transactions and demand

Google documents traditional direct-sold Sponsorship/Standard line items and programmatic guaranteed/preferred/auction transactions. Direct agreements require delivery, creative, billing and reconciliation operations. AdSense may remain backfill only after yield and policy review. Source: https://support.google.com/admanager/answer/9248464.

## Migration

1. Design inventory and consent/data map.
2. Create a staging network and test GPT without live demand.
3. Map exclusions and safe zones exactly.
4. Validate CMP/TC strings, creatives, sizes, CLS, keyboard flow and mobile overlap.
5. Pilot one HIGH_CONTENT class with rollback.
6. Reconcile reporting before expansion.

Do not run AdSense and Ad Manager tags in uncontrolled competition. Do not copy publisher or network IDs from examples. No migration begins merely because Ad Manager exists.

## AdMob boundary

AdMob remains a separate future native-app project using the Google Mobile Ads SDK and app-specific IDs/test devices. It is not a website monetization option and is not part of this migration.
