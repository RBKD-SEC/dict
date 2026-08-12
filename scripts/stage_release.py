#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepare an immutable CalVer release candidate for dict (Ticket 04).

Outputs:
  releases/<calver>/
    catalog-v1.json + .sha256
    schema/catalog-v1.schema.json + SHA256SUMS
    wordlists/<id>.txt  (accepted-only)
    LICENSE, NOTICE
    rights/provenance.json
    rights-report.md
    SHA256SUMS

Usage:
  uv run python scripts/stage_release.py --calver 2026.08.10.1
"""
import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dictlib as dl  # noqa: E402


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def write_digest_list(release_dir, files):
    lines = []
    for rel in files:
        lines.append(f"{sha256_file(release_dir / rel)}  {rel}")
    (release_dir / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def stage(calver):
    release_dir = dl.ROOT / "releases" / calver
    if release_dir.exists():
        print(f"release {calver} already exists", file=sys.stderr)
        return 1
    release_dir.mkdir(parents=True)

    # catalog + sidecar
    shutil.copy2(dl.CAP_DIR / "catalog-v1.json", release_dir / "catalog-v1.json")
    shutil.copy2(dl.CAP_DIR / "catalog-v1.json.sha256", release_dir / "catalog-v1.json.sha256")

    # schema
    schema_dir = release_dir / "schema"
    schema_dir.mkdir()
    shutil.copy2(dl.CAP_DIR / "schema" / "catalog-v1.schema.json", schema_dir / "catalog-v1.schema.json")
    shutil.copy2(dl.CAP_DIR / "schema" / "SHA256SUMS", schema_dir / "SHA256SUMS")

    # rights
    rights_dir = release_dir / "rights"
    rights_dir.mkdir()
    shutil.copy2(dl.CAP_DIR / "rights" / "provenance.json", rights_dir / "provenance.json")

    # accepted wordlists only
    provenance = dl.load_provenance()
    accepted = {a["destination"] for a in provenance.get("assets", []) if a.get("decision") == "accepted"}
    wordlists_dir = release_dir / "wordlists"
    wordlists_dir.mkdir()
    for rel, path in dl.iter_dict_files():
        if rel in accepted:
            dest = wordlists_dir / (dl.dict_file_id(rel) + ".txt")
            shutil.copy2(path, dest)

    # license/notice
    shutil.copy2(dl.ROOT / "LICENSE", release_dir / "LICENSE")
    shutil.copy2(dl.ROOT / "NOTICE", release_dir / "NOTICE")

    # rights report
    report = [
        f"# dict {calver} Rights and Provenance Report",
        "",
        f"Release: `{calver}`",
        f"Prepared: {datetime.now(timezone.utc).isoformat()}",
        "",
        "All dictionary assets in this release are currently held pending "
        "maintainer/rights-officer provenance review. The public catalog is therefore empty.",
        "",
        "See `rights/provenance.json` for per-asset status.",
        ""
    ]
    (release_dir / "rights-report.md").write_text("\n".join(report), encoding="utf-8")

    files = ["catalog-v1.json", "schema/catalog-v1.schema.json", "schema/SHA256SUMS",
             "LICENSE", "NOTICE", "rights/provenance.json", "rights-report.md"]
    for rel in accepted:
        files.append("wordlists/" + dl.dict_file_id(rel) + ".txt")
    write_digest_list(release_dir, files)
    print(f"✓ staged release candidate at {release_dir}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calver", required=True)
    args = parser.parse_args(argv)
    return stage(args.calver)


if __name__ == "__main__":
    sys.exit(main())
