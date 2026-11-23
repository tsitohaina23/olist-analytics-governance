select
    p.product_id,
    p.product_category_name                                       as category_pt,
    coalesce(t.product_category_name_english,
             case when p.product_category_name is null then 'unknown' end,
             p.product_category_name)                             as category,
    coalesce(t.translation_source, 'absente')                     as category_translation_source,
    p.product_photos_qty,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm
from {{ ref('stg_olist__products') }} as p
left join {{ ref('stg_olist__category_translation') }} as t
    on p.product_category_name = t.product_category_name
