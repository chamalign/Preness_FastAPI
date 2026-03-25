#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path
from typing import Any, Optional

import httpx

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from app.services.not_auto_json_importer import (
    build_full_parts_payload,
    build_practice_part_payload_from_file,
    pick_unused_reading_file,
)


def _default_repo_root() -> Path:
    # scripts/ から 1 階層戻る
    return REPO_ROOT


def _read_api_key(api_key: Optional[str]) -> str:
    if api_key:
        return api_key
    env = os.getenv("CONTENT_SOURCE_API_KEY", "").strip()
    if not env:
        raise SystemExit("CONTENT_SOURCE_API_KEY is required (pass --api-key or set env).")
    return env


def _post_json(*, base_url: str, api_key: str, endpoint: str, payload: dict, timeout_s: float = 300.0) -> Any:
    url = base_url.rstrip("/") + endpoint
    headers = {"Authorization": f"Bearer {api_key}"}
    with httpx.Client(timeout=timeout_s) as client:
        resp = client.post(url, headers=headers, json=payload)
    try:
        return resp.json()
    except Exception:
        return {"status_code": resp.status_code, "text": resp.text}


def cmd_import_full_mock(args: argparse.Namespace) -> None:
    repo_root = _default_repo_root()
    set_dir = Path(args.set_dir)
    if not set_dir.is_absolute():
        set_dir = repo_root / set_dir

    payload = build_full_parts_payload(set_dir, kind="full")
    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    out = _post_json(
        base_url=args.base_url,
        api_key=_read_api_key(args.api_key),
        endpoint="/api/v1/import/full_mock",
        payload=payload,
    )
    print(out)


def cmd_import_short_mock(args: argparse.Namespace) -> None:
    repo_root = _default_repo_root()
    set_dir = Path(args.set_dir)
    if not set_dir.is_absolute():
        set_dir = repo_root / set_dir

    payload = build_full_parts_payload(set_dir, kind="short")
    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    out = _post_json(
        base_url=args.base_url,
        api_key=_read_api_key(args.api_key),
        endpoint="/api/v1/import/short_mock",
        payload=payload,
    )
    print(out)


def cmd_import_practice(args: argparse.Namespace) -> None:
    repo_root = _default_repo_root()
    short_dir = repo_root / "NOT_auto_json" / "Excecise" / "Reading_Short"
    long_dir = repo_root / "NOT_auto_json" / "Excecise" / "Reading_Long"

    if args.reading_random:
        rng = random.Random(args.seed) if args.seed is not None else random.Random()
        record_path = (
            Path(args.used_record).resolve()
            if args.used_record
            else None
        )
        if record_path is not None and not record_path.is_absolute():
            record_path = repo_root / record_path

        chosen = pick_unused_reading_file(
            reading_short_dir=short_dir,
            reading_long_dir=long_dir,
            repo_root=repo_root,
            record_path=record_path,
            rng=rng,
            allow_all_if_exhausted=args.allow_all_if_exhausted,
            mark_used=not args.dry_run,
        )
        part_payload = build_practice_part_payload_from_file(chosen)
    else:
        if not args.file:
            raise SystemExit("Either --file or --reading-random must be specified.")
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = repo_root / file_path
        part_payload = build_practice_part_payload_from_file(file_path)

    if args.dry_run:
        print(json.dumps(part_payload, ensure_ascii=False, indent=2))
        return

    out = _post_json(
        base_url=args.base_url,
        api_key=_read_api_key(args.api_key),
        endpoint="/api/v1/import/practice",
        payload=part_payload,
    )
    print(out)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NOT_auto_json txt -> FastAPI import payload + POST")
    parser.add_argument("--base-url", default=os.getenv("BASE_URL", "http://127.0.0.1:8000"))
    parser.add_argument("--api-key", default=None, help="CONTENT_SOURCE_API_KEY (or set env)")
    parser.add_argument("--dry-run", action="store_true", help="payload JSON を出して POST しない")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_full = sub.add_parser("import-full-mock", help="POST /api/v1/import/full_mock")
    p_full.add_argument("set_dir", nargs="?", default="NOT_auto_json/Full_Mock")
    p_full.set_defaults(func=cmd_import_full_mock)

    p_short = sub.add_parser("import-short-mock", help="POST /api/v1/import/short_mock")
    p_short.add_argument("set_dir", nargs="?", default="NOT_auto_json/Short_Mock")
    p_short.set_defaults(func=cmd_import_short_mock)

    p_practice = sub.add_parser("import-practice", help="POST /api/v1/import/practice")
    p_practice.add_argument("--file", default=None, help="part txt file path (for listening/grammar/reading)")
    p_practice.add_argument("--reading-random", action="store_true", help="Reading_Short/Long から unused をランダム選択")
    p_practice.add_argument("--seed", type=int, default=None, help="random seed")
    p_practice.add_argument(
        "--used-record",
        default=None,
        help="used_reading record path (default outputs/used_reading.json)",
    )
    p_practice.add_argument(
        "--allow-all-if-exhausted",
        action="store_true",
        help="unused が尽きた場合でも全候補から選ぶ",
    )
    p_practice.set_defaults(func=cmd_import_practice)

    return parser


def main(argv: list[str]) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])

