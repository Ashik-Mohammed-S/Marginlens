# Architecture and design decisions

## Data flow

`seeded Python generator -> raw CSV -> validated Python reference -> SQLite SQL daily mart -> versioned JSON -> static web application`

An independent `raw CSV -> dbt/DuckDB -> fct_sales` branch checks every accepted transaction against the Python reference. The dashboard snapshot is published only after both branches pass validation.

## Why two calculation paths?

The Python/SQLite build runs with no third-party packages, making the demo easy to reproduce. dbt/DuckDB demonstrates dependency-aware SQL models and data tests. A full outer join parity test compares revenue, costs, profit, contract matches, and shortfall at the transaction-line grain. Neither dbt nor the browser is the source of raw data.

## Runtime boundary

The deployed app is static HTML/CSS/JavaScript with a 7 MB JSON snapshot. There is no database connection, API key, write endpoint, upload endpoint, or Python runtime in the browser. Filters operate locally. The hosted audience starts owner-private. All bundled data should nevertheless be treated as downloadable by any authorized visitor; browser filters are not authorization.

## Modeling decisions

- One sales/return row per transaction_id + line_id.
- Duplicate raw rows are quarantined after the first deterministic occurrence. The seeded duplicate is identical. A production system must define source version precedence before resolving conflicting duplicates.
- Missing dimensions are quarantined; missing costs and contracts remain in the accepted mart with flags.
- Sales use positive units and discounts; returns reverse both. Source cost is captured on the line, including original cost for generated returns.
- Agreements are product/store effective intervals with exclusive end dates.
- Contract candidates are counted before attaching prices. Zero/multiple matches never fabricate an expected amount.
- Full gross profit is unavailable when any selected line lacks a cost. Known-cost profit is explicitly labeled as partial.
- All source money is integer USD cents. Rates and bridge decompositions use floating-point arithmetic, with display rounding only.

## Tradeoffs and extensions

The data is deliberately compact, fictional, and single-currency. It lacks stockouts, causal demand elasticity, rebate accounting, pharmacy claims, and real organizational permissions. For a client pilot, replace the generator with authorized immutable extracts, adopt ingestion timestamps and source manifests, define an access matrix, test server-side or BI-service authorization, and measure finance acceptance of reviewed exceptions.

No feature store, Kubernetes, streaming infrastructure, LLM, or automatic retraining is required for this batch analytical use case.
