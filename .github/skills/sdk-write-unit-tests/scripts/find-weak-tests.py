#!/usr/bin/env python3
"""List tests whose only assertions are weak (non-null, non-empty, truthy, status).

Usage: python3 find-weak-tests.py <file-or-dir> [...]
Scans .NET [Fact]/[Theory] methods in *.cs and pytest test_* functions in *.py.
Exit code 1 when any weak test is found.
"""

import re
import sys
from pathlib import Path

# A test is "weak" when it has assertions and every one of them matches the *_WEAK pattern.
CS_ASSERT = re.compile(r"\bAssert\.\w+")
CS_WEAK = re.compile(r"\bAssert\.(NotNull|NotEmpty|True\([^,]*!= null|False\(string\.IsNullOrEmpty)")
PY_ASSERT = re.compile(r"^\s*assert\b|pytest\.raises|assert_endpoint_responds\(")
PY_WEAK = re.compile(
    r"^\s*assert\s+(\w[\w.\[\]\"']*\s+is not None|\w[\w.]*$|hasattr\("
    r"|len\([^)]*\)\s*>\s*0|[\w.]*status_code\s*==\s*200)"
    r"|assert_endpoint_responds\("
)


def cs_tests(text: str):
    # Split on test attributes; each chunk runs until the next attribute or end of class.
    parts = re.split(r"\n\s*\[(?:Fact|Theory)[^\]]*\]", text)
    for part in parts[1:]:
        name = re.search(r"(?:void|Task)\s+(\w+)\s*\(", part)
        yield (name.group(1) if name else "?"), part


def py_tests(text: str):
    for match in re.finditer(r"^def (test_\w+)\(.*?(?=^def |^@|\Z)", text, re.M | re.S):
        yield match.group(1), match.group(0)


def weak(body: str, assert_re, weak_re) -> bool:
    lines = [line for line in body.splitlines() if assert_re.search(line)]
    return bool(lines) and all(weak_re.search(line) for line in lines)


def main(paths: list[str]) -> int:
    found = 0
    files = []
    for p in map(Path, paths):
        files += [p] if p.is_file() else [*p.rglob("*.cs"), *p.rglob("*.py")]
    for f in sorted(files):
        if f.name.startswith("_") or "/Fakes/" in f.as_posix() or f.name == "conftest.py":
            continue
        text = f.read_text(encoding="utf-8-sig")
        if f.suffix == ".cs":
            tests, assert_re, weak_re = cs_tests(text), CS_ASSERT, CS_WEAK
        else:
            tests, assert_re, weak_re = py_tests(text), PY_ASSERT, PY_WEAK
        for name, body in tests:
            if weak(body, assert_re, weak_re):
                print(f"{f}: {name}")
                found += 1
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["."]))
