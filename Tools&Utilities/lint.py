"""
lint_fix.py

Auto-fixes linting issues across a repo. Exits 1 only if issues remain
that need a human. Missing tools are skipped with a warning.

Usage:
  python lint_fix.py [--path DIR] [--langs python,go,...] [--check-only] [-v]

Supported: python (ruff, isort)
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def tool_available(name):
    if shutil.which(name) is not None:
        return True
    r = subprocess.run([sys.executable, "-m", name, "--version"], capture_output=True)
    return r.returncode == 0


def cmd_for(name):
    if shutil.which(name) is not None:
        return [name]
    return [sys.executable, "-m", name]


def run(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def fix_python(root, check_only, verbose):
    if not tool_available("ruff"):
        print("[WARNING] ruff not found, skipping Python")
        return 0

    ruff = cmd_for("ruff")
    if check_only:
        run(ruff + ["check", str(root)])
        run(ruff + ["format", "--check", str(root)])
    else:
        run(ruff + ["check", "--fix", str(root)])
        run(ruff + ["format", str(root)])
        if tool_available("isort"):
            run(cmd_for("isort") + [str(root)])

    result = run(ruff + ["check", str(root)])
    if verbose and result.stdout:
        print(result.stdout)
    return result.returncode


def fix_javascript(root, check_only, verbose):
    rc = 0
    if tool_available("eslint"):
        cmd = cmd_for("eslint") + ([] if check_only else ["--fix"]) + [str(root)]
        r = run(cmd)
        if verbose and r.stdout:
            print(r.stdout)
        rc = max(rc, r.returncode)
    else:
        print("[WARNING] eslint not found, skipping JS/TS")

    if tool_available("prettier"):
        glob = "**/*.{js,ts,jsx,tsx,css,scss,json,html}"
        cmd = cmd_for("prettier") + ["--check" if check_only else "--write", "--glob", glob]
        r = run(cmd, cwd=str(root))
        if verbose and r.stdout:
            print(r.stdout)
        rc = max(rc, r.returncode)
    else:
        print("[WARNING] prettier not found, skipping JS/TS formatting")

    return rc


def fix_go(root, check_only, verbose):
    if not tool_available("gofmt"):
        print("[WARNING] gofmt not found, skipping Go")
        return 0

    rc = 0
    for f in root.rglob("*.go"):
        r = run(["gofmt", "-l" if check_only else "-w", str(f)])
        if check_only and r.stdout.strip():
            if verbose:
                print(f"[needs fmt] {r.stdout.strip()}")
            rc = 1
    return rc


def fix_rust(root, check_only, verbose):
    if not tool_available("rustfmt"):
        print("[WARNING] rustfmt not found, skipping Rust")
        return 0

    rc = 0
    for f in root.rglob("*.rs"):
        cmd = ["rustfmt", "--edition", "2021"] + (["--check"] if check_only else []) + [str(f)]
        r = run(cmd)
        if verbose and r.stderr:
            print(r.stderr)
        rc = max(rc, r.returncode)
    return rc


def fix_markdown(root, check_only, verbose):
    if not tool_available("markdownlint-cli2"):
        print("[WARNING] markdownlint-cli2 not found, skipping Markdown")
        return 0

    cmd = cmd_for("markdownlint-cli2") + ([] if check_only else ["--fix"]) + ["**/*.md"]
    r = run(cmd, cwd=str(root))
    if verbose and r.stdout:
        print(r.stdout)
    return r.returncode


FIXERS = {
    "python":     fix_python,
    "javascript": fix_javascript,
    "go":         fix_go,
    "rust":       fix_rust,
    "markdown":   fix_markdown,
}

EXT_MAP = {
    ".py": "python", ".js": "javascript", ".ts": "javascript",
    ".jsx": "javascript", ".tsx": "javascript",
    ".go": "go", ".rs": "rust", ".md": "markdown",
}


def detect_languages(root):
    found = set()
    for ext, lang in EXT_MAP.items():
        if any(root.rglob(f"*{ext}")):
            found.add(lang)
    return sorted(found)


def main():
    parser = argparse.ArgumentParser(description="Auto-fix linting issues across a repo.")
    parser.add_argument("--path", default=".", help="Project root (default: cwd)")
    parser.add_argument("--langs", default="", help="e.g. python,go  (auto-detected if omitted)")
    parser.add_argument("--check-only", action="store_true", help="Report issues without fixing")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show tool output")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"[ERROR] Path not found: {root}")
        return 2

    if args.langs:
        langs = [l.strip().lower() for l in args.langs.split(",") if l.strip()]
        invalid = [l for l in langs if l not in FIXERS]
        if invalid:
            print(f"[ERROR] Unknown language(s): {', '.join(invalid)}. Options: {', '.join(FIXERS)}")
            return 2
    else:
        langs = detect_languages(root)
        if not langs:
            print("[INFO] No supported files found.")
            return 0
        print(f"[INFO] Detected: {', '.join(langs)}")

    failed = []
    for lang in langs:
        print(f"\n[INFO] Running {lang}...")
        rc = FIXERS[lang](root, args.check_only, args.verbose)
        if rc != 0:
            failed.append(lang)

    print()
    if failed:
        print(f"[FAIL] Unfixable issues in: {', '.join(failed)} — needs manual review")
        return 1
    print("[OK] All issues resolved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())