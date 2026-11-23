select
    s.seller_id,
    s.seller_zip_prefix,
    s.seller_city,
    s.seller_state,
    st.region           as seller_region,
    g.latitude,
    g.longitude
from {{ ref('stg_olist__sellers') }} as s
left join {{ ref('brazil_states') }} as st
    on s.seller_state = st.state_code
left join {{ ref('int_geolocation__zip_centroids') }} as g
    on s.seller_zip_prefix = g.zip_prefix
