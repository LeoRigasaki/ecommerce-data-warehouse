-- models/fact/fact_orders.sql
with stg_order_items as (
   select * from {{ ref('stg_order_items') }}
),

stg_orders as (
   select * from {{ ref('stg_orders') }}
),

dim_customers as (
   select * from {{ ref('dim_customers') }}
),

dim_products as (
   select * from {{ ref('dim_products') }}
),

dim_sellers as (
   select * from {{ ref('dim_sellers') }}
),

dim_dates as (
   select * from {{ ref('dim_dates') }}
)

select
   {{ dbt_utils.generate_surrogate_key(['oi.order_id', 'oi.order_item_id']) }} as order_key,
   oi.order_id,
   c.customer_key,
   p.product_key,
   s.seller_key,
   oi.order_item_id,
   o.order_status,
   d1.date_key as purchase_date_key,
   d2.date_key as approved_date_key,
   d3.date_key as delivery_date_key,
   oi.price,
   oi.freight_value,
   current_timestamp as created_at
from stg_order_items oi
inner join stg_orders o on oi.order_id = o.order_id
left join dim_customers c on o.customer_id = c.customer_id
left join dim_products p on oi.product_id = p.product_id
left join dim_sellers s on oi.seller_id = s.seller_id
left join dim_dates d1 on date(o.order_purchase_timestamp) = d1.date_actual
left join dim_dates d2 on date(o.order_approved_at) = d2.date_actual
left join dim_dates d3 on date(o.order_delivered_customer_date) = d3.date_actual