-- Avis clients. Un même review_id peut couvrir plusieurs commandes (789 avis, achats groupés) :
-- la clé de cette table est donc (review_id, order_id). La source ne contient pas de doublon strict
-- sur cette clé ; le filtre ci-dessous garantit l'unicité si un export futur en introduisait.
with source as (
    select
        review_id,
        order_id,
        cast(review_score as integer)                      as review_score,
        nullif(trim(review_comment_title), '')             as review_title,
        nullif(trim(review_comment_message), '')           as review_message,
        cast(review_creation_date as timestamp)            as review_created_at,
        cast(review_answer_timestamp as timestamp)         as review_answered_at
    from {{ source('olist_raw', 'olist_order_reviews_dataset') }}
)

select *
from source
qualify row_number() over (
    partition by review_id, order_id
    order by review_answered_at desc nulls last
) = 1
