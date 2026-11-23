"""Construit les livrables à partir de la base DuckDB et des résultats d'analyse.

- docs/report/index.html : page de graphiques interactifs (intégrable au portfolio) ;
- reports/QUALITE.md     : rapport de qualité des données (règles, scores, actions) ;
- exports/*.csv          : jeux agrégés prêts pour Looker Studio ou Power BI.

Usage : python scripts/build_report.py   (après run_analyses.py)
"""
from __future__ import annotations

import html
import os
import shutil
import sys
from pathlib import Path

import duckdb
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "reports" / "results"
DB_PATH = Path(os.environ.get("OLIST_DUCKDB_PATH", ROOT / "data" / "olist.duckdb"))

TEAL, VIOLET, INK, MUTED = "#0f9f8f", "#7c5cd6", "#16202b", "#5b6b7a"
FONT = dict(family="Inter, Segoe UI, Arial, sans-serif", color=INK, size=13)


def load(name: str) -> pd.DataFrame:
    return pd.read_csv(RESULTS / f"{name}.csv")


def brl(v: float) -> str:
    return f"R$ {v:,.0f}".replace(",", " ")


def styled(fig: go.Figure, height: int = 380) -> go.Figure:
    fig.update_layout(template="plotly_white", font=FONT, height=height,
                      margin=dict(l=10, r=10, t=10, b=10), legend_title_text="",
                      hoverlabel=dict(font_size=13))
    return fig


# ---------------------------------------------------------------- graphiques
def charts() -> list[tuple[str, str, str, go.Figure]]:
    """(id, question, constat, figure) pour chaque analyse."""
    out = []

    q1 = load("q01_chiffre_affaires_mensuel")
    q1["month"] = pd.to_datetime(q1["month"])
    fig = go.Figure()
    fig.add_bar(x=q1["month"], y=q1["revenue_brl"], name="Chiffre d'affaires (BRL)", marker_color=TEAL)
    fig.add_scatter(x=q1["month"], y=q1["orders"], name="Commandes", yaxis="y2",
                    line=dict(color=VIOLET, width=3))
    fig.update_layout(yaxis=dict(title="BRL"), yaxis2=dict(title="Commandes", overlaying="y", side="right",
                                                           showgrid=False))
    nov = q1.loc[q1["month"] == "2017-11-01"].iloc[0]
    out.append(("q1", "Comment évoluent le chiffre d'affaires et les commandes ?",
                f"{brl(q1['revenue_brl'].sum())} sur 20 mois. Les commandes passent de {q1['orders'].iloc[0]:,} "
                f"(janv. 2017) à environ {int(q1['orders'].tail(6).mean()):,} par mois en 2018, puis plafonnent. "
                f"Pic de novembre 2017 : +{nov['revenue_growth_mom_pct']:.0f} % (Black Friday).".replace(",", " "),
                styled(fig)))

    q2 = load("q02_panier_moyen_par_region")
    fig = px.bar(q2, x="customer_region", y=["average_order_value", "average_freight"], barmode="group",
                 color_discrete_sequence=[TEAL, VIOLET],
                 labels={"value": "BRL", "customer_region": "Région", "variable": ""})
    fig.for_each_trace(lambda t: t.update(name={"average_order_value": "Panier moyen",
                                                "average_freight": "Frais de port moyens"}[t.name]))
    se, no = q2.set_index("customer_region").loc["Sudeste"], q2.set_index("customer_region").loc["Norte"]
    out.append(("q2", "Le panier moyen varie-t-il selon la région ?",
                f"Le Sudeste fait {100 * se['orders'] / q2['orders'].sum():.0f} % des commandes avec le panier le "
                f"plus bas ({brl(se['average_order_value'])}). Dans le Norte, le port pèse "
                f"{no['freight_share_pct']:.1f} % du panier contre {se['freight_share_pct']:.1f} % dans le Sudeste.",
                styled(fig)))

    q3 = load("q03_top_categories").sort_values("revenue_brl")
    fig = px.bar(q3, x="revenue_brl", y="category", orientation="h", color_discrete_sequence=[TEAL],
                 labels={"revenue_brl": "Chiffre d'affaires produits (BRL)", "category": ""},
                 hover_data={"revenue_share_pct": True, "average_item_price": True})
    out.append(("q3", "Quelles catégories pèsent le plus ?",
                f"Les 10 premières catégories (sur {int(q3['categories_total'].iloc[0])}) font "
                f"{q3['cumulative_share_pct'].max():.1f} % du chiffre d'affaires produits ; "
                f"« {q3.iloc[-1]['category']} » arrive en tête avec {q3.iloc[-1]['revenue_share_pct']:.1f} %.",
                styled(fig, 420)))

    q4 = load("q04_retention_cohortes")
    months = [f"m{k}_pct" for k in range(1, 7)]
    z = q4[months].values
    fig = go.Figure(go.Heatmap(z=z, x=[f"M+{k}" for k in range(1, 7)],
                               y=pd.to_datetime(q4["cohort_month"]).dt.strftime("%Y-%m"),
                               colorscale=[[0, "#f3f7f9"], [1, TEAL]], text=z, texttemplate="%{text:.2f}%",
                               hovertemplate="Cohorte %{y}<br>%{x} : %{z:.2f} %<extra></extra>"))
    fig.update_yaxes(autorange="reversed")
    out.append(("q4", "Les clients reviennent-ils acheter ?",
                f"Très peu : selon la cohorte, seuls {q4['returned_within_6m_pct'].min():.1f} à "
                f"{q4['returned_within_6m_pct'].max():.1f} % des clients recommandent dans les 6 mois, et moins de "
                f"{q4['m1_pct'].max():.1f} % le mois suivant.", styled(fig, 460)))

    q5 = load("q05_delais_livraison_par_etat")
    fig = px.scatter(q5, x="avg_delivery_days", y="late_rate_pct", size="delivered_orders", color="customer_region",
                     text="customer_state", size_max=48,
                     color_discrete_sequence=[TEAL, VIOLET, "#e08a3c", "#3c7be0", "#c94f6d"],
                     labels={"avg_delivery_days": "Délai moyen (jours)", "late_rate_pct": "Taux de retard (%)",
                             "customer_region": "Région"})
    fig.update_traces(textposition="middle center", textfont_size=10)
    worst, sp = q5.iloc[0], q5.set_index("customer_state").loc["SP"]
    out.append(("q5", "Où les livraisons sont-elles lentes et en retard ?",
                f"{worst['customer_state']} : {worst['avg_delivery_days']:.1f} jours en moyenne et "
                f"{worst['late_rate_pct']:.1f} % de retards, contre {sp['avg_delivery_days']:.1f} jours et "
                f"{sp['late_rate_pct']:.1f} % à São Paulo. Le Nordeste concentre les retards.", styled(fig, 440)))

    q6 = load("q06_retard_et_satisfaction")
    q6["label"] = q6["delay_bucket"].str[3:]
    fig = px.bar(q6, x="label", y="avg_review_score", color="negative_reviews_pct",
                 color_continuous_scale=[[0, TEAL], [1, "#c94f6d"]], text="avg_review_score",
                 labels={"label": "", "avg_review_score": "Note moyenne (/5)", "negative_reviews_pct": "% avis ≤ 2"})
    on_time, late = q6.iloc[0], q6.iloc[1:]
    out.append(("q6", "Quel est l'impact d'un retard sur la note client ?",
                f"Une commande à l'heure obtient {on_time['avg_review_score']:.2f}/5. Au-delà d'une semaine de "
                f"retard, la note tombe à {q6.iloc[3]['avg_review_score']:.2f}/5 avec "
                f"{q6.iloc[3]['negative_reviews_pct']:.0f} % d'avis négatifs. "
                f"{late['orders_share_pct'].sum():.1f} % des commandes livrées sont en retard.", styled(fig)))

    q7 = load("q07_clients_recurrents")
    fig = go.Figure()
    for col, name, color in [("customers_share_pct", "Part des clients", TEAL),
                             ("revenue_share_pct", "Part du chiffre d'affaires", VIOLET)]:
        fig.add_bar(x=q7["customer_type"], y=q7[col], name=name, marker_color=color,
                    text=q7[col].map(lambda v: f"{v:.1f} %"))
    fig.update_layout(barmode="group", yaxis_title="%")
    rep = q7.loc[q7["customer_type"].str.startswith("Récurrent")].iloc[0]
    one = q7.loc[q7["customer_type"].str.startswith("Unique")].iloc[0]
    out.append(("q7", "Quelle part des clients rachète ?",
                f"Seulement {rep['customers_share_pct']:.1f} % des clients ont plusieurs commandes livrées, pour "
                f"{rep['revenue_share_pct']:.1f} % du chiffre d'affaires. Mais ils valent "
                f"{rep['avg_lifetime_value'] / one['avg_lifetime_value']:.1f} fois plus "
                f"({brl(rep['avg_lifetime_value'])} contre {brl(one['avg_lifetime_value'])}).", styled(fig)))

    q8 = load("q08_pareto_vendeurs")
    fig = go.Figure()
    fig.add_bar(x=q8["decile"].map(lambda d: f"D{d}"), y=q8["revenue_share_pct"], name="Part du décile",
                marker_color=TEAL)
    fig.add_scatter(x=q8["decile"].map(lambda d: f"D{d}"), y=q8["cumulative_share_pct"], name="Cumul",
                    line=dict(color=VIOLET, width=3))
    fig.update_layout(yaxis_title="% du chiffre d'affaires", xaxis_title="Déciles de vendeurs (D1 = les 10 % meilleurs)")
    out.append(("q8", "Le chiffre d'affaires est-il concentré sur quelques vendeurs ?",
                f"Oui : les 10 % meilleurs vendeurs ({int(q8.iloc[0]['sellers'])}) réalisent "
                f"{q8.iloc[0]['revenue_share_pct']:.1f} % du chiffre d'affaires, et 20 % des vendeurs en font "
                f"{q8.iloc[1]['cumulative_share_pct']:.1f} %.", styled(fig)))

    q9 = load("q09_saisonnalite_jour_heure")
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    grid = q9.pivot_table(index="iso_day_of_week", columns="hour_of_day", values="orders", aggfunc="sum")
    fig = go.Figure(go.Heatmap(z=grid.values, x=[f"{h}h" for h in grid.columns], y=days,
                               colorscale=[[0, "#f3f7f9"], [1, VIOLET]],
                               hovertemplate="%{y} %{x} : %{z} commandes<extra></extra>"))
    fig.update_yaxes(autorange="reversed")
    q9b = load("q09b_jours_records")
    top = q9b.iloc[0]
    out.append(("q9", "Quand les clients commandent-ils ?",
                f"Surtout en semaine entre 10 h et 16 h, avec un second pic vers 21 h ; le samedi est le jour le plus "
                f"calme. Record absolu : {pd.to_datetime(top['purchase_date']).strftime('%d/%m/%Y')} (Black Friday), "
                f"{int(top['orders']):,} commandes, soit {top['ratio_to_month_average']:.1f} fois la moyenne du mois."
                .replace(",", " "), styled(fig, 360)))

    q10b = load("q10b_mensualites_et_panier")
    q10 = load("q10_moyens_de_paiement")
    fig = px.bar(q10b, x=q10b["installments_bucket"].str[3:], y="average_order_value",
                 text=q10b["average_order_value"].map(lambda v: f"R$ {v:.0f}"), color_discrete_sequence=[TEAL],
                 labels={"x": "Mensualités (carte de crédit)", "average_order_value": "Panier moyen (BRL)"})
    cc = q10.set_index("main_payment_type").loc["credit_card"]
    out.append(("q10", "Le moyen de paiement change-t-il le panier ?",
                f"La carte de crédit représente {cc['orders_share_pct']:.1f} % des commandes et "
                f"{cc['revenue_share_pct']:.1f} % du chiffre d'affaires. Le paiement en 7 à 10 fois accompagne un "
                f"panier de {brl(q10b.iloc[3]['average_order_value'])}, contre {brl(q10b.iloc[0]['average_order_value'])} "
                f"au comptant.", styled(fig)))
    return out


# ---------------------------------------------------------------- qualité
def quality(con: duckdb.DuckDBPyConnection) -> tuple[pd.DataFrame, pd.DataFrame]:
    checks = con.sql("select * from quality.dq_checks order by check_id").df()
    scores = con.sql("select * from quality.dq_table_scores order by quality_score").df()
    return checks, scores


def quality_markdown(checks: pd.DataFrame, scores: pd.DataFrame) -> str:
    lines = ["# Rapport de qualité des données", "",
             "Généré par `scripts/build_report.py` à partir des modèles dbt `quality.dq_checks` et "
             "`quality.dq_table_scores`. Politique de qualité et rôles : [GOUVERNANCE.md](../GOUVERNANCE.md).", "",
             "## Score par table", "", "| Table | Règles | Hors seuil | Lignes en échec | Score /100 | Règle la plus dégradée |",
             "| --- | --- | --- | --- | --- | --- |"]
    for r in scores.itertuples():
        lines.append(f"| {r.table_name} | {r.checks_count} | {r.checks_out_of_threshold} | "
                     f"{r.failed_rows:,} | {r.quality_score:.2f} | {r.worst_check} |".replace(",", " "))
    lines += ["", "## Détail des règles", "",
              "| Règle | Table | Dimension | Description | Échecs | Population | % échec | Seuil % | Statut |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in checks.itertuples():
        status = "✅ conforme" if r.status == "conforme" else "⚠️ hors seuil"
        lines.append(f"| {r.check_id} | {r.table_name} | {r.quality_dimension} | {r.description} | "
                     f"{r.failed_rows:,} | {r.total_rows:,} | {r.failed_pct:.3f} | {r.threshold_pct:g} | {status} |"
                     .replace(",", " "))
    out = checks[checks["status"] != "conforme"]
    lines += ["", "## Règles hors seuil et traitement", "",
              "| Règle | Traitement dans le pipeline | Action recommandée à la source |", "| --- | --- | --- |"]
    actions = {
        "GEO-01": ("Agrégation en un point médian par préfixe (int_geolocation__zip_centroids)",
                   "Dédoublonner le référentiel à l'ingestion ; une ligne par préfixe et par point distinct"),
        "ORD-03": ("Conservé et signalé ; non utilisé pour les délais (calculés depuis l'achat)",
                   "Contrôler l'horloge et le fuseau du système transporteur"),
        "PRD-01": ("Catégorie « unknown » dans dim_products, visible dans les analyses",
                   "Rendre la catégorie obligatoire à la création d'un produit"),
        "REV-01": ("Clé de la table = (review_id, order_id) : l'avis est rattaché à chaque commande concernée",
                   "Documenter ce cas dans le contrat d'interface, ou émettre un identifiant d'avis par commande"),
        "REV-02": ("Règle de gestion : l'avis le plus récent fait foi (int_orders__reviews)",
                   "Limiter à un avis par commande ou historiser explicitement les mises à jour"),
    }
    for r in out.itertuples():
        a, b = actions.get(r.check_id, ("À analyser", "À définir avec le data steward"))
        lines.append(f"| {r.check_id} — {r.description} | {a} | {b} |")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- exports
def exports(con: duckdb.DuckDBPyConnection) -> None:
    out = ROOT / "exports"
    out.mkdir(exist_ok=True)
    queries = {
        "ventes_quotidiennes": """
            select purchase_date, customer_state, customer_region, main_payment_type,
                   count(*) as orders, round(sum(order_value), 2) as revenue_brl,
                   round(avg(review_score), 2) as avg_review_score,
                   count(*) filter (where is_late) as late_orders, count(*) filter (where is_delivered) as delivered_orders
            from marts.fct_orders
            where in_analysis_window and order_status not in ('canceled', 'unavailable')
            group by all order by purchase_date""",
        "ventes_categories_mensuelles": """
            select cast(date_trunc('month', purchase_date) as date) as month, category, customer_region,
                   count(*) as items_sold, round(sum(price), 2) as revenue_brl
            from marts.fct_order_items
            where in_analysis_window and order_status not in ('canceled', 'unavailable')
            group by all order by month""",
        "livraisons_par_etat": "select * from read_csv('reports/results/q05_delais_livraison_par_etat.csv')",
        "qualite_regles": "select * from quality.dq_checks",
    }
    for name, sql in queries.items():
        con.sql(sql).df().to_csv(out / f"{name}.csv", index=False)
        print(f"exports/{name}.csv")


# ---------------------------------------------------------------- page HTML
PAGE = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Olist · Analyse des ventes et qualité des données</title>
<meta name="description" content="Étude de cas Data Analyst / BI : SQL, dbt, DuckDB et gouvernance des données sur 100 000 commandes e-commerce.">
<style>
:root {{ --ink:#16202b; --muted:#5b6b7a; --teal:#0f9f8f; --violet:#7c5cd6; --line:#e3e9ee; --bg:#f7fafb; }}
* {{ box-sizing:border-box }}
body {{ margin:0; font:16px/1.6 Inter, "Segoe UI", Arial, sans-serif; color:var(--ink); background:var(--bg) }}
header {{ background:linear-gradient(135deg,#0d2b33,#1e2b38); color:#fff; padding:48px 20px 40px }}
.wrap {{ max-width:1080px; margin:0 auto; padding:0 16px }}
h1 {{ margin:0 0 8px; font-size:clamp(26px,4vw,38px); line-height:1.15 }}
header p {{ margin:0; color:#c9d6df; max-width:760px }}
.tags {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:18px }}
.tags span {{ font-size:13px; padding:4px 10px; border-radius:99px; background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.18) }}
.kpis {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin:-26px auto 10px }}
.kpi {{ background:#fff; border:1px solid var(--line); border-radius:14px; padding:16px }}
.kpi b {{ display:block; font-size:24px }} .kpi span {{ color:var(--muted); font-size:13px }}
section.card {{ background:#fff; border:1px solid var(--line); border-radius:16px; padding:22px; margin:18px 0 }}
section.card h2 {{ margin:0 0 6px; font-size:20px }}
.finding {{ margin:0 0 12px; color:#2d3b48 }} .finding::before {{ content:"→ "; color:var(--teal); font-weight:700 }}
.q {{ color:var(--teal); font-weight:700; font-size:13px; letter-spacing:.06em }}
table {{ width:100%; border-collapse:collapse; font-size:14px }} th, td {{ text-align:left; padding:8px; border-bottom:1px solid var(--line) }}
th {{ color:var(--muted); font-weight:600 }} .ok {{ color:#0f8a5f }} .ko {{ color:#c0572b; font-weight:600 }}
.tablewrap {{ overflow-x:auto }}
footer {{ color:var(--muted); font-size:13px; padding:30px 0 50px }}
a {{ color:var(--teal) }}
@media (max-width:720px) {{ .kpis {{ grid-template-columns:1fr 1fr }} }}
</style></head>
<body>
<header><div class="wrap">
<h1>Analyse des ventes et qualité des données</h1>
<p>Étude de cas Data Analyst / BI sur environ 100 000 commandes de la marketplace brésilienne Olist (janvier 2017 à août 2018).
Données modélisées avec <b>dbt + DuckDB</b> (modèle en étoile, {tests} tests automatiques), contrôlées par {rules} règles de qualité
et documentées pour la gouvernance (dictionnaire, lignage, glossaire).</p>
<div class="tags"><span>SQL</span><span>dbt</span><span>DuckDB</span><span>Modèle en étoile</span><span>Qualité des données</span><span>Gouvernance</span><span>Python</span><span>Plotly</span></div>
</div></header>
<div class="wrap">
<div class="kpis">
<div class="kpi"><b>{revenue}</b><span>chiffre d'affaires analysé</span></div>
<div class="kpi"><b>{orders}</b><span>commandes</span></div>
<div class="kpi"><b>{late:.1f} %</b><span>commandes livrées en retard</span></div>
<div class="kpi"><b>{dq:.1f}/100</b><span>score qualité moyen des tables</span></div>
</div>
{sections}
<section class="card" id="qualite"><span class="q">QUALITÉ DES DONNÉES</span><h2>Score par table</h2>
<p class="finding">{dq_finding}</p>
<div class="tablewrap"><table><thead><tr><th>Table</th><th>Règles</th><th>Hors seuil</th><th>Lignes en échec</th><th>Score</th><th>Règle la plus dégradée</th></tr></thead>
<tbody>{dq_rows}</tbody></table></div></section>
<footer>Données : <a href="https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce">Olist, Brazilian E-Commerce Public Dataset</a> (CC BY-NC-SA 4.0).
Code et requêtes : <a href="https://github.com/tsitohaina23/olist-analytics-governance">github.com/tsitohaina23/olist-analytics-governance</a> ·
Sitraka Tsitohaina RAJOELISOLO</footer>
</div></body></html>
"""


def build_page(con: duckdb.DuckDBPyConnection, items, checks: pd.DataFrame, scores: pd.DataFrame) -> str:
    kpi = con.sql("""
        select sum(order_value) filter (where order_status not in ('canceled','unavailable')) as revenue,
               count(*) as orders,
               100.0 * count(*) filter (where is_late) / count(*) filter (where is_delivered) as late_pct
        from marts.fct_orders where in_analysis_window""").fetchone()
    sections = []
    for i, (cid, question, finding, fig) in enumerate(items):
        div = fig.to_html(full_html=False, include_plotlyjs="plotly.min.js" if i == 0 else False,
                          config={"displayModeBar": False, "responsive": True})
        sections.append(f'<section class="card" id="{cid}"><span class="q">{cid.upper()}</span>'
                        f"<h2>{html.escape(question)}</h2><p class=\"finding\">{html.escape(finding)}</p>{div}</section>")
    rows = "".join(
        f"<tr><td>{r.table_name}</td><td>{r.checks_count}</td>"
        f"<td class=\"{'ko' if r.checks_out_of_threshold else 'ok'}\">{r.checks_out_of_threshold}</td>"
        f"<td>{r.failed_rows:,}</td><td>{r.quality_score:.2f}</td><td>{r.worst_check}</td></tr>".replace(",", " ")
        for r in scores.itertuples())
    worst = scores.iloc[0]
    dq_finding = (f"{len(checks)} règles contrôlées, {int((checks['status'] != 'conforme').sum())} hors seuil. "
                  f"Table la plus dégradée : {worst['table_name']} ({worst['quality_score']:.1f}/100), "
                  f"surtout à cause de la règle {worst['worst_check']}. Toutes les anomalies sont traitées "
                  f"explicitement dans le pipeline, et non masquées.")
    run = pd.read_json(ROOT / "dbt" / "target" / "run_results.json", typ="series")
    tests = sum(1 for r in run["results"] if r["unique_id"].startswith("test."))
    return PAGE.format(tests=tests, rules=len(checks), revenue=brl(kpi[0]), orders=f"{kpi[1]:,}".replace(",", " "),
                       late=kpi[2], dq=scores["quality_score"].mean(), sections="\n".join(sections),
                       dq_finding=html.escape(dq_finding), dq_rows=rows)


def main() -> int:
    if not DB_PATH.exists() or not RESULTS.exists():
        print("Lancez d'abord dbt build puis scripts/run_analyses.py.")
        return 1
    with duckdb.connect(str(DB_PATH), read_only=True) as con:
        checks, scores = quality(con)
        (ROOT / "reports" / "QUALITE.md").write_text(quality_markdown(checks, scores), encoding="utf-8")
        print("reports/QUALITE.md")
        exports(con)
        page = build_page(con, charts(), checks, scores)
    target = ROOT / "docs" / "report"
    target.mkdir(parents=True, exist_ok=True)
    (target / "index.html").write_text(page, encoding="utf-8")
    # Plotly servi localement à côté de la page : aucune dépendance à un CDN externe
    shutil.copyfile(Path(plotly.__file__).parent / "package_data" / "plotly.min.js", target / "plotly.min.js")
    print("docs/report/index.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
