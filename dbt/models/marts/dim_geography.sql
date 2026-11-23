select
    z.zip_prefix,
    z.city,
    z.state             as state_code,
    s.state_name,
    s.region,
    z.latitude,
    z.longitude,
    z.source_points
from {{ ref('int_geolocation__zip_centroids') }} as z
left join {{ ref('brazil_states') }} as s
    on z.state = s.state_code
