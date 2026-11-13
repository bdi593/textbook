"""Fail if any notebook under content/ is too large, has saved errors,
or exposes a local file path in its outputs.

Uses only the standard library so it runs without installing anything.
Run from the repository root: python .github/scripts/check_notebooks.py
"""

import json
import re
import sys
from pathlib import Path

MAX_MB = 5.0
# Windows user folders, and Linux/macOS home folders that are not part of a URL.
LOCAL_PATH = re.compile(
    r"([A-Za-z]:\\\\[Uu]sers\\\\|(?<![\w.])/home/[a-z0-9_.-]+/|(?<![\w.])/Users/[A-Za-z0-9_.-]+/)"
)

problems = []
for path in sorted(Path("content").rglob("*.ipynb")):
    if ".ipynb_checkpoints" in path.parts:
        continue
    size_mb = path.stat().st_size / 1e6
    if size_mb > MAX_MB:
        problems.append(
            f"{path}: {size_mb:.1f} MB (limit {MAX_MB} MB). "
            "Aggregate data before plotting instead of embedding every row."
        )
    nb = json.loads(path.read_text(encoding="utf-8"))
    for i, cell in enumerate(nb.get("cells", [])):
        for out in cell.get("outputs", []):
            if out.get("output_type") == "error":
                problems.append(
                    f"{path}: cell {i} has a saved error ({out.get('ename')}). "
                    "Fix the cell and re-run the notebook."
                )
            match = LOCAL_PATH.search(json.dumps(out))
            if match:
                problems.append(
                    f"{path}: cell {i} output contains a local path ({match.group(0)}). "
                    "Fix the warning or error that prints it and re-run."
                )

if problems:
    print("Notebook check failed:")
    for p in problems:
        print(f"  - {p}")
    sys.exit(1)
print("Notebook check passed.")
