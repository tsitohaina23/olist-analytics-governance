-- Règle de cohérence : pour une commande livrée, la somme des paiements doit égaler articles + port
-- (tolérance de 1 BRL pour les arrondis et intérêts de mensualités).
-- Politique de qualité : alerte dès la première anomalie, blocage au-delà de 1 % des commandes (≈ 1 000).
{{ config(severity='error', warn_if='>0', error_if='>1000') }}

select
    order_id,
    order_value,
    payments_value,
    payments_value - order_value as gap
from {{ ref('fct_orders') }}
where is_delivered
  and abs(payments_value - order_value) > 1
