-- Une commande livrée doit contenir au moins un article. Bloquant.
select order_id
from {{ ref('fct_orders') }}
where is_delivered
  and items_count = 0
