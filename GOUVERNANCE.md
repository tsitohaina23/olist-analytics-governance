# Gouvernance des données

Ce document décrit comment les données de ce projet sont possédées, classées, définies, contrôlées et modifiées.
Il s'appuie sur le référentiel **DAMA-DMBOK**. Chaque règle est appliquée par du code : les métadonnées
`meta` des fichiers dbt, les tests et les modèles de qualité.

## 1. Périmètre

| Couche | Rôle | Garantie |
| --- | --- | --- |
| `olist_raw` (sources) | CSV publiés par Olist, lus tels quels | Intégrité vérifiée (nombre de lignes) par `scripts/download_data.py` |
| `staging` | Typage, renommage, nettoyage minimal | **Aucune ligne supprimée** : les anomalies sont mesurées, pas masquées |
| `intermediate` | Agrégats techniques par commande, géolocalisation consolidée | Clés uniques testées |
| `marts` | Modèle en étoile **certifié** pour l'analyse | Tests bloquants, contrat de données sur `fct_orders`, propriétaire désigné |
| `quality` | Mesure des règles de qualité | Exécuté à chaque construction |
| `reference` | Référentiels maintenus à la main (seeds) | Revue obligatoire, chaque correction est justifiée |

**Règle d'usage :** les analyses, exports et tableaux de bord ne lisent **que** la couche `marts`. Un test automatique le vérifie (`tests/test_project.py`).

## 2. Rôles et responsabilités

| Rôle | Responsabilités | Dans ce projet |
| --- | --- | --- |
| **Propriétaire des données** (data owner) | Décide des usages, valide les définitions métier | Direction commerciale (ventes), direction financière (paiements) |
| **Data steward** (par domaine) | Tient le glossaire, traite les anomalies hors seuil, valide les corrections de référentiels | Ventes, finance, clients, expérience client, catalogue produits, référentiels : voir `meta.steward` de chaque modèle |
| **Responsable qualité des données** | Fixe les seuils, suit les scores, déclenche les revues | Propriétaire des modèles `quality.*` |
| **Équipe data** (dépositaire) | Construit et exploite le pipeline, documente, teste | Auteur du dépôt |

Matrice RACI des opérations courantes :

| Opération | Owner | Steward | Qualité | Équipe data |
| --- | --- | --- | --- | --- |
| Modifier la définition d'un KPI | **A** | R | I | C |
| Corriger un référentiel (seed) | I | **A/R** | C | C |
| Ajuster un seuil de qualité | C | C | **A/R** | I |
| Modifier `fct_orders` (contrat) | **A** | C | C | R |
| Ajouter une règle de qualité | I | C | **A** | R |

## 3. Classification et données personnelles

Chaque modèle porte un niveau `meta.sensitivity` (et certaines colonnes aussi) :

| Niveau | Signification | Exemples |
| --- | --- | --- |
| `public` | Diffusable sans restriction | `dim_products`, `brazil_states`, `dim_dates` |
| `internal` | Usage interne, agrégats publiables | `fct_orders`, `dim_sellers`, `quality.*` |
| `pii` | Données à caractère personnel ou quasi-identifiants | `customer_unique_id` (pseudonymisé), préfixe postal et ville du client |
| `free_text` | Texte libre saisi par le client, pouvant contenir des données personnelles | `review_title`, `review_message` |

Règles appliquées :
- **Pas de publication sous le niveau de l'État** pour les données clients : les exports (`exports/`) et le rapport sont agrégés par État ou par région.
- **Les textes libres des avis ne sortent jamais du pipeline** : ils ne sont ni exportés ni affichés.
- L'identifiant `customer_unique_id` est déjà pseudonymisé par Olist ; il n'est jamais croisé avec une autre source.
- Les données étant brésiliennes, le cadre légal applicable serait la **LGPD** (Lei Geral de Proteção de Dados, loi n° 13.709/2018). Le jeu de données public a été anonymisé par Olist.

## 4. Glossaire métier

Les définitions font foi pour tous les livrables. Elles sont aussi publiées en **RDF/SKOS**, lisible par machine, dans [`governance/glossaire.ttl`](governance/glossaire.ttl), avec pour chaque terme la colonne qui le calcule.

| Terme | Définition | Calcul |
| --- | --- | --- |
| Chiffre d'affaires (GMV) | Montant des articles + frais de port des commandes non annulées et non indisponibles | `sum(fct_orders.order_value)` |
| Chiffre d'affaires produits | Montant des articles, hors frais de port | `sum(fct_order_items.price)` |
| Panier moyen | Chiffre d'affaires / nombre de commandes | `avg(fct_orders.order_value)` |
| Commande livrée | Statut `delivered` **et** date de livraison connue | `fct_orders.is_delivered` |
| Délai de livraison | Jours entre l'achat et la livraison au client | `fct_orders.delivery_days` |
| Commande en retard | Livrée après la date promise (au jour près) | `fct_orders.is_late` |
| Taux de retard | Commandes en retard / commandes livrées | `count(is_late) / count(is_delivered)` |
| Note client retenue | Note de l'avis **le plus récent** de la commande | `fct_orders.review_score` |
| Client | Une personne (`customer_unique_id`), et non un identifiant de commande | `dim_customers` |
| Client récurrent | Client avec au moins deux commandes livrées | `dim_customers.is_repeat_customer` |
| Cohorte | Mois de la première commande du client | `dim_customers.cohort_month` |
| Rétention M+k | Part d'une cohorte qui commande à nouveau k mois après son premier achat | `sql/analyses/q04_retention_cohortes.sql` |
| Fenêtre d'analyse | Janvier 2017 à août 2018 (mois complets uniquement) | `var('analysis_start')`, `var('analysis_end')` |

## 5. Règles de gestion

| Règle | Justification | Où |
| --- | --- | --- |
| Les commandes `canceled` et `unavailable` sont exclues du chiffre d'affaires | Aucune vente réalisée | analyses `q01`, `q02`, `q03`, `q08`, `q10` |
| Fenêtre d'analyse limitée à janv. 2017 – août 2018 | 2016 et sept.-oct. 2018 contiennent des mois incomplets (4 à 324 commandes) | `dbt_project.yml` |
| Un avis peut couvrir plusieurs commandes ; si une commande a plusieurs avis, le plus récent fait foi | 789 avis partagés et 547 commandes multi-avis constatés | `stg_olist__reviews`, `int_orders__reviews` |
| Produit sans catégorie → `unknown` (visible, pas supprimé) | 610 produits concernés | `dim_products` |
| Catégories sans traduction officielle → référentiel de corrections justifié | 2 catégories manquantes | seed `category_translation_fixes` |
| Géolocalisation : un point médian par préfixe postal, hors coordonnées en dehors du Brésil | 1 000 163 points pour environ 19 000 préfixes, dont 42 hors du pays | `int_geolocation__zip_centroids` |
| Préfixes postaux complétés à 5 chiffres | Zéros initiaux perdus à la lecture en nombre | modèles `stg_*` |

## 6. Politique de qualité

- **20 règles**, chacune rattachée à une dimension DAMA (complétude, unicité, validité, cohérence, conformité, exactitude), sont mesurées **à chaque exécution** dans `quality.dq_checks`.
- Chaque règle a un **seuil toléré** (en % de la population). Au-delà, elle passe « hors seuil » et le data steward du domaine doit l'analyser.
- Le **score par table** (`quality.dq_table_scores`) est la moyenne des taux de réussite des règles. Il sert d'indicateur de suivi.
- **Sévérité des tests dbt :**
  - *bloquant* (`error`) : clés primaires, intégrité référentielle des marts, rapprochement des totaux, contrat de données ;
  - *alerte* (`warn`) : anomalies connues de la source, avec un seuil de blocage explicite (par exemple, écart paiements / montant : alerte dès 1 commande, blocage au-delà de 1 000, soit environ 1 %).
- Rapport détaillé et actions recommandées à la source : [`reports/QUALITE.md`](reports/QUALITE.md).

## 7. Gestion des changements

1. Toute modification passe par une branche et une revue.
2. `dbt build` doit passer : tests bloquants verts, **contrat de `fct_orders` respecté**.
3. Les **expositions** dbt (`_marts.yml`) listent les livrables qui dépendent de chaque table. Le graphe de lignage montre l'impact d'un changement avant de le faire.
4. Une modification de définition métier met à jour, en même temps, ce document, le glossaire SKOS et la description dbt de la colonne.

## 8. Documentation et lignage

- **Dictionnaire de données et lignage :** documentation dbt générée ([`docs/dbt-docs/index.html`](docs/dbt-docs/index.html)). Chaque table et chaque colonne y est décrite, avec son propriétaire, son data steward et sa sensibilité.
- **Lignage simplifié :** voir le schéma du [README](README.md#architecture).
