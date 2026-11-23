-- Traduction officielle complétée par le référentiel de corrections (seed documenté).
select product_category_name, product_category_name_english, 'officielle' as translation_source
from {{ source('olist_raw', 'product_category_name_translation') }}

union all

select product_category_name, product_category_name_english, 'correction' as translation_source
from {{ ref('category_translation_fixes') }}
