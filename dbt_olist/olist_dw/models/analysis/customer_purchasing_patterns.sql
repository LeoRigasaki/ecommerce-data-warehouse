-- This analysis shows customer purchasing patterns across different states
-- Breaking it down into clear CTEs (Common Table Expressions) for readability
with customer_orders as (
    -- First, gather all relevant order information
    select
        c.customer_state,
        c.customer_city,
        d.year,
        d.month,
        d.is_weekend,
        p.product_category_name_english,
        f.price,
        f.freight_value,
        f.order_status
    from {{ ref('fact_orders') }} f
    join {{ ref('dim_customers') }} c on f.customer_key = c.customer_key
    join {{ ref('dim_products') }} p on f.product_key = p.product_key
    join {{ ref('dim_dates') }} d on f.purchase_date_key = d.date_key
),

customer_insights as (
    -- Calculate meaningful metrics about customer behavior
    select
        customer_state,
        product_category_name_english,
        count(*) as purchase_count,
        sum(price) as total_spent,
        avg(price) as avg_order_value,
        sum(case when is_weekend then 1 else 0 end)::float / count(*) * 100 as weekend_shopping_percentage,
        avg(freight_value) as avg_shipping_cost,
        count(distinct case when order_status = 'delivered' then 1 end)::float / count(*) * 100 as delivery_success_rate
    from customer_orders
    group by 1, 2
),

ranked_categories as (
    -- Rank product categories within each state
    select 
        customer_state,
        product_category_name_english,
        purchase_count,
        total_spent,
        avg_order_value,
        weekend_shopping_percentage,
        delivery_success_rate,
        row_number() over (partition by customer_state order by purchase_count desc) as category_rank
    from customer_insights
)

-- Final output showing top 3 categories per state with key metrics
select 
    customer_state as "State",
    product_category_name_english as "Top Category",
    purchase_count as "Number of Orders",
    round(total_spent::numeric, 2) as "Total Revenue",
    round(avg_order_value::numeric, 2) as "Average Order Value",
    round(weekend_shopping_percentage::numeric, 2) as "Weekend Shopping %",
    round(delivery_success_rate::numeric, 2) as "Delivery Success Rate %"
from ranked_categories
where category_rank <= 3
order by customer_state, category_rank