-- Q9 (complément). Quels sont les jours records, comparés à la moyenne de leur mois ?
with daily as (
    select purchase_date, count(*) as orders
    from marts.fct_orders
    where in_analysis_window
    group by purchase_date
)

select
    purchase_date,
    dayname(purchase_date)                                                              as day_name,
    orders,
    round(avg(orders) over (partition by date_trunc('month', purchase_date)), 1)        as month_daily_average,
    round(orders / avg(orders) over (partition by date_trunc('month', purchase_date)), 1) as ratio_to_month_average
from daily
qualify rank() over (order by orders desc) <= 5
order by orders desc
