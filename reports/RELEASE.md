# MarginLens release 1.0

Released 2026-11-02 (Asia/Calcutta).

- Live app: https://marginlens-retail-finance.swoonysnipe19.chatgpt.site
- Audience: owner-private; ChatGPT sign-in required. An unauthenticated browser reached the sign-in gate; the authenticated hosted app was not inspected in this session.
- Native deployment status: succeeded.
- Site project: appgprj_6ae7b16144508191b459e765d75b8ddd
- Deployment: appgdep_6ae7b6bc6bb481919693722deb99a49c
- Saved version: appgprj_6ae7b16144508191b459e765d75b8ddd~appgver_16d97b4d9db88191823ce5cfd3f20f36
- Site source commit: e85b54242430db1a488a439a7f564c116bffb661
- GitHub implementation commit: 513a09439db6e23bbdfcf32e712a2606d699b91c
- GitHub validation: https://github.com/Ashik-Mohammed-S/Marginlens/actions/runs/41355087992 (completed, success).

The CI run executed Python tests, independent dbt models/tests, dashboard checks, release checks, and dependency auditing. The same dashboard assets were inspected locally at desktop and compact widths. Search and financial bridge behavior were exercised in the browser.

## Delivered scope

Working web dashboard, deterministic synthetic pipeline, independent dbt/DuckDB transformations, tests, forecasts/scenarios, quality views, CSV exports, six-slide printable web presentation, documentation, and Power BI handoff kit.

## Boundaries

No native PBIX is included. No real data connector, scheduled production refresh, regional authorization, writeback, live alerts, or production incident process is configured. The first release documents rollback but does not claim a live rollback drill. These are requirements for a client pilot, not concealed capabilities of the demonstration.
