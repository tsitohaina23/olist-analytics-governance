"""Exécute les requêtes de sql/analyses sur la base DuckDB construite par dbt.

Sorties :
- reports/results/<requête>.csv : résultat brut de chaque requête ;
- reports/RESULTATS.md : toutes les questions et leurs résultats en tableaux.

Usage : python scripts/run_analyses.py   (après `dbt build`)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = ROOT / "sql" / "analyses"
OUT_DIR = ROOT / "reports" / "results"
DB_PATH = Path(os.environ.get("OLIST_DUCKDB_PATH", ROOT / "data" / "olist.duckdb"))


def question_of(sql: str) -> str:
    """Première ligne de commentaire de la requête = la question métier."""
    for line in sql.splitlines():
        if line.startswith("--"):
            return line.lstrip("- ").strip()
    return ""


def to_markdown(df: pd.DataFrame) -> str:
    def fmt(v):
        if isinstance(v, pd.Timestamp):
            return v.strftime("%Y-%m-%d")
        if isinstance(v, float):
            return "—" if pd.isna(v) else f"{v:,.2f}".replace(",", " ")
        if isinstance(v, int) and not isinstance(v, bool):
            return f"{v:,}".replace(",", " ")
        return str(v)

    head = "| " + " | ".join(df.columns) + " |"
    sep = "| " + " | ".join("---" for _ in df.columns) + " |"
    rows = ["| " + " | ".join(fmt(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join([head, sep, *rows])


def run_all(con: duckdb.DuckDBPyConnection) -> dict[str, tuple[str, pd.DataFrame]]:
    results = {}
    for path in sorted(SQL_DIR.glob("*.sql")):
        sql = path.read_text(encoding="utf-8")
        results[path.stem] = (question_of(sql), con.sql(sql).df())
    return results


def main() -> int:
    if not DB_PATH.exists():
        print(f"Base introuvable : {DB_PATH}. Lancez d'abord dbt build.")
        return 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(DB_PATH), read_only=True) as con:
        results = run_all(con)

    lines = ["# Résultats des analyses", "",
             "Généré par `scripts/run_analyses.py` à partir des requêtes de `sql/analyses/`.", ""]
    for name, (question, df) in results.items():
        df.to_csv(OUT_DIR / f"{name}.csv", index=False)
        shown = df
        if name.startswith("q09_"):
            # 168 lignes jour × heure : affichées en tableau croisé (jours en lignes, heures en colonnes)
            shown = (df.pivot_table(index=["iso_day_of_week", "day_name"], columns="hour_of_day",
                                    values="orders", aggfunc="sum")
                       .reset_index().drop(columns="iso_day_of_week"))
            shown.columns = [str(c) if isinstance(c, str) else f"{c}h" for c in shown.columns]
            shown = shown.astype({c: int for c in shown.columns if c.endswith("h")})
        lines += [f"## {question}", "", f"Requête : [`sql/analyses/{name}.sql`](../sql/analyses/{name}.sql)", "",
                  to_markdown(shown), ""]
        print(f"{name}: {len(df)} lignes")
    (ROOT / "reports" / "RESULTATS.md").write_text("\n".join(lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
