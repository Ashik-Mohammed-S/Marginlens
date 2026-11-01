# Validation evidence

Build date: 2026-11-02 (Asia/Calcutta).

## Executed locally

- Python unittest: 9 tests passed, covering reconciliation, quarantine, unique grain, ambiguous joins, missing costs, return signs, overrides, exclusive contract end, and forecast edge cases.
- dbt/DuckDB: 5 models built and 11 data tests passed, including independent transaction-level parity and dimension relationships. See dbt-summary.json.
- Dashboard Node tests: six views render; exact SQLite totals agree; filters, missing-cost suppression, bridge reconciliation, escaping, empty results, and scenario changes pass.
- Release checks: source/mart counts and revenue agree, forecast dates/bounds are valid, model selection follows validation WAPE, CSP is present, common secret patterns absent.
- Dependency audit: no known vulnerabilities reported for resolved requirements at audit time. See dependency-audit.json; this is not a security guarantee.
- Browser: performance rendered; September bridge reconciled to $0.00; forecast/scenario controls rendered; Ambiguous contract search returned 30 records with unknown expected price and shortfall.

## Financial checkpoint

August 2026, all regions/categories: net revenue $99,611.24; gross profit $41,914.04. Compare SQL and dashboard before changing metric logic.

## Forecast evidence

Final holdout: 2026-10-04 through 2026-10-31. Weekday-trend WAPE 2.2631%; seasonal baseline WAPE 3.8324%. Empirical interval coverage 96.43%. Exact metrics: validation.json.

## Verification boundaries

Power BI DAX has not been executed in Desktop. A native PBIX, scheduled production refresh, live regional authorization, penetration test, and live rollback drill are not claimed. GitHub-hosted CI and deployed status are recorded separately once observed.
