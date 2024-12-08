with source as (
    select * from {{ ref('olist_sellers_dataset') }}
)

select
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
from source