-- Table de faits au grain de la commande. Contrat de données appliqué (voir _marts.yml) :
-- les noms et types de colonnes sont garantis aux utilisateurs (tableaux de bord, analyses).
with orders as (
    select * from {{ ref('stg_olist__orders') }}
)

select
    cast(o.order_id as varchar)                                       as order_id,
    cast(o.customer_id as varchar)                                    as customer_id,
    cast(c.customer_unique_id as varchar)                             as customer_unique_id,
    cast(o.order_status as varchar)                                   as order_status,
    o.purchased_at,
    cast(o.purchased_at as date)                                      as purchase_date,
    o.approved_at,
    o.delivered_to_carrier_at,
    o.delivered_to_customer_at,
    o.estimated_delivery_at,
    cast(c.customer_state as varchar)                                 as customer_state,
    cast(s.region as varchar)                                         as customer_region,
    cast(coalesce(i.items_count, 0) as integer)                       as items_count,
    cast(coalesce(i.sellers_count, 0) as integer)                     as sellers_count,
    cast(coalesce(i.items_value, 0) as decimal(14, 2))                as items_value,
    cast(coalesce(i.freight_value, 0) as decimal(14, 2))              as freight_value,
    cast(coalesce(i.items_value, 0) + coalesce(i.freight_value, 0)
         as decimal(14, 2))                                           as order_value,
    cast(coalesce(p.payments_value, 0) as decimal(14, 2))             as payments_value,
    cast(coalesce(p.payments_count, 0) as integer)                    as payments_count,
    cast(p.main_payment_type as varchar)                              as main_payment_type,
    cast(p.max_installments as integer)                               as max_installments,
    cast(r.review_score as integer)                                   as review_score,
    cast(coalesce(r.reviews_count, 0) as integer)                     as reviews_count,
    cast(date_diff('second', o.purchased_at, o.delivered_to_customer_at) / 86400.0
         as double)                                                   as delivery_days,
    cast(date_diff('second', o.estimated_delivery_at, o.delivered_to_customer_at) / 86400.0
         as double)                                                   as delay_days,
    o.order_status = 'delivered'
        and o.delivered_to_customer_at is not null                    as is_delivered,
    cast(o.delivered_to_customer_at as date)
        > cast(o.estimated_delivery_at as date)                       as is_late,
    cast(o.purchased_at as date)
        between cast('{{ var("analysis_start") }}' as date)
            and cast('{{ var("analysis_end") }}' as date)             as in_analysis_window
from orders as o
left join {{ ref('stg_olist__customers') }} as c on o.customer_id = c.customer_id
left join {{ ref('brazil_states') }} as s on c.customer_state = s.state_code
left join {{ ref('int_orders__items') }} as i on o.order_id = i.order_id
left join {{ ref('int_orders__payments') }} as p on o.order_id = p.order_id
left join {{ ref('int_orders__reviews') }} as r on o.order_id = r.order_id
