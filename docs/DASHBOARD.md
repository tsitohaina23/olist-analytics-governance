# Publier un tableau de bord gratuit

Les fichiers de [`exports/`](../exports) sont prêts à brancher dans un outil de BI. Ils sont agrégés par jour, par État et par catégorie :
aucune donnée client individuelle n'y figure (voir [GOUVERNANCE.md](../GOUVERNANCE.md), § 3).

| Fichier | Grain | Usage |
| --- | --- | --- |
| `ventes_quotidiennes.csv` | jour × État × moyen de paiement | KPI, évolution, carte par État |
| `ventes_categories_mensuelles.csv` | mois × catégorie × région | Classement des catégories |
| `livraisons_par_etat.csv` | État | Délais et taux de retard |
| `qualite_regles.csv` | règle de qualité | Page « qualité des données » |

## Option 1 : Looker Studio (gratuit, lien public)

1. Ouvrir <https://lookerstudio.google.com>, puis **Créer → Source de données → Importation de fichiers**, et importer
   `ventes_quotidiennes.csv` (répéter pour les autres fichiers). Autre possibilité : importer les CSV dans Google Sheets
   puis utiliser le connecteur Google Sheets.
2. Vérifier les types : `purchase_date` en **Date**, `revenue_brl` en **Devise (BRL)**, `customer_state` en
   **Géo → Subdivision de pays (niveau 1)**.
3. Créer un **champ calculé** « Panier moyen » = `SUM(revenue_brl) / SUM(orders)` et « Taux de retard » =
   `SUM(late_orders) / SUM(delivered_orders)`. Mêmes définitions que le glossaire.
4. Page 1 « Ventes » : 4 cartes de score (chiffre d'affaires, commandes, panier moyen, taux de retard), une série
   temporelle mensuelle, une carte géographique par État, un filtre de dates et un filtre de région.
5. Page 2 « Catégories » : barres horizontales du top 10 (`ventes_categories_mensuelles.csv`).
6. Page 3 « Qualité » : tableau de `qualite_regles.csv`, avec une mise en forme conditionnelle sur `status`.
7. **Partager → Gérer l'accès → Toute personne disposant du lien peut consulter**, puis copier le lien dans le
   README et dans le portfolio.

## Option 2 : Power BI Desktop

1. **Obtenir les données → Texte/CSV** pour chaque fichier ; relier `ventes_quotidiennes[customer_state]` à
   `livraisons_par_etat[customer_state]`.
2. Mesures DAX, mêmes définitions que le glossaire :
   ```DAX
   Chiffre d'affaires = SUM(ventes_quotidiennes[revenue_brl])
   Commandes = SUM(ventes_quotidiennes[orders])
   Panier moyen = DIVIDE([Chiffre d'affaires], [Commandes])
   Taux de retard = DIVIDE(SUM(ventes_quotidiennes[late_orders]), SUM(ventes_quotidiennes[delivered_orders]))
   ```
3. La publication publique (« Publier sur le web ») demande un compte Power BI professionnel. Sans ce compte,
   exporter le rapport en PDF et le joindre au dépôt (`docs/media/`), ou utiliser Looker Studio pour le lien public.
