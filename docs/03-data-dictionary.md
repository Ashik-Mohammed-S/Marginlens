# Data dictionary and known defects

| Dataset | Grain | Important fields |
|---|---|---|
| stores | one store | store_id, store, region |
| products | one product | product_id, product, category, list_cents, cost_cents |
| contracts | one effective agreement | contract_id, store_id, product_id, valid_from, valid_to, agreed_cents |
| sales_lines | one source line, including injected duplicate | transaction_id, line_id, date, event_type, quantity, list_cents, discount_cents, unit_cost_cents, original_transaction_id, authorized_override |
| mart_sales | one accepted line | source fields plus revenue_cents, cogs_cents, profit_cents, contract_matches, expected_cents, shortfall_cents |
| rejected | one rejected source row | source fields and reject_reason |
| daily_finance | date / region / category / product | additive revenue, known costs/profit, missing-cost count, units, shortfall, match coverage |

`quantity` is signed. `list_cents` is a nonnegative unit price. `discount_cents` is the signed total line discount. `unit_cost_cents` is nullable. Blank CSV costs must import as null, not zero. A null shortfall means ineligible or not determinable; it is not a zero-valued estimate.

Dates cover 2025-01-01 through 2026-10-31, six stores, nine products, and three categories. Every amount is fictional. The random seed and SHA-256 source fingerprint are recorded in reports/validation.json.

## Intentional defects

1. One identical duplicate line: quarantined by natural key.
2. One line referencing S99: quarantined for an unknown store.
3. Missing October sale costs at a deterministic interval: retained with null profit.
4. S02 / P02 overlapping September contract: retained once, ambiguous expected price.
5. S06 / P09 agreement ending 2026-09-01: subsequent sales retained without a matching agreement.

## Intentional commercial scenarios

- West / Personal care: selling price decreases by $1 per unit from September 2026.
- Home essentials: unit cost increases by $0.65 from September 2026.
- Occasional price reductions; some are authorized overrides.
- Weekday seasonality, annual seasonality, modest trend, and random volume variation.

These are planted scenarios for evaluation. They must not be presented as discoveries about any real retailer.
