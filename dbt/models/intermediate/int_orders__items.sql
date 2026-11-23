-- Agrégats des articles par commande.
select
    order_id,
    count(*)                        as items_count,
    count(distinct product_id)      as products_count,
    count(distinct seller_id)       as sellers_count,
    sum(price)                      as items_value,
    sum(freight_value)              as freight_value
from {{ ref('stg_olist__order_items') }}
group by order_id
