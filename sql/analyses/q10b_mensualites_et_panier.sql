-- Q10 (complément). Pour les cartes de crédit, le nombre de mensualités augmente-t-il avec le panier ?
select
    case
        when max_installments <= 1  then '1. Comptant'
        when max_installments <= 3  then '2. 2 à 3 fois'
        when max_installments <= 6  then '3. 4 à 6 fois'
        when max_installments <= 10 then '4. 7 à 10 fois'
        else                             '5. Plus de 10 fois'
    end                                                     as installments_bucket,
    count(*)                                                as orders,
    round(100.0 * count(*) / sum(count(*)) over (), 1)      as orders_share_pct,
    round(avg(order_value), 2)                              as average_order_value,
    round(median(order_value), 2)                           as median_order_value
from marts.fct_orders
where in_analysis_window
  and order_status not in ('canceled', 'unavailable')
  and main_payment_type = 'credit_card'
group by 1
order by 1
