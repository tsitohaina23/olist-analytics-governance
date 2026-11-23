-- Q5. Où les livraisons sont-elles les plus lentes et les plus souvent en retard ?
-- Commandes livrées de la fenêtre d'analyse ; États avec au moins 300 commandes.
select
    customer_state,
    customer_region,
    count(*)                                                          as delivered_orders,
    round(avg(delivery_days), 1)                                      as avg_delivery_days,
    round(median(delivery_days), 1)                                   as median_delivery_days,
    round(100.0 * count(*) filter (where is_late) / count(*), 1)      as late_rate_pct,
    round(avg(delay_days) filter (where is_late), 1)                  as avg_delay_when_late_days
from marts.fct_orders
where in_analysis_window
  and is_delivered
group by customer_state, customer_region
having count(*) >= 300
order by late_rate_pct desc
