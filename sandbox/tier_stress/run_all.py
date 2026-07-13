#!/usr/bin/env python3
"""One reproducible runner for the predictive-reach campaign.
Usage:
  python3 run_all.py           # integrity tests + full pipeline
  python3 run_all.py --quick   # skip the slow exhaustive search (combo_search)
Panels (predictors.json/outcomes.json) are prerequisites built by build_panels.py from the
sibling mi-research repo; they are committed in this dir, so the runner assumes they exist.
`test_harness.py` is a hard gate — if integrity fails, the pipeline aborts.
"""
import sys, subprocess, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
QUICK="--quick" in sys.argv

STAGES=[
 ("test_harness.py",     "integrity gate (leakage / determinism / panel fidelity)", True,  False),
 ("forward_screen.py",   "univariate predict-forward screen + confirmation split", False, False),
 ("forecast_test.py",    "autoregressive-baseline test (forecast vs persistence)", False, False),
 ("stack_screen.py",     "additive stacking + interactions",                       False, False),
 ("stack_validate.py",   "stacking replication across leads",                      False, False),
 ("combo_search.py",     "exhaustive combinatorial search (~21k subsets)",         False, True),
 ("calib.py",            "bootstrap CI + calibration of the stacked model",        False, False),
 ("relational_screen.py","relational/ratio features vs additive",                  False, False),
 ("relational_validate.py","relational replication + CIs",                         False, False),
 ("confirm_oot.py",      "OUT-OF-TIME confirmation (temporal holdout)",            False, False),
 ("robustness.py",       "rolling-origin / λ-sweep / placebo / threshold",         False, False),
]

def run(script):
    t=time.time()
    p=subprocess.run([sys.executable, str(HERE/script)], cwd=HERE)
    return p.returncode, time.time()-t

print(f"predictive-reach pipeline  ({'quick' if QUICK else 'full'})\n"+"="*60)
for script, desc, is_gate, slow in STAGES:
    if QUICK and slow:
        print(f"·· SKIP  {script:<24} ({desc}) [slow]"); continue
    print(f"\n▶ {script}  — {desc}")
    rc, dt = run(script)
    tag = "OK" if rc==0 else "FAIL"
    print(f"  [{tag}] {script} ({dt:.1f}s)")
    if is_gate and rc!=0:
        print("\nABORT: integrity gate failed — fix before trusting downstream results.")
        raise SystemExit(1)
print("\n"+"="*60+"\ndone. Findings: PREDICTION_LEDGER.md · confirmation: PREREG_BACKSLIDING.md")
