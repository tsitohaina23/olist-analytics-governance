# Résultats des analyses

Généré par `scripts/run_analyses.py` à partir des requêtes de `sql/analyses/`.

## Q1. Comment évoluent le chiffre d'affaires et le nombre de commandes chaque mois ?

Requête : [`sql/analyses/q01_chiffre_affaires_mensuel.sql`](../sql/analyses/q01_chiffre_affaires_mensuel.sql)

| month | orders | revenue_brl | average_order_value | revenue_growth_mom_pct | cumulative_revenue_brl |
| --- | --- | --- | --- | --- | --- |
| 2017-01-01 | 787 | 136 943.46 | 174.01 | — | 136 943.46 |
| 2017-02-01 | 1 718 | 283 561.69 | 165.05 | 107.10 | 420 505.15 |
| 2017-03-01 | 2 617 | 425 617.96 | 162.64 | 50.10 | 846 123.11 |
| 2017-04-01 | 2 377 | 405 848.61 | 170.74 | -4.60 | 1 251 971.72 |
| 2017-05-01 | 3 640 | 582 710.83 | 160.09 | 43.60 | 1 834 682.55 |
| 2017-06-01 | 3 205 | 499 652.24 | 155.90 | -14.30 | 2 334 334.79 |
| 2017-07-01 | 3 946 | 578 753.73 | 146.67 | 15.80 | 2 913 088.52 |
| 2017-08-01 | 4 272 | 661 903.52 | 154.94 | 14.40 | 3 574 992.04 |
| 2017-09-01 | 4 227 | 717 102.72 | 169.65 | 8.30 | 4 292 094.76 |
| 2017-10-01 | 4 547 | 764 756.03 | 168.19 | 6.60 | 5 056 850.79 |
| 2017-11-01 | 7 423 | 1 172 191.68 | 157.91 | 53.30 | 6 229 042.47 |
| 2017-12-01 | 5 620 | 861 526.77 | 153.30 | -26.50 | 7 090 569.24 |
| 2018-01-01 | 7 187 | 1 101 920.01 | 153.32 | 27.90 | 8 192 489.25 |
| 2018-02-01 | 6 625 | 979 486.16 | 147.85 | -11.10 | 9 171 975.41 |
| 2018-03-01 | 7 168 | 1 152 656.99 | 160.81 | 17.70 | 10 324 632.40 |
| 2018-04-01 | 6 919 | 1 156 248.89 | 167.11 | 0.30 | 11 480 881.29 |
| 2018-05-01 | 6 833 | 1 145 686.46 | 167.67 | -0.90 | 12 626 567.75 |
| 2018-06-01 | 6 145 | 1 020 381.90 | 166.05 | -10.90 | 13 646 949.65 |
| 2018-07-01 | 6 233 | 1 039 783.58 | 166.82 | 1.90 | 14 686 733.23 |
| 2018-08-01 | 6 421 | 996 973.51 | 155.27 | -4.10 | 15 683 706.74 |

## Q2. Le panier moyen et le poids des frais de port varient-ils selon la région du client ?

Requête : [`sql/analyses/q02_panier_moyen_par_region.sql`](../sql/analyses/q02_panier_moyen_par_region.sql)

| customer_region | orders | average_order_value | average_freight | freight_share_pct | items_per_order |
| --- | --- | --- | --- | --- | --- |
| Norte | 1 828 | 223.32 | 41.37 | 18.50 | 1.12 |
| Nordeste | 9 272 | 201.17 | 35.92 | 17.90 | 1.11 |
| Centro-Oeste | 5 712 | 176.98 | 26.51 | 15.00 | 1.15 |
| Sul | 13 947 | 162.82 | 24.40 | 15.00 | 1.15 |
| Sudeste | 67 146 | 150.84 | 19.86 | 13.20 | 1.14 |

## Q3. Quelles catégories génèrent le plus de chiffre d'affaires, et quelle part cumulent-elles ?

Requête : [`sql/analyses/q03_top_categories.sql`](../sql/analyses/q03_top_categories.sql)

| revenue_rank | category | revenue_brl | items_sold | orders | average_item_price | revenue_share_pct | cumulative_share_pct | categories_total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | health_beauty | 1 251 145.54 | 9 585 | 8 757 | 130.53 | 9.30 | 9.30 | 74 |
| 2 | watches_gifts | 1 194 824.97 | 5 965 | 5 599 | 200.31 | 8.88 | 18.19 | 74 |
| 3 | bed_bath_table | 1 035 485.07 | 11 089 | 9 394 | 93.38 | 7.70 | 25.89 | 74 |
| 4 | sports_leisure | 977 728.77 | 8 573 | 7 656 | 114.05 | 7.27 | 33.15 | 74 |
| 5 | computers_accessories | 902 922.70 | 7 760 | 6 636 | 116.36 | 6.71 | 39.87 | 74 |
| 6 | furniture_decor | 721 584.27 | 8 229 | 6 373 | 87.69 | 5.37 | 45.23 | 74 |
| 7 | housewares | 625 538.73 | 6 903 | 5 838 | 90.62 | 4.65 | 49.88 | 74 |
| 8 | cool_stuff | 619 724.39 | 3 772 | 3 609 | 164.30 | 4.61 | 54.49 | 74 |
| 9 | auto | 585 177.48 | 4 195 | 3 863 | 139.49 | 4.35 | 58.84 | 74 |
| 10 | garden_tools | 479 650.06 | 4 323 | 3 500 | 110.95 | 3.57 | 62.41 | 74 |

## Q4. Les clients reviennent-ils acheter ? Rétention mensuelle par cohorte de première commande.

Requête : [`sql/analyses/q04_retention_cohortes.sql`](../sql/analyses/q04_retention_cohortes.sql)

| cohort_month | cohort_size | m1_pct | m2_pct | m3_pct | m4_pct | m5_pct | m6_pct | returned_within_6m_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-01-01 | 752 | 0.40 | 0.27 | 0.13 | 0.40 | 0.13 | 0.40 | 1.73 |
| 2017-02-01 | 1 690 | 0.24 | 0.30 | 0.12 | 0.41 | 0.12 | 0.24 | 1.42 |
| 2017-03-01 | 2 571 | 0.51 | 0.35 | 0.39 | 0.35 | 0.16 | 0.16 | 1.79 |
| 2017-04-01 | 2 325 | 0.60 | 0.22 | 0.17 | 0.34 | 0.26 | 0.34 | 1.89 |
| 2017-05-01 | 3 541 | 0.51 | 0.51 | 0.40 | 0.31 | 0.34 | 0.42 | 2.12 |
| 2017-06-01 | 3 101 | 0.48 | 0.35 | 0.39 | 0.26 | 0.39 | 0.39 | 2.10 |
| 2017-07-01 | 3 820 | 0.52 | 0.37 | 0.26 | 0.29 | 0.21 | 0.31 | 1.88 |
| 2017-08-01 | 4 129 | 0.70 | 0.34 | 0.27 | 0.36 | 0.53 | 0.29 | 2.30 |
| 2017-09-01 | 4 073 | 0.69 | 0.54 | 0.29 | 0.44 | 0.22 | 0.22 | 2.16 |
| 2017-10-01 | 4 390 | 0.71 | 0.25 | 0.09 | 0.23 | 0.21 | 0.21 | 1.62 |
| 2017-11-01 | 7 189 | 0.56 | 0.39 | 0.17 | 0.19 | 0.18 | 0.11 | 1.57 |
| 2017-12-01 | 5 437 | 0.26 | 0.28 | 0.35 | 0.28 | 0.20 | 0.17 | 1.51 |
| 2018-01-01 | 6 949 | 0.33 | 0.37 | 0.29 | 0.29 | 0.16 | 0.17 | 1.53 |
| 2018-02-01 | 6 356 | 0.38 | 0.39 | 0.30 | 0.27 | 0.22 | 0.20 | 1.71 |

## Q5. Où les livraisons sont-elles les plus lentes et les plus souvent en retard ?

Requête : [`sql/analyses/q05_delais_livraison_par_etat.sql`](../sql/analyses/q05_delais_livraison_par_etat.sql)

| customer_state | customer_region | delivered_orders | avg_delivery_days | median_delivery_days | late_rate_pct | avg_delay_when_late_days |
| --- | --- | --- | --- | --- | --- | --- |
| AL | Nordeste | 396 | 24.50 | 22.30 | 21.50 | 10.20 |
| MA | Nordeste | 713 | 21.50 | 19.20 | 17.50 | 11.20 |
| SE | Nordeste | 332 | 21.40 | 17.90 | 15.40 | 16.90 |
| PI | Nordeste | 475 | 19.40 | 16.30 | 13.90 | 14.10 |
| CE | Nordeste | 1 273 | 21.20 | 18.20 | 13.80 | 15.90 |
| BA | Nordeste | 3 253 | 19.30 | 16.90 | 12.20 | 12.70 |
| RJ | Sudeste | 12 310 | 15.30 | 12.00 | 12.10 | 14.20 |
| PA | Norte | 942 | 23.80 | 21.10 | 11.30 | 13.50 |
| ES | Sudeste | 1 992 | 15.80 | 13.60 | 10.70 | 12.00 |
| PB | Nordeste | 516 | 20.40 | 18.20 | 10.50 | 11.00 |
| MS | Centro-Oeste | 701 | 15.60 | 13.90 | 9.70 | 9.00 |
| PE | Nordeste | 1 587 | 18.40 | 15.70 | 9.60 | 12.70 |
| RN | Nordeste | 470 | 19.20 | 16.00 | 9.40 | 15.10 |
| SC | Sul | 3 537 | 14.90 | 13.00 | 8.20 | 9.00 |
| GO | Centro-Oeste | 1 950 | 15.60 | 13.90 | 6.60 | 12.10 |
| RS | Sul | 5 327 | 15.30 | 13.20 | 6.10 | 10.90 |
| MT | Centro-Oeste | 885 | 18.10 | 16.10 | 6.00 | 11.30 |
| DF | Centro-Oeste | 2 074 | 12.90 | 11.40 | 5.70 | 8.10 |
| MG | Sudeste | 11 319 | 12.00 | 10.30 | 4.60 | 9.10 |
| SP | Sudeste | 40 399 | 8.70 | 7.20 | 4.50 | 9.00 |
| PR | Sul | 4 903 | 12.00 | 10.40 | 4.10 | 9.00 |

## Q6. Quel est l'impact d'un retard de livraison sur la note donnée par le client ?

Requête : [`sql/analyses/q06_retard_et_satisfaction.sql`](../sql/analyses/q06_retard_et_satisfaction.sql)

| delay_bucket | orders | orders_share_pct | avg_review_score | negative_reviews_pct | five_star_pct |
| --- | --- | --- | --- | --- | --- |
| 0. À l'heure ou en avance | 89 182 | 93.30 | 4.29 | 9.20 | 62.30 |
| 1. Retard de 1 à 3 jours | 1 355 | 1.40 | 3.51 | 25.50 | 36.20 |
| 2. Retard de 4 à 7 jours | 1 773 | 1.90 | 2.32 | 61.30 | 18.10 |
| 3. Retard de 8 à 14 jours | 1 748 | 1.80 | 1.74 | 78.10 | 7.90 |
| 4. Retard de plus de 14 jours | 1 502 | 1.60 | 1.71 | 78.80 | 7.00 |

## Q7. Quelle part des clients rachète, et que pèsent-ils dans le chiffre d'affaires ?

Requête : [`sql/analyses/q07_clients_recurrents.sql`](../sql/analyses/q07_clients_recurrents.sql)

| customer_type | customers | customers_share_pct | revenue_brl | revenue_share_pct | avg_lifetime_value | avg_delivered_orders |
| --- | --- | --- | --- | --- | --- | --- |
| Unique (1 commande livrée) | 90 557 | 97.00 | 14 555 586.29 | 94.40 | 160.73 | 1.00 |
| Récurrent (2 commandes livrées ou plus) | 2 801 | 3.00 | 864 187.46 | 5.60 | 308.53 | 2.11 |

## Q8. Le chiffre d'affaires est-il concentré sur quelques vendeurs ? (analyse de Pareto par décile)

Requête : [`sql/analyses/q08_pareto_vendeurs.sql`](../sql/analyses/q08_pareto_vendeurs.sql)

| decile | sellers | revenue_brl | revenue_share_pct | cumulative_share_pct | median_seller_revenue |
| --- | --- | --- | --- | --- | --- |
| 1 | 303 | 9 061 963.84 | 67.38 | 67.38 | 16 788.00 |
| 2 | 303 | 2 035 079.15 | 15.13 | 82.51 | 6 669.70 |
| 3 | 303 | 1 029 567.27 | 7.66 | 90.16 | 3 381.73 |
| 4 | 303 | 554 331.21 | 4.12 | 94.29 | 1 790.00 |
| 5 | 303 | 328 561.39 | 2.44 | 96.73 | 1 078.41 |
| 6 | 303 | 203 244.24 | 1.51 | 98.24 | 671.50 |
| 7 | 303 | 118 438.34 | 0.88 | 99.12 | 388.89 |
| 8 | 303 | 67 783.23 | 0.50 | 99.62 | 218.00 |
| 9 | 303 | 36 741.14 | 0.27 | 99.90 | 120.00 |
| 10 | 302 | 13 819.87 | 0.10 | 100.00 | 47.90 |

## Q9. À quels jours et à quelles heures les clients commandent-ils ?

Requête : [`sql/analyses/q09_saisonnalite_jour_heure.sql`](../sql/analyses/q09_saisonnalite_jour_heure.sql)

| day_name | 0h | 1h | 2h | 3h | 4h | 5h | 6h | 7h | 8h | 9h | 10h | 11h | 12h | 13h | 14h | 15h | 16h | 17h | 18h | 19h | 20h | 21h | 22h | 23h |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 326 | 134 | 65 | 36 | 19 | 22 | 69 | 158 | 478 | 777 | 1 031 | 1 074 | 968 | 1 026 | 1 093 | 1 072 | 1 089 | 988 | 924 | 945 | 1 027 | 1 116 | 987 | 717 |
| Tuesday | 306 | 158 | 80 | 28 | 29 | 24 | 71 | 223 | 522 | 861 | 964 | 1 053 | 896 | 1 035 | 1 119 | 1 039 | 1 074 | 965 | 874 | 919 | 985 | 1 023 | 961 | 687 |
| Wednesday | 396 | 178 | 81 | 33 | 33 | 27 | 93 | 210 | 512 | 827 | 1 042 | 1 056 | 915 | 1 027 | 1 046 | 980 | 1 039 | 961 | 850 | 847 | 900 | 961 | 873 | 614 |
| Thursday | 353 | 167 | 74 | 39 | 31 | 28 | 85 | 218 | 500 | 754 | 980 | 958 | 978 | 978 | 974 | 926 | 1 073 | 906 | 780 | 824 | 835 | 840 | 854 | 549 |
| Friday | 425 | 216 | 71 | 49 | 40 | 36 | 97 | 206 | 490 | 766 | 946 | 987 | 853 | 1 002 | 956 | 977 | 972 | 814 | 722 | 781 | 738 | 723 | 698 | 510 |
| Saturday | 315 | 174 | 66 | 43 | 24 | 24 | 53 | 105 | 246 | 431 | 658 | 708 | 689 | 705 | 675 | 718 | 696 | 699 | 708 | 756 | 726 | 650 | 546 | 428 |
| Sunday | 266 | 141 | 69 | 44 | 27 | 27 | 34 | 105 | 205 | 349 | 530 | 718 | 674 | 721 | 684 | 714 | 712 | 797 | 895 | 899 | 967 | 888 | 863 | 603 |

## Q9 (complément). Quels sont les jours records, comparés à la moyenne de leur mois ?

Requête : [`sql/analyses/q09b_jours_records.sql`](../sql/analyses/q09b_jours_records.sql)

| purchase_date | day_name | orders | month_daily_average | ratio_to_month_average |
| --- | --- | --- | --- | --- |
| 2017-11-24 | Friday | 1 176 | 251.50 | 4.70 |
| 2017-11-25 | Saturday | 499 | 251.50 | 2.00 |
| 2017-11-27 | Monday | 403 | 251.50 | 1.60 |
| 2017-11-26 | Sunday | 391 | 251.50 | 1.60 |
| 2017-11-28 | Tuesday | 380 | 251.50 | 1.50 |

## Q10. Comment les clients paient-ils, et le moyen de paiement change-t-il le panier ?

Requête : [`sql/analyses/q10_moyens_de_paiement.sql`](../sql/analyses/q10_moyens_de_paiement.sql)

| main_payment_type | orders | orders_share_pct | revenue_share_pct | average_order_value | avg_installments |
| --- | --- | --- | --- | --- | --- |
| credit_card | 73 891 | 75.50 | 78.50 | 166.54 | 3.55 |
| boleto | 19 479 | 19.90 | 18.00 | 144.64 | 1.00 |
| voucher | 3 028 | 3.10 | 2.20 | 114.92 | 1.15 |
| debit_card | 1 512 | 1.50 | 1.40 | 140.33 | 1.00 |

## Q10 (complément). Pour les cartes de crédit, le nombre de mensualités augmente-t-il avec le panier ?

Requête : [`sql/analyses/q10b_mensualites_et_panier.sql`](../sql/analyses/q10b_mensualites_et_panier.sql)

| installments_bucket | orders | orders_share_pct | average_order_value | median_order_value |
| --- | --- | --- | --- | --- |
| 1. Comptant | 23 675 | 32.00 | 100.81 | 71.64 |
| 2. 2 à 3 fois | 22 344 | 30.20 | 135.25 | 111.50 |
| 3. 4 à 6 fois | 15 922 | 21.50 | 182.07 | 128.19 |
| 4. 7 à 10 fois | 11 614 | 15.70 | 333.87 | 206.24 |
| 5. Plus de 10 fois | 336 | 0.50 | 360.12 | 214.16 |
