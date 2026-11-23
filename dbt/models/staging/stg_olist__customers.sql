-- Les préfixes de code postal sont lus comme des nombres : on restaure les zéros initiaux.
select
    customer_id,
    customer_unique_id,
    lpad(cast(customer_zip_code_prefix as varchar), 5, '0')   as customer_zip_prefix,
    lower(trim(customer_city))                                as customer_city,
    upper(trim(customer_state))                               as customer_state
from {{ source('olist_raw', 'olist_customers_dataset') }}
