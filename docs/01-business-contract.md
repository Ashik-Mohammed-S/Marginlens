# Business and KPI contract - release 1.0

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
- date: a calendar date on each source line and daily mart row; a separate date dimension is not required by the delivered web app.
- costs: captured as a nullable unit cost on each source transaction. Generated returns carry the original sale cost. A separate cost-history table is not implemented in this release.

Contract joins must return at most one matched price per sales line. Missing/ambiguous contract matches and missing captured costs remain visible as exceptions. Preserve unmatched lines in financial totals where values are available.

## Sign conventions and measures

Use integer cents for money and signed quantity with event_type SALE or RETURN. Quantity is positive for sales and negative for returns. Discounts are positive for sales and negative when reversing a discount on a return.

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
2. Duplicate keys, unknown dimensions, overlapping contracts, and missing costs/contracts are surfaced. The generated returns reference their original sale; late-arrival monitoring requires ingestion timestamps and is outside this fixed snapshot.
3. Each exception has source identifiers, reason, relevant dates, and evidence.
4. Dashboard measures agree with SQL reference queries.
5. Forecast assessment uses historical cutoffs and compares against a baseline; improvement is not assumed.

## Release decisions

- Dataset: January 2025 through October 2026; six stores and nine products; deterministic seed 20261102.
- Attribution: sequential volume, mix, price, cost, and separate returns; see docs/04-methodology.md.
- Review: surface all positive eligible price differences; no materiality cutoff, approval workflow, or writeback in the demo.
- Delivery: owner-private Sites web app. Power BI measures/theme/import guide are provided as a handoff kit; no Power BI service or PBIX is claimed.
