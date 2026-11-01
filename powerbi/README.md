# Power BI handoff

The complete interactive dashboard is delivered as a hosted web app. This directory is a Power BI implementation kit, not a finished or validated PBIX file.

1. Run the pipeline; import data/daily_finance.csv as DailyFinance using UTF-8.
2. Set date to Date; all *_cents, counts, and units to Whole Number. Leave absent cost values null when importing the detailed mart.
3. Add the measures from measures.dax, one measure at a time. Format financial measures as USD and percentages appropriately.
4. Import theme.json. Add month, region, and category slicers; revenue/profit/margin/shortfall cards; daily revenue chart; category matrix; and cost coverage indicators.
5. For transaction investigation, import mart_sales.csv. Use products and stores as unique dimension tables and one-to-many relationships to the fact. Avoid connecting two fact tables directly.
6. Reconcile August 2026 all-region totals: net revenue $99,611.24; gross profit $41,914.04. October aggregate gross profit and margin must be blank because costs are missing.
7. If published to Power BI Service, configure viewer roles and test actual workspace permissions and RLS with separate accounts. A slicer is not row-level security.

Power BI Service licensing, tenant provisioning, and native PBIX authoring are outside the delivered web deployment. DAX is supplied for review and has not been executed in Power BI Desktop in this build.
