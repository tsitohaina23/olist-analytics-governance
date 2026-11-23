-- Note retenue par commande : l'avis le plus récent (règle de gestion documentée dans GOUVERNANCE.md).
select
    order_id,
    arg_max(review_score, coalesce(review_answered_at, review_created_at))  as review_score,
    count(*)                                                                as reviews_count,
    bool_or(review_message is not null)                                     as has_comment
from {{ ref('stg_olist__reviews') }}
group by order_id
