-- Score de qualité par table : moyenne des taux de réussite de ses règles (100 = aucune anomalie).
select
    table_name,
    count(*)                                                        as checks_count,
    count(*) filter (where status = 'hors seuil')                   as checks_out_of_threshold,
    sum(failed_rows)                                                as failed_rows,
    round(100 * avg(1 - failed_rows / nullif(total_rows, 0)), 2)    as quality_score,
    arg_max(check_id, failed_pct)                                   as worst_check
from {{ ref('dq_checks') }}
group by table_name
order by quality_score
