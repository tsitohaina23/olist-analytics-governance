-- Q10. Comment les clients paient-ils, et le moyen de paiement change-t-il le panier ?
select
    main_payment_type,
    count(*)                                                              as orders,
    round(100.0 * count(*) / sum(count(*)) over (), 1)                    as orders_share_pct,
    round(100.0 * sum(order_value) / sum(sum(order_value)) over (), 1)    as revenue_share_pct,
    round(avg(order_value), 2)                                            as average_order_value,
    round(avg(max_installments), 2)                                       as avg_installments
from marts.fct_orders
where in_analysis_window
  and order_status not in ('canceled', 'unavailable')
  and main_payment_type is not null
group by main_payment_type
order by orders desc
