"""Tests du projet (en plus des 95 tests dbt).

- règles de gouvernance vérifiables sans données (analyses, glossaire, métadonnées dbt) ;
- contrôles de cohérence sur la base construite (ignorés si `dbt build` n'a pas encore tourné).

Usage : pytest -q
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

DB_PATH = ROOT / "data" / "olist.duckdb"
ANALYSES = sorted((ROOT / "sql" / "analyses").glob("*.sql"))


# ---------------------------------------------------------------- gouvernance
def test_download_script_covers_the_nine_source_files():
    from download_data import EXPECTED_ROWS

    sources = yaml.safe_load((ROOT / "dbt" / "models" / "staging" / "_sources.yml").read_text(encoding="utf-8"))
    declared = {t["name"] + ".csv" for t in sources["sources"][0]["tables"]}
    assert set(EXPECTED_ROWS) == declared
    assert len(declared) == 9


@pytest.mark.parametrize("path", ANALYSES, ids=lambda p: p.stem)
def test_analyses_only_read_certified_marts(path):
    sql = path.read_text(encoding="utf-8").lower()
    schemas = set(re.findall(r"\b(staging|intermediate|marts|quality|reference)\.\w+", sql))
    assert schemas == {"marts"}, f"{path.name} lit une couche non certifiée : {schemas}"


@pytest.mark.parametrize("path", ANALYSES, ids=lambda p: p.stem)
def test_analyses_start_with_their_business_question(path):
    first = path.read_text(encoding="utf-8").splitlines()[0]
    assert re.match(r"-- Q\d+", first), f"{path.name} doit commencer par « -- Qn. question »"


def _model_docs() -> list[dict]:
    models = []
    for yml in (ROOT / "dbt" / "models").rglob("_*.yml"):
        models += yaml.safe_load(yml.read_text(encoding="utf-8")).get("models", [])
    return models


def test_every_model_is_documented_with_owner_steward_and_sensitivity():
    sql_models = {p.stem for p in (ROOT / "dbt" / "models").rglob("*.sql")}
    docs = {m["name"]: m for m in _model_docs()}
    assert sql_models == set(docs), f"modèles sans documentation : {sql_models - set(docs)}"
    for name, model in docs.items():
        meta = model.get("config", {}).get("meta", {})
        assert model.get("description"), f"{name} : description manquante"
        for key in ("owner", "steward", "sensitivity"):
            assert meta.get(key), f"{name} : meta.{key} manquant"
        assert meta["sensitivity"] in {"public", "internal", "pii"}


def test_glossary_is_valid_skos_with_bilingual_definitions():
    rdflib = pytest.importorskip("rdflib")
    from rdflib.namespace import RDF, SKOS

    g = rdflib.Graph().parse(ROOT / "governance" / "glossaire.ttl", format="turtle")
    concepts = set(g.subjects(RDF.type, SKOS.Concept))
    assert len(concepts) >= 15
    for c in concepts:
        labels = {lbl.language for lbl in g.objects(c, SKOS.prefLabel)}
        assert {"fr", "en"} <= labels, f"{c} : libellé FR et EN requis"
        assert any(True for _ in g.objects(c, SKOS.definition)), f"{c} : définition manquante"
        assert any(True for _ in g.objects(c, SKOS.inScheme)), f"{c} : hors du schéma de concepts"


# ---------------------------------------------------------------- données
needs_db = pytest.mark.skipif(not DB_PATH.exists(), reason="base absente : lancer d'abord dbt build")


@pytest.fixture(scope="module")
def con():
    duckdb = pytest.importorskip("duckdb")
    with duckdb.connect(str(DB_PATH), read_only=True) as c:
        yield c


@needs_db
def test_fact_table_keeps_every_source_order(con):
    raw = con.sql("select count(*) from read_csv('data/raw/olist_orders_dataset.csv', header = true)").fetchone()[0] \
        if (ROOT / "data" / "raw" / "olist_orders_dataset.csv").exists() else 99_441
    assert con.sql("select count(*), count(distinct order_id) from marts.fct_orders").fetchone() == (raw, raw)


@needs_db
def test_revenue_is_identical_across_grains(con):
    by_order = con.sql("select sum(items_value) from marts.fct_orders").fetchone()[0]
    by_item = con.sql("select sum(price) from marts.fct_order_items").fetchone()[0]
    assert by_order == by_item


@needs_db
def test_quality_catalogue_has_twenty_rules_with_sane_figures(con):
    rows = con.sql("select failed_rows, total_rows, failed_pct from quality.dq_checks").fetchall()
    assert len(rows) == 20
    for failed, total, pct in rows:
        assert 0 <= failed <= total and total > 0
        assert pct == pytest.approx(100 * failed / total, abs=1e-3)


@needs_db
def test_report_kpis_match_the_warehouse(con):
    html = (ROOT / "docs" / "report" / "index.html").read_text(encoding="utf-8")
    revenue = con.sql("""select sum(order_value) from marts.fct_orders
                         where in_analysis_window and order_status not in ('canceled', 'unavailable')""").fetchone()[0]
    assert f"R$ {revenue:,.0f}".replace(",", " ") in html
