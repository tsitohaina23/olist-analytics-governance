-- Un point par préfixe de code postal : médiane des coordonnées, en excluant les points
-- situés hors du Brésil (erreurs de saisie identifiées dans le rapport de qualité).
with in_brazil as (
    select *
    from {{ ref('stg_olist__geolocation') }}
    where latitude between -33.8 and 5.3
      and longitude between -74.0 and -34.7
)

select
    zip_prefix,
    median(latitude)    as latitude,
    median(longitude)   as longitude,
    mode(city)          as city,
    mode(state)         as state,
    count(*)            as source_points
from in_brazil
group by zip_prefix
