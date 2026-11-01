DROP VIEW IF EXISTS daily_finance;
CREATE VIEW daily_finance AS
SELECT date, region, category, product_id, product,
       SUM(revenue_cents) revenue_cents,
       SUM(CASE WHEN cogs_cents IS NOT NULL THEN revenue_cents ELSE 0 END) covered_revenue_cents,
       SUM(COALESCE(cogs_cents,0)) known_cogs_cents,
       SUM(COALESCE(profit_cents,0)) known_profit_cents,
       SUM(CASE WHEN cogs_cents IS NULL THEN 1 ELSE 0 END) missing_cost_rows,
       COUNT(*) line_count,
       SUM(CASE WHEN event_type='SALE' THEN quantity ELSE 0 END) sale_units,
       SUM(CASE WHEN event_type='RETURN' THEN -quantity ELSE 0 END) return_units,
       SUM(CASE WHEN event_type='SALE' THEN revenue_cents ELSE 0 END) sale_revenue_cents,
       SUM(CASE WHEN event_type='SALE' THEN COALESCE(cogs_cents,0) ELSE 0 END) sale_known_cogs_cents,
       SUM(COALESCE(shortfall_cents,0)) potential_shortfall_cents,
       SUM(CASE WHEN contract_matches=1 THEN 1 ELSE 0 END) matched_rows
FROM mart_sales
GROUP BY date,region,category,product_id,product;
