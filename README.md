# MarginLens

Retail margin and contract intelligence: an analytics engineering and data science portfolio project.

## Business question

Revenue increased, but gross margin fell. What changed, which transactions need investigation, and what should finance prioritize before contract negotiations?

## Scope

A fictional US general-merchandise retailer, USD only, synthetic data only. No employer data, patient data, real contracts, or claims of realized savings. Contract prices represent fictional agreed selling prices; this is not a pharmacy reimbursement model.

Planned outputs: validated SQL marts, Power BI dashboard, exception investigation view, volume forecast, deployed demonstration, and client presentation.

## Start here

1. Read [the business and KPI contract](docs/01-business-contract.md).
2. Track evidence in [PROGRESS.md](PROGRESS.md).

## Planned stack

Python, SQL, DuckDB, dbt, Git, Power BI Desktop. Hosting and dependencies will be selected and pinned at implementation. No runtime application exists yet.

## Working agreement

GitHub tracks project deliverables, implementation, validation, and deployment only. Each GitHub issue should have acceptance criteria and evidence; pull requests describe business behavior and validation.

## Delivery gates

- Source totals reconcile to dashboard metrics.
- Bad records are detected and reported rather than silently discarded.
- Contract joins do not multiply transactions.
- Forecasts are evaluated against a seasonal baseline on future holdouts.
- Published demonstrations use explicitly labeled synthetic data.
- Deployment access, refresh failure behavior, and recovery are verified.
