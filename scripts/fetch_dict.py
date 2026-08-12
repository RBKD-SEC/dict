#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch a dict capability by ID from a release candidate (Ticket 04).

Usage:
  uv run python scripts/fetch_dict.py --release releases/2026.08.10.1 --id username-top100 --output /tmp/username-top100.txt
"""
import argparse
import json
import sys
from pathlib import Path


def fetch(release_dir, cap_id, output):
    release_dir = Path(release_dir)
    catalog_path = release_dir / "catalog-v1.json"
    if not catalog_path.is_file():
        print(f"catalog not found: {catalog_path}", file=sys.stderr)
        return 1
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    matches = [c for c in catalog.get("capabilities", []) if c.get("id") == cap_id]
    if not matches:
        print(f"capability id not found: {cap_id}", file=sys.stderr)
        return 1
    cap = matches[0]
    src = release_dir / "wordlists" / (cap_id + ".txt")
    if not src.is_file():
        print(f"wordlist file not found: {src}", file=sys.stderr)
        return 1
    data = src.read_bytes()
    expected = cap.get("content_digest", "")
    if expected and expected.startswith("sha256:"):
        import hashlib
        actual = "sha256:" + hashlib.sha256(data).hexdigest()
        if actual != expected:
            print(f"digest mismatch for {cap_id}", file=sys.stderr)
            return 1
    Path(output).write_bytes(data)
    print(f"✓ fetched {cap_id} -> {output}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", required=True)
    parser.add_argument("--id", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    return fetch(args.release, args.id, args.output)


if __name__ == "__main__":
    sys.exit(main())
