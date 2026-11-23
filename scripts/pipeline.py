"""Exécute tout le pipeline, dans l'ordre, depuis la racine du dépôt.

1. téléchargement et vérification des données ;
2. dbt build (référentiels, modèles, 95 tests, contrat de données) ;
3. analyses SQL ;
4. rapport interactif, rapport qualité, exports ;
5. documentation dbt statique (dictionnaire et lignage).

Usage : python scripts/pipeline.py [--skip-download]
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIN = Path(sys.executable).parent
DBT = shutil.which("dbt", path=str(BIN)) or "dbt"
DBT_ARGS = ["--project-dir", "dbt", "--profiles-dir", "dbt"]


def step(title: str, cmd: list[str]) -> None:
    print(f"\n=== {title}", flush=True)
    env = {**os.environ, "DBT_SEND_ANONYMOUS_USAGE_STATS": "false"}
    result = subprocess.run(cmd, cwd=ROOT, env=env)
    if result.returncode != 0:
        sys.exit(f"Échec de l'étape « {title} » (code {result.returncode}).")


def main() -> None:
    py = sys.executable
    if "--skip-download" not in sys.argv:
        step("Données sources", [py, "scripts/download_data.py"])
    else:
        step("Vérification des données", [py, "scripts/download_data.py", "--check"])
    step("dbt build", [DBT, "build", *DBT_ARGS])
    step("Analyses SQL", [py, "scripts/run_analyses.py"])
    step("Rapports et exports", [py, "scripts/build_report.py"])
    step("Documentation dbt", [DBT, "docs", "generate", "--static", *DBT_ARGS])
    target = ROOT / "docs" / "dbt-docs"
    target.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "dbt" / "target" / "static_index.html", target / "index.html")
    print("\nTerminé. Rapport : docs/report/index.html · Documentation : docs/dbt-docs/index.html")


if __name__ == "__main__":
    main()
