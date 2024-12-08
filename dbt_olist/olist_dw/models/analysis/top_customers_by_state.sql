select 
    customer_state,
    customer_segment,
    count(*) as customer_count,
    avg(total_spent) as avg_customer_value
from {{ ref('customer_360') }}
group by 1, 2
order by 3 desc