with customer_stats as (
    -- Get basic customer information and enrich it with insights
    select
        c.customer_key,
        c.customer_id,
        c.customer_state,
        c.customer_city,
        
        -- Shopping Behavior
        count(distinct f.order_id) as total_orders,
        sum(f.price) as total_spent,
        avg(f.price) as avg_order_value,
        
        -- Time Analysis
        min(d.date_actual) as first_purchase_date,
        max(d.date_actual) as last_purchase_date,
        
        -- Product Preferences
        array_agg(distinct p.product_category_name_english) as bought_categories,
        
        -- Calculate customer lifetime value
        sum(f.price) / nullif(
            extract(
                month from 
                age(max(d.date_actual), min(d.date_actual))
            ), 0
        ) as monthly_value,
        
        -- Shopping Patterns
        count(distinct case 
            when d.is_weekend then f.order_id 
        end) as weekend_orders,
        
        avg(f.freight_value) as avg_freight_cost

    from {{ ref('dim_customers') }} c
    left join {{ ref('fact_orders') }} f 
        on c.customer_key = f.customer_key
    left join {{ ref('dim_products') }} p 
        on f.product_key = p.product_key
    left join {{ ref('dim_dates') }} d 
        on f.purchase_date_key = d.date_key
    group by 1, 2, 3, 4
),

customer_segments as (
    -- Create customer segments based on buying behavior
    select 
        *,
        case 
            when total_orders >= 10 then 'VIP'
            when total_orders >= 5 then 'Regular'
            when total_orders >= 2 then 'Occasional'
            else 'One-time'
        end as customer_segment,
        
        case
            when avg_order_value > 500 then 'High Value'
            when avg_order_value > 100 then 'Mid Value'
            else 'Budget'
        end as value_segment,
        
        case 
            when weekend_orders::float / nullif(total_orders, 0) > 0.5 
            then 'Weekend Shopper'
            else 'Weekday Shopper'
        end as shopping_pattern
    from customer_stats
)

select * from customer_segments