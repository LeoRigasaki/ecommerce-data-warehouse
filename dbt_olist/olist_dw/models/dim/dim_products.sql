with stg_products as (
    select * from {{ ref('stg_products') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['product_id']) }} as product_key,
    *,
    current_timestamp as created_at
from stg_products