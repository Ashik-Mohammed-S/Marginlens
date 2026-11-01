select transaction_id,line_id,count(*) n from {{ ref('fct_sales') }} group by 1,2 having count(*)<>1
