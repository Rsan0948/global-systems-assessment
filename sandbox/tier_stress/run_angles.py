#!/usr/bin/env python3
"""Runner for the deep angles + capacity arsenal (the extension past run_all.py).
`python3 run_angles.py` runs all; `--quick` skips the slow ones (angle1/2/3). Integrity gate first."""
import sys, subprocess, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
QUICK="--quick" in sys.argv
STAGES=[
 ("test_harness.py",        "integrity + unit + regression gate", True,  False),
 ("deep_time.py",           "deep-time horizon sweep",            False, False),
 ("deep_horizon.py",        "fine horizon / fast-slow crossover", False, False),
 ("deep_democratization.py","capacity->democratization shift",    False, False),
 ("deep_cohort_test.py",    "third-wave prospective test",        False, False),
 ("deep_audit.py",          "adversarial audit",                  False, False),
 ("angle1_dynamic.py",      "A1 dynamic/rates (null)",            False, True),
 ("angle2_within.py",       "A2 within-country (real)",           False, True),
 ("angle3_contagion.py",    "A3 contagion (null)",                False, True),
 ("angle4_attributes.py",   "A4 attributes (capacity dominates)", False, False),
 ("angle5_survival.py",     "A5 survival/hazard",                 False, False),
 ("angle6_nonlinear.py",    "A6 nonlinear (inverted-U)",          False, False),
 ("capacity_arsenal.py",    "capacity arsenal (0.746)",           False, False),
 ("capacity_relational.py", "relational-vs-additive boundary",    False, False),
]
print(f"deep-angles pipeline ({'quick' if QUICK else 'full'})\n"+"="*56)
for script,desc,gate,slow in STAGES:
    if QUICK and slow: print(f"·· SKIP  {script}  [slow]"); continue
    t=time.time(); rc=subprocess.run([sys.executable,str(HERE/script)],cwd=HERE,
                                      stdout=subprocess.DEVNULL if not gate else None).returncode
    print(f"  [{'OK' if rc==0 else 'FAIL'}] {script:26} ({time.time()-t:.0f}s)")
    if gate and rc!=0: print("ABORT: integrity gate failed."); raise SystemExit(1)
print("="*56+"\ndone. Findings: PREDICTION_LEDGER.md · FINAL_REPORT.md")
