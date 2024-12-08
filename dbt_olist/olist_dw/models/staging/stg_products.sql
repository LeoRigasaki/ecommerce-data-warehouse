with source as (
    select * from {{ ref('olist_products_dataset') }}
),

translations as (
    select * from {{ ref('product_category_name_translation') }}
)

select
    p.product_id,
    p.product_category_name,
    t.product_category_name_english,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm
from source p
left join translations t 
    on p.product_category_name = t.product_category_name