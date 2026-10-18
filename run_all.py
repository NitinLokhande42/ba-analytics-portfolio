"""Generate synthetic data and run the analysis for every project in the portfolio."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

failures = []
for proj in sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name[:2].isdigit()):
    print(f"\n{'=' * 70}\n{proj.name}\n{'=' * 70}")
    scripts = [proj / "data" / "generate_data.py"] + sorted((proj / "src").glob("*.py"))
    for s in scripts:
        if not s.exists() or s.name.startswith("_"):
            continue
        r = subprocess.run([sys.executable, str(s)], cwd=ROOT)
        if r.returncode != 0:
            failures.append(str(s.relative_to(ROOT)))

print("\nAll projects ran successfully." if not failures else f"\nFailed: {failures}")
sys.exit(1 if failures else 0)
