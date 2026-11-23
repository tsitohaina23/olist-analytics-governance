-- Q7. Quelle part des clients rachète, et que pèsent-ils dans le chiffre d'affaires ?
-- Base : clients ayant au moins une commande livrée ; valeur = commandes livrées.
with customers as (
    select
        case when is_repeat_customer then 'Récurrent (2 commandes livrées ou plus)'
             else 'Unique (1 commande livrée)' end   as customer_type,
        lifetime_value,
        delivered_orders_count
    from marts.dim_customers
    where delivered_orders_count >= 1
)

select
    customer_type,
    count(*)                                                                as customers,
    round(100.0 * count(*) / sum(count(*)) over (), 2)                      as customers_share_pct,
    round(sum(lifetime_value), 2)                                           as revenue_brl,
    round(100.0 * sum(lifetime_value) / sum(sum(lifetime_value)) over (), 2) as revenue_share_pct,
    round(avg(lifetime_value), 2)                                           as avg_lifetime_value,
    round(avg(delivered_orders_count), 2)                                   as avg_delivered_orders
from customers
group by customer_type
order by customers desc
