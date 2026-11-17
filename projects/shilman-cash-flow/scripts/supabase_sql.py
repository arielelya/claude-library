#!/usr/bin/env python3
"""Run SQL against the Cash Flow production Supabase project (fzwxcaidvaweczxwvljk).

Usage (from shilman-cash-flow/):
  python3 .claude/scripts/supabase_sql.py --sql "select 1"
  python3 .claude/scripts/supabase_sql.py --file supabase/migrations/X.sql --sql "select ..."

Steps run in the order given and stop at the first error (exit code 1).
The Management API token is read from the macOS Keychain item
`supabase-management-token` and is never printed.

This is production. There is no staging database. Follow the db-change skill.
"""
import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request

PROJECT_REF = "fzwxcaidvaweczxwvljk"
ENDPOINT = f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query"


def token() -> str:
    try:
        return subprocess.check_output(
            ["security", "find-generic-password", "-s", "supabase-management-token", "-w"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except subprocess.CalledProcessError:
        sys.exit("Keychain item supabase-management-token is missing")


def run(sql: str, auth: str, timeout: int):
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps({"query": sql}).encode(),
        headers={"Authorization": f"Bearer {auth}", "Content-Type": "application/json", "User-Agent": "curl/8.4.0"},
        method="POST",
    )
    try:
        return True, json.loads(urllib.request.urlopen(request, timeout=timeout).read().decode() or "null")
    except urllib.error.HTTPError as error:
        return False, f"HTTP {error.code}: {error.read().decode()[:2000]}"
    except Exception as error:  # network errors, timeouts
        return False, f"{type(error).__name__}: {error}"


class Step(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        steps = getattr(namespace, "steps", None) or []
        steps.append((option_string.lstrip("-"), value))
        namespace.steps = steps


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sql", action=Step, help="SQL text to run")
    parser.add_argument("--file", action=Step, help="SQL file to run exactly as written")
    parser.add_argument("--timeout", type=int, default=300, help="Seconds per step (default 300)")
    parser.add_argument("--out", help="Write the first value of the last step's first row to this file, as raw text")
    args = parser.parse_args()
    steps = getattr(args, "steps", None)
    if not steps:
        parser.error("give at least one --sql or --file")

    auth = token()
    result = None
    for index, (kind, value) in enumerate(steps, 1):
        sql = open(value, encoding="utf-8").read() if kind == "file" else value
        label = value if kind == "file" else " ".join(value.split())[:100]
        print(f"== [{index}] {kind}: {label}")
        ok, result = run(sql, auth, args.timeout)
        if not ok:
            print(f"   ERROR {result}")
            sys.exit(1)
        if isinstance(result, list):
            for row in result:
                print(f"   {json.dumps(row, ensure_ascii=False, default=str)}")
            if not result:
                print("   (no rows)")
        else:
            print(f"   {json.dumps(result, ensure_ascii=False, default=str)}")

    if args.out:
        if not (isinstance(result, list) and result and isinstance(result[0], dict)):
            sys.exit("--out: the last step returned no row")
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(str(next(iter(result[0].values()))))
        print(f"== wrote {args.out}")


if __name__ == "__main__":
    main()
