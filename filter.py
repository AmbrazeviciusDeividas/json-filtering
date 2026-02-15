#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Any, Dict, Iterable, Tuple

def record_matches(rec: Dict[str, Any]) -> bool:
    t = rec.get("[ Match any field which have strin... (just add the field for example 't') ]")
    if isinstance(t, str) and "strin..." in t:
        return True

    for v in rec.values():
        if isinstance(v, str) and "strin2...." in v.lower():
            return True

    return False

def iter_jsonl(path: str) -> Iterable[Tuple[int, Dict[str, Any]]]:
    with open(path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict):
                    yield lineno, obj
            except json.JSONDecodeError:
                yield lineno, {"__parse_error__": True, "__raw__": line}


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Filter JSON records that contain X Y Z  or any string field containing 'STRING' and output to additional JSON."
    )
    ap.add_argument("input")
    ap.add_argument("-o", "--output", default="filterd.json")
    ap.add_argument("--include-line-number", action="store_true")
    ap.add_argument("--skip-parse-errors", action="store_true")
    args = ap.parse_args()

    matched = []
    total = 0
    parse_errors = 0

    for lineno, rec in iter_jsonl(args.input):
        total += 1

        if rec.get("__parse_error__"):
            parse_errors += 1
            if args.skip_parse_errors:
                continue
            continue

        if record_matches(rec):
            if args.include_line_number:
                rec = dict(rec)
                rec["__line__"] = lineno
            matched.append(rec)

    with open(args.output, "w", encoding="utf-8") as out:
        json.dump(matched, out, ensure_ascii=False, indent=2)

    print(f"Lines I read: {total}")
    print(f"Errors: {parse_errors}")
    print(f"It's a Match: {len(matched)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
