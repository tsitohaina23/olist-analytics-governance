-- Q2. Le panier moyen et le poids des frais de port varient-ils selon la région du client ?
select
    customer_region,
    count(*)                                                    as orders,
    round(avg(order_value), 2)                                  as average_order_value,
    round(avg(freight_value), 2)                                as average_freight,
    round(100 * sum(freight_value) / sum(order_value), 1)       as freight_share_pct,
    round(avg(items_count), 2)                                  as items_per_order
from marts.fct_orders
where in_analysis_window
  and order_status not in ('canceled', 'unavailable')
  and items_count > 0
group by customer_region
order by average_order_value desc
