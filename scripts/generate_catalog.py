#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dict capability catalog generator (Ticket 04)

Generates capabilities/catalog-v1.json from tracked .txt wordlists,
including only assets marked accepted in capabilities/rights/provenance.json.

Usage:
  uv run python scripts/generate_catalog.py --write
  uv run python scripts/generate_catalog.py --check
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dictlib as dl  # noqa: E402


def classify_safety(rel_path):
    """Default safety classification based on path and content heuristics."""
    lowered = rel_path.lower()
    if "password" in lowered or "username" in lowered:
        return "optional"
    if "backup" in lowered or "api" in lowered:
        return "optional"
    return "safe"


def build_catalog():
    provenance = dl.load_provenance()
    file_prov = provenance.get("assets", [])
    accepted = {a["destination"]: a for a in file_prov if a.get("decision") == "accepted"}
    capabilities = []
    for rel, path in dl.iter_dict_files():
        prov = accepted.get(rel)
        if not prov:
            continue
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        capabilities.append({
            "id": dl.dict_file_id(rel),
            "kind": "dictionary",
            "path": rel,
            "contract": {
                "target_types": ["wordlist"],
                "inputs": [],
                "positive_evidence": "lines are candidate strings for the documented use",
                "negative_or_failure": "empty or malformed file",
                "interface_version": "dict-v1",
            },
            "safety": classify_safety(rel),
            "lifecycle": "active",
            "replacement": None,
            "provenance_id": prov["provenance_id"],
            "content_digest": prov["content_digest"],
            "components": [],
            "requires": [],
            "extensions": {
                "rbkd": {
                    "line_count": len(lines),
                    "encoding": "utf-8",
                    "use": _guess_use(rel),
                }
            },
        })
    return {
        "schema_version": 1,
        "repository": "dict",
        "capabilities": capabilities,
    }


def _guess_use(rel):
    mapping = {
        "username": "username-enumeration",
        "password": "password-spray",
        "path": "path-discovery",
        "api": "api-endpoint-discovery",
        "backup": "backup-file-discovery",
    }
    for prefix, use in mapping.items():
        if rel.startswith(prefix + "/"):
            return use
    return "general"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    catalog = build_catalog()
    catalog_path = dl.CAP_DIR / "catalog-v1.json"
    if args.write:
        dl.write_canonical(catalog_path, catalog)
        print(f"✓ wrote {catalog_path} ({len(catalog['capabilities'])} capabilities)")
        return 0
    expected = dl.canonical_json(catalog)
    actual = catalog_path.read_text(encoding="utf-8") if catalog_path.is_file() else ""
    if expected != actual:
        print("✗ catalog drift")
        return 1
    print("✓ catalog up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
