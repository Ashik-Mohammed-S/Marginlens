-- Independent SQL transformation must agree with the Python reference at line level.
with reference as (select * from read_csv('../data/mart_sales.csv',header=true,auto_detect=true))
select coalesce(a.transaction_id,b.transaction_id) as transaction_id
from {{ ref('fct_sales') }} a full outer join reference b using(transaction_id,line_id)
where a.transaction_id is null or b.transaction_id is null
   or a.revenue_cents is distinct from b.revenue_cents
   or a.cogs_cents is distinct from b.cogs_cents
   or a.profit_cents is distinct from b.profit_cents
   or a.shortfall_cents is distinct from b.shortfall_cents
   or a.contract_matches is distinct from b.contract_matches
