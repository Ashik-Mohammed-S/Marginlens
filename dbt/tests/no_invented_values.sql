select * from {{ ref('fct_sales') }}
where (unit_cost_cents is null and profit_cents is not null)
   or (contract_matches<>1 and shortfall_cents is not null)
   or (event_type='RETURN' and shortfall_cents is not null)
