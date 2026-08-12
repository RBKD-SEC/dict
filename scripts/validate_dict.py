#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dict release gate validator (Ticket 04)

Checks every tracked .txt wordlist for:
  - UTF-8, LF line endings, no BOM, no NUL bytes
  - no trailing whitespace per line
  - no internal duplicate lines (ratchet baseline)
  - no leading '/' in path wordlists
  - no binary / unexpected encoding
  - catalog validates against schema and sidecar matches
  - basic secret scan (no private keys, aws keys, github tokens)

Usage:
  uv run python scripts/validate_dict.py [--all]
  exit 0 = passed, 1 = failed
"""
import argparse
import json
import re
import sys
from pathlib import Path

import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dictlib as dl  # noqa: E402

# Current baseline counts from initial audit (after cleanup)
DUPLICATE_BASELINES = {
    "password/top500.txt": 0,
    "path/top1000.txt": 0,
    "username/top500.txt": 0,
}
LEADING_SLASH_FILES = {
    "path/admin-panel-low-noise.txt",
    "path/src-low-noise.txt",
    "path/actuator.txt",
    "path/sensitive-files-low-noise.txt",
    "path/swagger.txt",
    "path/debug-low-noise.txt",
}


def _is_binary(path):
    sample = path.read_bytes()[:8192]
    return b"\x00" in sample


def check_format(rel, path, errors):
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeError as exc:
        errors.append(f"{rel}: not valid UTF-8 ({exc})")
        return
    if text.startswith("\ufeff"):
        errors.append(f"{rel}: BOM detected")
    if "\r" in text:
        errors.append(f"{rel}: CRLF detected")
    for i, line in enumerate(text.splitlines(), start=1):
        if line != line.rstrip():
            errors.append(f"{rel}:{i}: trailing whitespace")


def check_duplicates(rel, path, errors):
    lines = path.read_text(encoding="utf-8").splitlines()
    seen = set()
    dupes = 0
    for line in lines:
        if line in seen:
            dupes += 1
        seen.add(line)
    baseline = DUPLICATE_BASELINES.get(rel, 0)
    if dupes > baseline:
        errors.append(f"{rel}: duplicates increased from {baseline} to {dupes}")


def check_leading_slash(rel, path, errors):
    lines = path.read_text(encoding="utf-8").splitlines()
    leading = sum(1 for line in lines if line.startswith("/"))
    if rel in LEADING_SLASH_FILES:
        if leading != 0:
            errors.append(f"{rel}: leading '/' not cleaned ({leading} lines)")
    elif leading > 0:
        errors.append(f"{rel}: unexpected leading '/' on {leading} lines")


def check_catalog(errors):
    catalog_path = dl.CAP_DIR / "catalog-v1.json"
    schema_path = dl.CAP_DIR / "schema" / "catalog-v1.schema.json"
    if not catalog_path.is_file():
        errors.append("capabilities/catalog-v1.json missing")
        return
    if not schema_path.is_file():
        errors.append("capabilities/schema/catalog-v1.schema.json missing")
        return
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    for err in validator.iter_errors(catalog):
        path = ".".join(str(p) for p in err.absolute_path) or "(root)"
        errors.append(f"catalog schema: {path}: {err.message}")
    # sidecar
    sidecar = catalog_path.with_suffix(".json.sha256")
    if not sidecar.is_file():
        errors.append("catalog sidecar missing")
        return
    expected = dl.sha256_digest(catalog_path.read_text(encoding="utf-8"))
    actual = sidecar.read_text(encoding="utf-8").strip()
    if actual != expected:
        errors.append(f"catalog sidecar mismatch")


def check_secrets(rel, path, errors):
    text = path.read_text(encoding="utf-8", errors="replace")
    patterns = [
        ("private key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----")),
        ("aws key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
        ("github pat", re.compile(r"\bghp_[A-Za-z0-9]{36}\b")),
    ]
    for name, pat in patterns:
        if pat.search(text):
            errors.append(f"{rel}: potential {name} detected")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="include all .txt files")
    args = parser.parse_args()

    errors = []
    print("Validating dict gates...")
    for rel, path in dl.iter_dict_files():
        if _is_binary(path):
            errors.append(f"{rel}: appears binary")
            continue
        check_format(rel, path, errors)
        check_duplicates(rel, path, errors)
        check_leading_slash(rel, path, errors)
        check_secrets(rel, path, errors)
    check_catalog(errors)

    if errors:
        print(f"\n✗ {len(errors)} gate failure(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\n✓ All dict gates passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
