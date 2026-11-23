# Médias du projet

Déposer ici les captures et la vidéo de démonstration, référencées dans le README.

| Fichier attendu | Contenu |
| --- | --- |
| `apercu-rapport.png` | Haut du rapport interactif (`docs/report/index.html`) : titre et 4 KPI |
| `lignage-dbt.png` | Graphe de lignage de la documentation dbt (bouton en bas à droite, sur `fct_orders`) |
| `qualite.png` | Tableau des scores de qualité (bas du rapport) |
| `demo.mp4` | Vidéo de 20 à 30 s, sans son, en 1280×720, de moins de 10 Mo |

Scénario conseillé pour la vidéo (20 s) :
1. Terminal : `python scripts/pipeline.py --skip-download`, montrer « 95 tests » et « PASS » (5 s).
2. Rapport interactif : défiler sur Q1, puis survoler le graphique Q6 (retard → note) (8 s).
3. Documentation dbt : ouvrir `fct_orders`, montrer les colonnes et leur propriétaire, puis le graphe de lignage (7 s).
