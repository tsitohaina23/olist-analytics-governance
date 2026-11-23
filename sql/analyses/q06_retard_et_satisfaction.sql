-- Q6. Quel est l'impact d'un retard de livraison sur la note donnée par le client ?
with delivered as (
    select
        review_score,
        case
            when not is_late                   then '0. À l''heure ou en avance'
            when ceil(delay_days) <= 3         then '1. Retard de 1 à 3 jours'
            when ceil(delay_days) <= 7         then '2. Retard de 4 à 7 jours'
            when ceil(delay_days) <= 14        then '3. Retard de 8 à 14 jours'
            else                                    '4. Retard de plus de 14 jours'
        end as delay_bucket
    from marts.fct_orders
    where in_analysis_window
      and is_delivered
      and review_score is not null
)

select
    delay_bucket,
    count(*)                                                                   as orders,
    round(100.0 * count(*) / sum(count(*)) over (), 1)                         as orders_share_pct,
    round(avg(review_score), 2)                                                as avg_review_score,
    round(100.0 * count(*) filter (where review_score <= 2) / count(*), 1)     as negative_reviews_pct,
    round(100.0 * count(*) filter (where review_score = 5) / count(*), 1)      as five_star_pct
from delivered
group by delay_bucket
order by delay_bucket
