with date_spine as (
   {{ dbt_utils.date_spine(
       datepart="day",
       start_date="cast('2016-01-01' as date)",
       end_date="cast('2019-01-01' as date)"
   ) }}
)

select
   {{ dbt_utils.generate_surrogate_key(['date_day']) }} as date_key,
   date_day as date_actual,
   extract(year from date_day) as year,
   extract(month from date_day) as month,
   extract(day from date_day) as day,
   extract(quarter from date_day) as quarter,
   extract(dow from date_day) + 1 as day_of_week,
   case when extract(dow from date_day) in (6,0) then true else false end as is_weekend,
   current_timestamp as created_at
from date_spine