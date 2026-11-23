-- Q4. Les clients reviennent-ils acheter ? Rétention mensuelle par cohorte de première commande.
-- Cohortes de janv. 2017 à févr. 2018 : chacune a au moins 6 mois de recul dans la fenêtre d'analyse.
with activity as (
    select distinct
        customer_unique_id,
        cast(date_trunc('month', purchase_date) as date)  as active_month
    from marts.fct_orders
    where order_status not in ('canceled', 'unavailable')
      and purchase_date <= date '2018-08-31'
),

cohort_activity as (
    select
        c.cohort_month,
        a.customer_unique_id,
        date_diff('month', c.cohort_month, a.active_month)  as month_number
    from activity as a
    join marts.dim_customers as c using (customer_unique_id)
),

cohort_size as (
    select cohort_month, count(distinct customer_unique_id) as customers
    from cohort_activity
    where month_number = 0
    group by cohort_month
)

select
    s.cohort_month,
    s.customers                                                                                     as cohort_size,
    round(100.0 * count(distinct case when a.month_number = 1 then a.customer_unique_id end) / s.customers, 2) as m1_pct,
    round(100.0 * count(distinct case when a.month_number = 2 then a.customer_unique_id end) / s.customers, 2) as m2_pct,
    round(100.0 * count(distinct case when a.month_number = 3 then a.customer_unique_id end) / s.customers, 2) as m3_pct,
    round(100.0 * count(distinct case when a.month_number = 4 then a.customer_unique_id end) / s.customers, 2) as m4_pct,
    round(100.0 * count(distinct case when a.month_number = 5 then a.customer_unique_id end) / s.customers, 2) as m5_pct,
    round(100.0 * count(distinct case when a.month_number = 6 then a.customer_unique_id end) / s.customers, 2) as m6_pct,
    round(100.0 * count(distinct case when a.month_number between 1 and 6 then a.customer_unique_id end) / s.customers, 2) as returned_within_6m_pct
from cohort_size as s
join cohort_activity as a using (cohort_month)
where s.cohort_month between date '2017-01-01' and date '2018-02-01'
group by s.cohort_month, s.customers
order by s.cohort_month
