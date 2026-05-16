#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_FILES = (
    Path("domains/cistom.lst"),
    Path("subnets/custom.lst"),
)


def dedupe_file(path: Path, *, dry_run: bool) -> tuple[int, int]:
    lines = path.read_text(encoding="utf-8").splitlines()

    seen: set[str] = set()
    deduped: list[str] = []

    for line in lines:
        if line in seen:
            continue

        seen.add(line)
        deduped.append(line)

    removed = len(lines) - len(deduped)

    if removed and not dry_run:
        path.write_text("\n".join(deduped) + "\n", encoding="utf-8")

    return len(lines), removed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove duplicate lines from list files while preserving first occurrence order.",
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
        help="Exit with code 1 if any duplicates are found.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dry_run = args.dry_run or args.check
    found_duplicates = False

    for path in args.files:
        total, removed = dedupe_file(path, dry_run=dry_run)
        found_duplicates = found_duplicates or removed > 0
        print(f"{path}: {total} lines, {removed} duplicates")

    if args.check and found_duplicates:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
