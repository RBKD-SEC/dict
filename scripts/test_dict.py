#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dict gate tests (Ticket 04)

Covers:
  - catalog generation respects accepted/held provenance
  - wordlist format validation
  - duplicate detection
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dictlib as dl  # noqa: E402
import generate_catalog  # noqa: E402
import validate_dict  # noqa: E402

PASS = 0
FAIL = 0


def case(name, fn):
    global PASS, FAIL
    try:
        fn()
        PASS += 1
        print(f"  ✓ {name}")
    except Exception as exc:
        FAIL += 1
        print(f"  ✗ {name}: {exc}")


def t_held_asset_not_in_catalog():
    provenance = {
        "assets": [
            {"destination": "username/top100.txt", "decision": "held",
             "provenance_id": "prov-dict-00000000", "content_digest": "sha256:" + "0" * 64}
        ]
    }
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        dl.ROOT = tmp
        dl.CAP_DIR = tmp / "capabilities"
        (tmp / "username").mkdir()
        (tmp / "username" / "top100.txt").write_text("admin\nroot\n", encoding="utf-8")
        (dl.CAP_DIR / "schema").mkdir(parents=True)
        (dl.CAP_DIR / "rights").mkdir(parents=True)
        json.dump({"$schema": "..."}, (dl.CAP_DIR / "schema" / "catalog-v1.schema.json").open("w"))
        (dl.CAP_DIR / "rights" / "provenance.json").write_text(json.dumps(provenance), encoding="utf-8")
        generate_catalog.build_catalog()
        catalog_path = dl.CAP_DIR / "catalog-v1.json"
        # build_catalog doesn't write; main does
        generate_catalog.main(["--write"])
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        assert catalog["capabilities"] == []


def t_duplicate_detection():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        path = tmp / "test.txt"
        path.write_text("a\nb\na\nc\n", encoding="utf-8")
        errors = []
        validate_dict.check_duplicates("test.txt", path, errors)
        assert any("duplicates" in e for e in errors), "should detect duplicates"


def t_leading_slash_detection():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        path = tmp / "test.txt"
        path.write_text("/admin\n/login\n", encoding="utf-8")
        errors = []
        validate_dict.check_leading_slash("path/test.txt", path, errors)
        assert any("leading" in e for e in errors), "should detect leading slash"


def main():
    cases = [
        ("held asset excluded from catalog", t_held_asset_not_in_catalog),
        ("duplicate detection", t_duplicate_detection),
        ("leading slash detection", t_leading_slash_detection),
    ]
    print("dict gate tests")
    for name, fn in cases:
        case(name, fn)
    print()
    print(f"结果：{PASS} 通过，{FAIL} 失败，共 {PASS + FAIL} 项")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
