# Business and KPI contract - draft v0.1

## Users and decisions

Finance director: understand gross profit changes and prioritize investigation.
Commercial analyst: investigate pricing exceptions and prepare negotiations.
Regional manager: inspect store and category performance within authorized scope.

## Initial boundaries

Fictional general-merchandise retailer; USD; sales tax excluded; no FX, rebates, loyalty accounting, pharmacy claims, or inventory valuation in v1. Operational analytics, not an audited financial statement. Synthetic historical data demonstrates methods, not real-world predictive performance.

## Grain

- sales_lines: one posted sale or return line, identified by transaction_id + line_id. Returns reference the original sale line when available.
- products: one product per product_id in v1.
- stores: one store per store_id in v1.
- contracts: one product/store agreed-price interval, with inclusive valid_from and exclusive valid_to. Overlapping applicable intervals are invalid.
- dates: one calendar date.
- cost records: one product cost interval, also non-overlapping. Matched cost is captured on the analytical transaction.

Contract and cost joins must return at most one match per sales line. Missing matches remain visible as exceptions. Preserve unmatched lines in financial totals where values are available.

## Sign conventions and measures

Use integer cents for money and positive quantity magnitudes with event_type SALE or RETURN. Signed quantity is positive for sales and negative for returns. Signed discounts are positive for sales and negative when reversing a discount on a return.

- Gross sales amount = signed quantity * unit list price.
- Net revenue = gross sales amount - signed discount amount; excludes sales tax.
- COGS = signed quantity * applicable unit cost. Returns reverse original cost where traceable.
- Gross profit = net revenue - COGS.
- Gross margin % = SUM(gross profit) / SUM(net revenue); return null and flag when aggregate net revenue <= 0. Never average line-level percentages.
- Potential price shortfall = MAX(expected contract net revenue - actual net revenue, 0) for eligible sale lines only. Expected contract net revenue = quantity * agreed net unit price. Only uniquely matched contracts and comparable pricing terms qualify.

Potential shortfall is an investigation amount, not recovered revenue or confirmed error. Authorized overrides must be separated. Returns are excluded from this v1 exception metric and analyzed separately.

If cost is missing, gross profit is unknown for that line. Report cost coverage; do not treat missing cost as zero or silently show partial margin as complete. Unmatched contracts are a coverage issue, not zero shortfall.

## Acceptance criteria

1. Exact reconciliation in integer cents on complete synthetic fixtures.
2. Duplicate keys, overlapping intervals, missing costs, orphan returns, and late arrivals are surfaced.
3. Each exception has source identifiers, reason, relevant dates, and evidence.
4. Dashboard measures agree with SQL reference queries.
5. Forecast assessment uses historical cutoffs and compares against a baseline; improvement is not assumed.

## Open decisions

- Final synthetic dataset size and date range.
- Attribution method for price-volume-mix-cost decomposition.
- Materiality thresholds and review workflow.
- Hosting destination and Power BI service availability.
