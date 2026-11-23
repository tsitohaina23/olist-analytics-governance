"""Télécharge les 9 fichiers CSV du jeu de données Olist et vérifie leur intégrité.

Source officielle : https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
(Olist, licence CC BY-NC-SA 4.0). Par défaut, les fichiers sont récupérés depuis une
copie publique sur Hugging Face, qui ne demande pas de compte. Chaque fichier est
contrôlé : nom attendu et nombre de lignes identique à la publication officielle.

Usage :
    python scripts/download_data.py            # télécharge dans data/raw/
    python scripts/download_data.py --check    # vérifie seulement les fichiers présents

Pour utiliser Kaggle à la place : téléchargez l'archive depuis la page officielle,
décompressez les CSV dans data/raw/, puis lancez --check.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import requests

MIRROR = "https://huggingface.co/datasets/aviahYadler/Olist_Ecommerce_Dataset/resolve/main/"
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# Nombre de lignes (hors en-tête) de la publication officielle Olist.
EXPECTED_ROWS = {
    "olist_customers_dataset.csv": 99_441,
    "olist_geolocation_dataset.csv": 1_000_163,
    "olist_order_items_dataset.csv": 112_650,
    "olist_order_payments_dataset.csv": 103_886,
    "olist_order_reviews_dataset.csv": 99_224,
    "olist_orders_dataset.csv": 99_441,
    "olist_products_dataset.csv": 32_951,
    "olist_sellers_dataset.csv": 3_095,
    "product_category_name_translation.csv": 71,
}


def count_rows(path: Path) -> int:
    # csv gère les retours à la ligne à l'intérieur des commentaires d'avis
    with path.open(encoding="utf-8", newline="") as f:
        return sum(1 for _ in csv.reader(f)) - 1


def download(name: str) -> None:
    dest = RAW_DIR / name
    tmp = dest.with_suffix(".part")
    with requests.get(MIRROR + name, stream=True, timeout=60) as r:
        r.raise_for_status()
        with tmp.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                f.write(chunk)
    tmp.replace(dest)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="vérifie sans télécharger")
    args = parser.parse_args()
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    ok = True
    for name, expected in EXPECTED_ROWS.items():
        path = RAW_DIR / name
        if not args.check and not path.exists():
            print(f"téléchargement  {name} ...", flush=True)
            download(name)
        if not path.exists():
            print(f"MANQUANT        {name}")
            ok = False
            continue
        rows = count_rows(path)
        status = "ok" if rows == expected else "ÉCART"
        ok &= rows == expected
        print(f"{status:<15} {name}: {rows:,} lignes (attendu {expected:,})")

    print("Données complètes et conformes." if ok else "Problème détecté : voir ci-dessus.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
