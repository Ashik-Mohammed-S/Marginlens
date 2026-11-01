select *, row_number() over(partition by transaction_id,line_id order by date) as occurrence
from read_csv('../data/sales_lines.csv', header=true, auto_detect=true)
