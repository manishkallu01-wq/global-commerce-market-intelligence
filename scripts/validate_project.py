#!/usr/bin/env python3
"""Fail fast when required project contracts or documentation are missing."""

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "LICENSE",
    "configs/workload_profiles.yml",
    "contracts/product_offer.schema.json",
    "dashboards/kpi_catalog.yml",
    "docs/architecture.md",
    "docs/source_strategy.md",
]


def main() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit(f"Missing required files: {', '.join(missing)}")
    json.loads((ROOT / "contracts/product_offer.schema.json").read_text())
    yaml.safe_load((ROOT / "configs/workload_profiles.yml").read_text())
    yaml.safe_load((ROOT / "dashboards/kpi_catalog.yml").read_text())
    readme = (ROOT / "README.md").read_text()
    for heading in ("What this project solves", "Genuine open data sources", "Dashboard outcomes"):
        if heading not in readme:
            raise SystemExit(f"README is missing: {heading}")
    print("Project structure and contracts are valid.")


if __name__ == "__main__":
    main()
