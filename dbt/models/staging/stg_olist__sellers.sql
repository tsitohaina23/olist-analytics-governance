select
    seller_id,
    lpad(cast(seller_zip_code_prefix as varchar), 5, '0')   as seller_zip_prefix,
    lower(trim(seller_city))                                as seller_city,
    upper(trim(seller_state))                               as seller_state
from {{ source('olist_raw', 'olist_sellers_dataset') }}
