-- Règle de cohérence : le chiffre d'affaires des articles est identique au grain article
-- (fct_order_items) et au grain commande (fct_orders). Bloquant.
with by_item as (
    select sum(price) as total from {{ ref('fct_order_items') }}
),
by_order as (
    select sum(items_value) as total from {{ ref('fct_orders') }}
)
select by_item.total as total_items, by_order.total as total_orders
from by_item, by_order
where by_item.total <> by_order.total
