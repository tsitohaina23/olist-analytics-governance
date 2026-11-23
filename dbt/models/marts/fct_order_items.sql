-- Table de faits au grain de l'article : sert aux analyses par catégorie, vendeur et région.
select
    i.order_id,
    i.order_item_id,
    i.product_id,
    i.seller_id,
    o.customer_unique_id,
    o.order_status,
    o.purchase_date,
    o.customer_state,
    o.customer_region,
    sl.seller_state,
    p.category,
    i.price,
    i.freight_value,
    o.is_delivered,
    o.in_analysis_window
from {{ ref('stg_olist__order_items') }} as i
join {{ ref('fct_orders') }} as o on i.order_id = o.order_id
left join {{ ref('dim_products') }} as p on i.product_id = p.product_id
left join {{ ref('dim_sellers') }} as sl on i.seller_id = sl.seller_id
