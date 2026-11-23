-- Q3. Quelles catégories génèrent le plus de chiffre d'affaires, et quelle part cumulent-elles ?
-- Chiffre d'affaires produit = somme des prix (hors frais de port).
with by_category as (
    select
        category,
        sum(price)                  as revenue,
        count(*)                    as items_sold,
        count(distinct order_id)    as orders
    from marts.fct_order_items
    where in_analysis_window
      and order_status not in ('canceled', 'unavailable')
    group by category
)

select
    rank() over (order by revenue desc)                                      as revenue_rank,
    category,
    round(revenue, 2)                                                        as revenue_brl,
    items_sold,
    orders,
    round(revenue / items_sold, 2)                                           as average_item_price,
    round(100 * revenue / sum(revenue) over (), 2)                           as revenue_share_pct,
    round(100 * sum(revenue) over (order by revenue desc rows unbounded preceding)
              / sum(revenue) over (), 2)                                     as cumulative_share_pct,
    count(*) over ()                                                         as categories_total
from by_category
qualify revenue_rank <= 10
order by revenue_rank
