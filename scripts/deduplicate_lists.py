#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_FILES = (
    Path("domains/cistom.lst"),
    Path("subnets/custom.lst"),
)


def dedupe_file(path: Path, *, dry_run: bool) -> tuple[int, int, bool]:
    lines = path.read_text(encoding="utf-8").splitlines()
    deduped = sorted(set(lines))

    removed = len(lines) - len(deduped)
    changed = lines != deduped

    if changed and not dry_run:
        content = "\n".join(deduped)
        if content:
            content += "\n"

        path.write_text(content, encoding="utf-8")

    return len(lines), removed, changed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove duplicate lines from list files and sort them.",
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        default=DEFAULT_FILES,
        help="Files to dedupe. Defaults to domains/cistom.lst and subnets/custom.lst.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print stats without changing files.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit with code 1 if any file has duplicates or is not sorted.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dry_run = args.dry_run or args.check
    found_changes = False

    for path in args.files:
        total, removed, changed = dedupe_file(path, dry_run=dry_run)
        found_changes = found_changes or changed
        status = "changed" if changed else "ok"
        print(f"{path}: {total} lines, {removed} duplicates, {status}")

    if args.check and found_changes:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
