-- Une ligne par personne (customer_unique_id). La localisation retenue est celle de la
-- commande la plus récente ; les indicateurs de valeur ne comptent que les commandes livrées.
with orders as (
    select
        c.customer_unique_id,
        c.customer_zip_prefix,
        c.customer_city,
        c.customer_state,
        o.order_id,
        o.purchased_at,
        o.order_status
    from {{ ref('stg_olist__orders') }} as o
    join {{ ref('stg_olist__customers') }} as c using (customer_id)
),

delivered_value as (
    select o.customer_unique_id, sum(i.items_value + i.freight_value) as lifetime_value
    from orders as o
    join {{ ref('int_orders__items') }} as i using (order_id)
    where o.order_status = 'delivered'
    group by o.customer_unique_id
)

select
    o.customer_unique_id,
    arg_max(o.customer_zip_prefix, o.purchased_at)                         as zip_prefix,
    arg_max(o.customer_city, o.purchased_at)                               as city,
    arg_max(o.customer_state, o.purchased_at)                              as state_code,
    min(o.purchased_at)                                                    as first_order_at,
    max(o.purchased_at)                                                    as last_order_at,
    cast(date_trunc('month', min(o.purchased_at)) as date)                 as cohort_month,
    count(*)                                                               as orders_count,
    count(*) filter (where o.order_status = 'delivered')                   as delivered_orders_count,
    coalesce(any_value(v.lifetime_value), 0)                               as lifetime_value,
    count(*) filter (where o.order_status = 'delivered') > 1               as is_repeat_customer
from orders as o
left join delivered_value as v using (customer_unique_id)
group by o.customer_unique_id
