-- Q9. À quels jours et à quelles heures les clients commandent-ils ?
select
    isodow(purchased_at)        as iso_day_of_week,
    dayname(purchased_at)       as day_name,
    hour(purchased_at)          as hour_of_day,
    count(*)                    as orders
from marts.fct_orders
where in_analysis_window
group by 1, 2, 3
order by 1, 3
