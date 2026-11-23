-- Avis clients. Le fichier brut contient des doublons stricts de (review_id, order_id) :
-- on garde la réponse la plus récente. Un même review_id peut couvrir plusieurs commandes
-- (achats groupés) : ce n'est pas une erreur, la clé de cette table est donc (review_id, order_id).
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
