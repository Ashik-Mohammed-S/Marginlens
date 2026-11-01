with eligible as (
  select s.* from {{ ref('stg_sales') }} s
  inner join {{ ref('dim_stores') }} d using(store_id)
  inner join {{ ref('dim_products') }} p using(product_id)
  where occurrence=1
), matches as (
  select s.transaction_id,s.line_id,count(c.contract_id) contract_matches,
         case when count(c.contract_id)=1 then max(c.agreed_cents) end agreed_cents
  from eligible s left join {{ ref('stg_contracts') }} c
    on s.store_id=c.store_id and s.product_id=c.product_id
    and s.date>=c.valid_from and s.date<c.valid_to
  group by 1,2
), valued as (
  select s.*,m.contract_matches,m.agreed_cents,
         quantity*list_cents-discount_cents revenue_cents,
         quantity*unit_cost_cents cogs_cents
  from eligible s inner join matches m using(transaction_id,line_id)
)
select *,revenue_cents-cogs_cents profit_cents,
       case when event_type='SALE' and contract_matches=1 and authorized_override=0
            then greatest(0,quantity*agreed_cents-revenue_cents) end shortfall_cents
from valued
