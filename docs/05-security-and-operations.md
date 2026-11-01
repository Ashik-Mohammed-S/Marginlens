# Security and operations runbook

## Implemented controls

- Synthetic records only; no employer, customer, or patient data.
- Static, read-only deployment; no data upload or credential entry.
- HTML escaping for record strings; no eval or remote JavaScript in the browser.
- CSV cells beginning with formula-like text are escaped on export.
- Browser Content Security Policy restricts script and connection sources to self, blocks objects and form submissions. Styles permit inline chart widths and Google Fonts; those font hosts are the only external visual dependency.
- No secrets in source; release check searches for common token/private-key formats. This lightweight check is not a comprehensive secret scanner.
- GitHub Actions runs tests, dbt parity checks, release checks, and pip-audit. Dependabot requests dependency updates monthly.
- The Sites audience is owner-private by default. Local preview binds to 127.0.0.1. The UI does not implement regional authorization.

The _headers file supplies additional desired headers on hosts supporting that convention; do not assume a host honors it without inspecting response headers. The HTML CSP applies independently of that file. This project is not a security certification or penetration test.

## Rebuild / refresh

1. Run `python src/pipeline.py` from the repository root.
2. Run the Python, dbt, dashboard, and release checks in README.md.
3. Compare source fingerprint and reconciliation. Warnings from seeded defects are expected; any FAIL blocks release.
4. Review the change and commit source and the validation fingerprint; regenerate the snapshot for deployment.
5. Package site/ with the Sites workflow and deploy an owner-private version.
6. Confirm the deployment returns success. Open performance, exceptions, forecast, and data trust.

This release is a fixed historical snapshot, not a continuously refreshed service. Scheduling, live alert delivery, and client-source credentials are not configured.

## Failure handling

- Build or test failure: do not replace the live version. Review the failing assertion and quarantine report.
- Missing snapshot / page loading error: verify data.json is packaged beside index.html; compare its fingerprint to the release.
- Unexpected margin: check missing_cost_rows first, then signed returns and duplicate contract candidates.
- Forecast deterioration on client data: compare with baseline, inspect input freshness and drift, and seek model review before promotion.

## Rollback

Redeploy the last successful saved Sites version (same audience), or revert the Git commit and rebuild/redeploy. Retain version IDs and commit hashes in the release record. Never overwrite a failing release's evidence. Validate snapshot load and four core views after rollback. Rollback is documented; a live rollback drill has not been performed for the first release.

## Client adoption gate

Define real source ownership, retention, licensing, tenant identity, least-privilege roles, server-side access, audit logging, refresh SLA, and monitoring ownership before adding confidential records. A public GitHub repository is not an approved store for confidential data.
