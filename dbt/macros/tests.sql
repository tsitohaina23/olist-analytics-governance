{#- Tests génériques maison, utilisables dans les fichiers .yml. -#}

{#- Échoue sur chaque ligne où la colonne est nulle ou négative (ou nulle si strict). -#}
{% test positive_value(model, column_name, allow_zero=false) %}
select *
from {{ model }}
where {{ column_name }} is not null
  and {{ column_name }} {{ '<' if allow_zero else '<=' }} 0
{% endtest %}

{#- Échoue si la combinaison de colonnes n'est pas unique. -#}
{% test unique_combination(model, combination_of_columns) %}
select {{ combination_of_columns | join(', ') }}, count(*) as n
from {{ model }}
group by {{ combination_of_columns | join(', ') }}
having count(*) > 1
{% endtest %}

{#- Échoue si une date est postérieure à une autre date de la même ligne (ex. livraison avant achat). -#}
{% test not_before(model, column_name, reference_column) %}
select *
from {{ model }}
where {{ column_name }} is not null
  and {{ reference_column }} is not null
  and {{ column_name }} < {{ reference_column }}
{% endtest %}
