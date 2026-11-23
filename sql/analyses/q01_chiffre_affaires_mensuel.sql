-- Q1. Comment évoluent le chiffre d'affaires et le nombre de commandes chaque mois ?
-- KPI « chiffre d'affaires » = order_value (articles + port) des commandes non annulées
-- et non indisponibles (définition : GOUVERNANCE.md, glossaire).
with monthly as (
    select
        cast(date_trunc('month', purchase_date) as date)   as month,
        count(*)                                           as orders,
        sum(order_value)                                   as revenue
    from marts.fct_orders
    where in_analysis_window
      and order_status not in ('canceled', 'unavailable')
    group by 1
)

select
    month,
    orders,
    round(revenue, 2)                                                   as revenue_brl,
    round(revenue / orders, 2)                                          as average_order_value,
    round(100 * (revenue / lag(revenue) over (order by month) - 1), 1)  as revenue_growth_mom_pct,
    round(sum(revenue) over (order by month), 2)                        as cumulative_revenue_brl
from monthly
order by month
