select
    lpad(cast(geolocation_zip_code_prefix as varchar), 5, '0')   as zip_prefix,
    cast(geolocation_lat as double)                              as latitude,
    cast(geolocation_lng as double)                              as longitude,
    lower(trim(geolocation_city))                                as city,
    upper(trim(geolocation_state))                               as state
from {{ source('olist_raw', 'olist_geolocation_dataset') }}
