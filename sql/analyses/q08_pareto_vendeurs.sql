-- Q8. Le chiffre d'affaires est-il concentré sur quelques vendeurs ? (analyse de Pareto par décile)
with seller_revenue as (
    select seller_id, sum(price) as revenue
    from marts.fct_order_items
    where in_analysis_window
      and order_status not in ('canceled', 'unavailable')
    group by seller_id
),

ranked as (
    select
        seller_id,
        revenue,
        ntile(10) over (order by revenue desc)                                             as decile,
        sum(revenue) over (order by revenue desc rows unbounded preceding)
            / sum(revenue) over ()                                                         as cumulative_share
    from seller_revenue
)

select
    decile,
    count(*)                                                        as sellers,
    round(sum(revenue), 2)                                          as revenue_brl,
    round(100 * sum(revenue) / (select sum(revenue) from ranked), 2) as revenue_share_pct,
    round(100 * max(cumulative_share), 2)                           as cumulative_share_pct,
    round(median(revenue), 2)                                       as median_seller_revenue
from ranked
group by decile
order by decile
