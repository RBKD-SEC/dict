#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Secret / PII scan for dict wordlists (Ticket 04).

Distinguishes between intentional weak passwords/usernames and real secret
patterns (private keys, AWS keys, GitHub PATs, email addresses).

Usage:
  uv run python scripts/secret_scan.py --tree .
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dictlib as dl  # noqa: E402

PATTERNS = [
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github-pat", re.compile(r"\bghp_[A-Za-z0-9]{36}\b")),
    ("generic-token", re.compile(r"\b(?:api[_-]?key|apikey|token|secret)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,}[\"']?", re.IGNORECASE)),
]


def scan(root):
    findings = []
    root = Path(root)
    for rel, path in dl.iter_dict_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for name, pat in PATTERNS:
                if pat.search(line):
                    findings.append((rel, lineno, name, line[:80]))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tree", default=".", help="root directory to scan")
    args = parser.parse_args(argv)
    findings = scan(args.tree)
    if findings:
        print(f"✗ {len(findings)} potential secret/PII finding(s):")
        for rel, lineno, name, snippet in findings:
            print(f"  [{name}] {rel}:{lineno}: {snippet}")
        return 1
    print("✓ No obvious secret/PII patterns detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
