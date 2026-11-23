-- Agrégats des paiements par commande ; le moyen principal est celui du plus gros montant.
select
    order_id,
    count(*)                                              as payments_count,
    sum(payment_value)                                    as payments_value,
    arg_max(payment_type, payment_value)                  as main_payment_type,
    max(payment_installments)                             as max_installments,
    count(distinct payment_type) > 1                      as is_mixed_payment
from {{ ref('stg_olist__payments') }}
group by order_id
