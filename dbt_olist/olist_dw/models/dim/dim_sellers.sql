-- models/dim/dim_sellers.sql
with stg_sellers as (
    select * from {{ ref('stg_sellers') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['seller_id']) }} as seller_key,
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state,
    current_timestamp as created_at
from stg_sellers