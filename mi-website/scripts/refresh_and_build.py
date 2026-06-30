#!/usr/bin/env python3
"""
The data-collection pipeline — the chain that keeps the site a LIVING instrument.

  1. (best-effort) refresh the public source data from the upstream APIs
  2. run the validated MI engine over all available data
  3. publish the dataset the website reads (web/public/data/*)

Run locally:  python mi-website/scripts/refresh_and_build.py
On schedule:  .github/workflows/update-mi-data.yml runs this weekly, commits the
              regenerated dataset, and the push triggers a Vercel deploy.

The engine is the single source of truth; this only orchestrates refresh -> score -> publish.
Deterministic given fixed source data.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
MI_RESEARCH = ROOT / "mi-research"
PY = sys.executable


def run(cmd, cwd, *, optional=False, timeout=None):
    print(f"\n$ {' '.join(str(c) for c in cmd)}  (cwd={cwd.name})")
    try:
        r = subprocess.run(cmd, cwd=cwd, timeout=timeout)
    except subprocess.TimeoutExpired:
        if optional:
            print(f"  (optional step timed out after {timeout}s — continuing with existing data)")
            return False
        raise
    if r.returncode != 0:
        if optional:
            print(f"  (optional step failed rc={r.returncode} — continuing with existing data)")
            return False
        sys.exit(r.returncode)
    return True


def main():
    # 1. best-effort refresh of upstream source data (needs network; non-fatal in CI)
    refresh = MI_RESEARCH / "scripts" / "refresh_wgi_wdi.py"
    if refresh.exists():
        run([PY, str(refresh)], MI_RESEARCH, optional=True, timeout=300)
    else:
        print("refresh script not found — skipping refresh, rebuilding from committed sources")

    # 2 + 3. run the engine over all data and publish the site dataset
    run([PY, str(MI_RESEARCH / "scripts" / "build_site_dataset.py")], MI_RESEARCH)
    # 4. enrich with the T3 relational layer where we have it
    run([PY, str(MI_RESEARCH / "scripts" / "build_relational.py")], MI_RESEARCH)
    print("\n✓ pipeline complete — web/public/data refreshed.")


if __name__ == "__main__":
    main()
