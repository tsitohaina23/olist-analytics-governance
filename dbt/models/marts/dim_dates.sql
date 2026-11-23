-- Calendrier couvrant toute la période des données.
with days as (
    select cast(unnest(generate_series(date '2016-09-01', date '2018-12-31', interval 1 day)) as date) as date_day
)

select
    date_day,
    cast(date_trunc('month', date_day) as date)     as month_start,
    year(date_day)                                  as year,
    quarter(date_day)                               as quarter,
    month(date_day)                                 as month,
    strftime(date_day, '%Y-%m')                     as year_month,
    isodow(date_day)                                as iso_day_of_week,
    dayname(date_day)                               as day_name,
    isodow(date_day) in (6, 7)                      as is_weekend,
    date_day between cast('{{ var("analysis_start") }}' as date)
                 and cast('{{ var("analysis_end") }}' as date)   as in_analysis_window
from days
