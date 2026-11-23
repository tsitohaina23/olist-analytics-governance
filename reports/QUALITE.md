# Rapport de qualité des données

Généré par `scripts/build_report.py` à partir des modèles dbt `quality.dq_checks` et `quality.dq_table_scores`. Politique de qualité et rôles : [GOUVERNANCE.md](../GOUVERNANCE.md).

## Score par table

| Table | Règles | Hors seuil | Lignes en échec | Score /100 | Règle la plus dégradée |
| --- | --- | --- | --- | --- | --- |
| geolocation | 2 | 1 | 280 051.0 | 86.00 | GEO-01 |
| products | 3 | 1 | 629.0 | 99.36 | PRD-01 |
| reviews | 3 | 2 | 1 361.0 | 99.54 | REV-01 |
| customers | 1 | 0 | 278.0 | 99.72 | CUS-01 |
| sellers | 1 | 0 | 7.0 | 99.77 | SEL-01 |
| orders | 6 | 1 | 1 216.0 | 99.79 | ORD-04 |
| order_items | 1 | 0 | 0.0 | 100.00 | ITM-01 |
| payments | 3 | 0 | 14.0 | 100.00 | PAY-02 |

## Détail des règles

| Règle | Table | Dimension | Description | Échecs | Population | % échec | Seuil % | Statut |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CUS-01 | customers | Conformité | Préfixe postal client absent du référentiel de géolocalisation | 278 | 99 441 | 0.280 | 0.5 | ✅ conforme |
| GEO-01 | geolocation | Unicité | Ligne en double exact (même préfixe  mêmes coordonnées) | 280 009 | 1 000 163 | 27.996 | 5 | ⚠️ hors seuil |
| GEO-02 | geolocation | Validité | Coordonnées situées hors du Brésil | 42 | 1 000 163 | 0.004 | 0.01 | ✅ conforme |
| ITM-01 | order_items | Validité | Article à prix nul ou négatif | 0 | 112 650 | 0.000 | 0 | ✅ conforme |
| ORD-01 | orders | Complétude | Commande non annulée sans date d'approbation du paiement | 19 | 98 816 | 0.019 | 0.5 | ✅ conforme |
| ORD-02 | orders | Cohérence | Statut « delivered » sans date de livraison au client | 8 | 96 478 | 0.008 | 0.1 | ✅ conforme |
| ORD-03 | orders | Validité | Remise au transporteur datée avant l'achat | 166 | 97 658 | 0.170 | 0.1 | ⚠️ hors seuil |
| ORD-04 | orders | Cohérence | Commande sans aucun article | 775 | 99 441 | 0.779 | 1 | ✅ conforme |
| ORD-05 | orders | Cohérence | Commande sans aucun paiement | 1 | 99 441 | 0.001 | 0.1 | ✅ conforme |
| ORD-06 | orders | Exactitude | Commande livrée dont les paiements diffèrent du montant articles + port de plus de 1 BRL | 247 | 96 470 | 0.256 | 1 | ✅ conforme |
| PAY-01 | payments | Validité | Moyen de paiement non défini (« not_defined ») | 3 | 103 886 | 0.003 | 0.1 | ✅ conforme |
| PAY-02 | payments | Validité | Paiement d'un montant nul | 9 | 103 886 | 0.009 | 0.1 | ✅ conforme |
| PAY-03 | payments | Validité | Paiement par carte de crédit avec 0 mensualité | 2 | 76 795 | 0.003 | 0.1 | ✅ conforme |
| PRD-01 | products | Complétude | Produit sans catégorie | 610 | 32 951 | 1.851 | 1 | ⚠️ hors seuil |
| PRD-02 | products | Conformité | Produit dont la catégorie n'a pas de traduction officielle | 13 | 32 341 | 0.040 | 0.1 | ✅ conforme |
| PRD-03 | products | Validité | Poids manquant ou égal à zéro | 6 | 32 951 | 0.018 | 0.1 | ✅ conforme |
| REV-01 | reviews | Unicité | Ligne d'avis dont le review_id est partagé par plusieurs commandes (achat groupé) | 814 | 99 224 | 0.820 | 0.5 | ⚠️ hors seuil |
| REV-02 | reviews | Unicité | Commande ayant reçu plusieurs avis | 547 | 98 673 | 0.554 | 0.5 | ⚠️ hors seuil |
| REV-03 | reviews | Validité | Note hors de l'échelle 1 à 5 | 0 | 99 224 | 0.000 | 0 | ✅ conforme |
| SEL-01 | sellers | Conformité | Préfixe postal vendeur absent du référentiel de géolocalisation | 7 | 3 095 | 0.226 | 0.5 | ✅ conforme |

## Règles hors seuil et traitement

| Règle | Traitement dans le pipeline | Action recommandée à la source |
| --- | --- | --- |
| GEO-01 — Ligne en double exact (même préfixe, mêmes coordonnées) | Agrégation en un point médian par préfixe (int_geolocation__zip_centroids) | Dédoublonner le référentiel à l'ingestion ; une ligne par préfixe et par point distinct |
| ORD-03 — Remise au transporteur datée avant l'achat | Conservé et signalé ; non utilisé pour les délais (calculés depuis l'achat) | Contrôler l'horloge et le fuseau du système transporteur |
| PRD-01 — Produit sans catégorie | Catégorie « unknown » dans dim_products, visible dans les analyses | Rendre la catégorie obligatoire à la création d'un produit |
| REV-01 — Ligne d'avis dont le review_id est partagé par plusieurs commandes (achat groupé) | Clé de la table = (review_id, order_id) : l'avis est rattaché à chaque commande concernée | Documenter ce cas dans le contrat d'interface, ou émettre un identifiant d'avis par commande |
| REV-02 — Commande ayant reçu plusieurs avis | Règle de gestion : l'avis le plus récent fait foi (int_orders__reviews) | Limiter à un avis par commande ou historiser explicitement les mises à jour |
