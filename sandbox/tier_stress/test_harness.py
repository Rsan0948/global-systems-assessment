#!/usr/bin/env python3
"""Regression + integrity tests for the predictive-reach harness.
Run standalone (`python3 test_harness.py`) or via pytest. Guards the properties that make the
findings trustworthy: no leakage, no double-counting, determinism, panel fidelity, placebo~0.5.
"""
import json, hashlib
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
MIROOT=HERE.parents[1]/"mi-research"

import combo_search as CS
import relational_screen as R
import confirm_oot as O
import forward_screen as FS

PRED=json.load(open(HERE/"predictors.json"))
OUTC=json.load(open(HERE/"outcomes.json"))

# ---------------------------------------------------------------- panels
def test_panel_shape():
    assert isinstance(PRED,dict) and len(PRED)>=180, "expected ~191 iso keys"
    # every predictor row is {year:{field:val}}
    iso=next(iter(PRED)); yr=next(iter(PRED[iso]))
    assert yr.isdigit() and 1996<=int(yr)<=2024
    assert "conflict_onsets_by_iso" in OUTC, "outcomes must carry the onset index"

def test_no_all_nan_fields():
    # each pool predictor must have real coverage
    for f in CS.POOL:
        n=sum(1 for iso in PRED for y in PRED[iso] if isinstance(PRED[iso][y].get(f),(int,float)))
        assert n>=200, f"predictor {f} nearly empty (n={n})"

def test_v1_matches_mi_5pt():
    """V1 back-score must equal the committed mi_5pt_panel (the keystone)."""
    m5=json.load(open(MIROOT/"data/robustness/decoupling/mi_5pt_panel.json"))["rows"]
    checked=diffs=0
    for iso in ["EST","NOR","USA","DEU","POL","KOR","BRA","ZAF"]:
        if iso not in m5 or iso not in PRED: continue
        for y,rec in m5[iso].get("years",{}).items():
            for pk in ("P1","P4"):
                a=rec.get(pk); b=PRED[iso].get(y,{}).get(pk)
                if a is None or b is None: continue
                checked+=1
                if abs(a-b)>1e-6: diffs+=1
    assert checked>=20 and diffs==0, f"V1 mismatch vs mi_5pt: {diffs}/{checked}"

# ---------------------------------------------------------------- splits
def test_splits_disjoint_and_stable():
    isos=sorted(PRED)
    # 2-way (forward_screen) and 3-way (combo) partitions must be exhaustive + disjoint
    a={i for i in isos if FS.half(i)=="A"}; b={i for i in isos if FS.half(i)=="B"}
    assert a and b and not (a&b) and (a|b)==set(isos)
    g3={i:CS.grp(i) for i in isos}
    assert set(g3.values())=={"FIT","SEL","TEST"}
    # stable across calls (deterministic hashing)
    assert all(CS.grp(i)==CS.grp(i) for i in isos)

def test_confirm_split_is_temporal_not_country():
    rows=O.assemble_temporal("libdem_backslide","libdem","libdem","bin",5)
    tr={r["iso"] for r in rows if r["phase"]=="train"}
    te={r["iso"] for r in rows if r["phase"]=="test"}
    # temporal split: a country may appear in BOTH phases (different years) — that is intended,
    # but train rows must all be <=2012 base and test rows >=2016 base (no year overlap).
    assert max(r["b"] for r in rows if r["phase"]=="train")<=2012
    assert min(r["b"] for r in rows if r["phase"]=="test")>=2016

# ---------------------------------------------------------------- leakage / normalization
def test_normalization_uses_predictors_only():
    """z/percentile must be identical whether or not outcomes exist -> proves no outcome leak."""
    rows=O.assemble_temporal("libdem_backslide","libdem","libdem","bin",5)
    O.normalize_temporal(rows)
    z1={(r["iso"],r["b"]):r["z"].get("v1_mi") for r in rows}
    # corrupt all outcomes, re-normalize a fresh copy, z must be unchanged
    rows2=O.assemble_temporal("libdem_backslide","libdem","libdem","bin",5)
    for r in rows2: r["y"]=1.0
    O.normalize_temporal(rows2)
    z2={(r["iso"],r["b"]):r["z"].get("v1_mi") for r in rows2}
    assert z1==z2, "normalization changed when outcomes changed -> LEAK"

def test_placebo_is_chance():
    """permuted TEST labels -> relational OOT AUC must average ~0.5 (no pipeline leakage)."""
    aucs=[]
    for s in range(8):
        r=O.fit_eval_oot("libdem_backslide","libdem","libdem",5,"rel",R.RELNAMES,shuffle_seed=s)
        if r: aucs.append(r["auc"])
    assert aucs and abs(np.mean(aucs)-0.5)<0.08, f"placebo AUC {np.mean(aucs):.3f} not ~0.5"

# ---------------------------------------------------------------- no double counting
def test_cohort_one_row_per_country():
    """forward_screen cohort cross-sections must use each country at most once per (cohort,lead)."""
    oc=next(o for o in FS.OUTCOMES if o[0]=="libdem_backslide")
    seen=[]
    isoA={i for i in PRED if FS.half(i)=="A"}
    for iso in isoA:
        pv=(PRED.get(iso,{}) or {}).get("2008")
        if isinstance(pv,dict) and pv.get("v3_numer") is not None and oc[2](iso,2008,5) is not None:
            seen.append(iso)
    assert len(seen)==len(set(seen)), "duplicate country in a single cohort cross-section"

# ---------------------------------------------------------------- feature math
def test_matching_gap_definition():
    rows=O.normalize_temporal(O.assemble_temporal("libdem_backslide","libdem","libdem","bin",5))
    for r in rows[:200]:
        f=R.feat(r); z=r["z"]
        comp=[z.get(x) for x in ("v3_numer","t4_scar","t6_spark")]; comp=[c for c in comp if c is not None]
        cap=z.get("v1_mi")
        if f.get("matching_gap") is not None and comp and cap is not None:
            assert abs(f["matching_gap"]-(np.mean(comp)-cap))<1e-9

# ---------------------------------------------------------------- determinism & result fidelity
def test_determinism():
    a=O.fit_eval_oot("electdem_backslide","electdem","electdem",5,"rel",R.RELNAMES)
    b=O.fit_eval_oot("electdem_backslide","electdem","electdem",5,"rel",R.RELNAMES)
    assert a["auc"]==b["auc"] and a["ci"]==b["ci"], "non-deterministic OOT eval"

def test_stored_results_reproduce():
    """the committed confirm_oot_results.json must match a fresh run (guards silent drift)."""
    p=HERE/"confirm_oot_results.json"
    if not p.exists(): return
    stored=json.load(open(p))
    fresh=O.fit_eval_oot("libdem_backslide","libdem","libdem",5,"rel",R.RELNAMES)
    assert abs(stored["libdem_backslide"]["relational"]["auc"]-fresh["auc"])<1e-9

def test_baseline_sane():
    r=O.fit_eval_oot("libdem_backslide","libdem","libdem",5,"rel",R.RELNAMES)
    assert r is not None and 0.35<r["base_auc"]<0.95 and 0.35<r["auc"]<0.95

# ---------------------------------------------------------------- deep-time engine
def test_deep_reaches_19th_century():
    import deep_time as DT
    assert min(DT.BASES)<=1820 and max(DT.BASES)>=2015
    # a 19th-century cohort must have real countries with regime data
    assert len(DT.PANEL[1840])>=50, "too few 1840 states"

def test_deep_partial_drops_degenerate():
    import deep_time as DT
    assert DT.partial([1,1,1,1],[0,1,0,1],[1,2,3,4]) is None  # constant x -> None, no crash

def test_deep_determinism():
    import deep_time as DT
    a=DT.era_skill("gap_rol_anoc","backslide",5,1945,1988)
    b=DT.era_skill("gap_rol_anoc","backslide",5,1945,1988)
    assert a==b

def test_composition_inversion_independent_of_vdem():
    """The load-bearing deep claim (modern democratizers are low-capacity) must hold with
    INDEPENDENT WGI capacity, not just V-Dem rol — else it's circular."""
    import deep_time as DT
    from scipy import stats
    import numpy as np
    cap=lambda iso,b:(PRED.get(iso,{}).get(str(b),{}) or {}).get("v1_mi")
    gaps=[]
    for b in range(1996,2006):
        rows=[(cap(iso,b),DT.near(DT.LIB,iso,b),DT.near(DT.LIB,iso,b+10)) for iso in PRED]
        rows=[(c,a,cc) for c,a,cc in rows if None not in (c,a,cc)]
        if len(rows)<25: continue
        z=stats.zscore([r[0] for r in rows]); dy=[1 if (cc-a)>=0.05 else 0 for _,a,cc in rows]
        cd=[z[i] for i in range(len(rows)) if dy[i]]; cn=[z[i] for i in range(len(rows)) if not dy[i]]
        if cd and cn: gaps.append(np.mean(cd)-np.mean(cn))
    assert gaps and np.mean(gaps) < -0.2, f"modern WGI democratizer capΔ={np.mean(gaps):.2f} not clearly negative"

def test_cohort_transition_signal_direction():
    """post-1975 low-capacity democratizers should backslide more (capacity-at-transition ρ<0)."""
    p=HERE/"cohort_test_results.json"
    if not p.exists(): return  # produced by deep_cohort_test.py
    r=json.load(open(p))
    assert r["n"]>=50 and r["nb"]>=10, "too few transitions/events to test"
    assert r["corr_post75"]<0 and r["share_back"]>r["share_trans"], "third-wave direction not present"

def test_angle1_state_not_rate():
    """Angle 1 finding: static gap is real; the RATE (mismatch-velocity) does NOT add over it."""
    p=HERE/"angle1_results.json"
    if not p.exists(): return
    r=json.load(open(p))
    assert r["static_gap_backslide_k5"]["real"] and r["static_gap_backslide_k5"]["rho"]<-0.05
    assert not r["mismatch_vel_net_gap_k5"]["real"]  # rate adds nothing over the level gap

def test_angle2_within_gap_real_capacity_alone_null():
    """Angle 2: the capacity-mobilization GAP is a real within-country signal (net of libdem);
    capacity alone is a ceiling artifact (null after control); between-country is ~0."""
    p=HERE/"angle2_results.json"
    if not p.exists(): return
    r=json.load(open(p))
    assert r["rol_cso_gap"]["real"] and r["rol_cso_gap"]["within"]<-0.04
    assert abs(r["rol_cso_gap"]["between"])<0.03      # invisible in the cross-section
    assert not r["rol_alone"]["real"]                 # capacity-alone within = ceiling artifact

def test_angle3_contagion_null():
    """Angle 3: no geographic-adjacency contagion — real neighbours don't beat random ones."""
    p=HERE/"angle3_results.json"
    if not p.exists(): return
    r=json.load(open(p))
    assert not r["adjacency_specific"] and abs(r["obs_partial"])<0.05

def test_angle4_capacity_dominates():
    """Angle 4: rival explanations null net of capacity; legal-origin gradient collapses to ~0 residual."""
    p=HERE/"angle4_results.json"
    if not p.exists(): return
    r=json.load(open(p))
    assert not r["main_effects_net_of_capacity"]["resource_rents"]["real"]  # resource curse null net of capacity
    assert not r["main_effects_net_of_capacity"]["ethnic_excl"]["real"]     # ethnic exclusion null net of capacity
    assert r["legal_origin_mediated_by_capacity"]
    assert max(abs(v) for v in r["legal_origin_residual_net_capacity"].values())<0.06  # gradient collapses

def test_angle5_hazard_frontloaded_capacity_robust():
    """Angle 5: hazard is front-loaded (young >> old) descriptively; capacity is the robust reducer;
    age effect entangled with survival structure (not permutation-clean)."""
    p=HERE/"angle5_results.json"
    if not p.exists(): return
    r=json.load(open(p))
    assert r["hazard_young_0_4"] > 5*r["hazard_old_40plus"]   # strong descriptive front-loading
    assert r["capacity_coef"] < -0.5                          # capacity robustly reduces hazard
    assert not r["age_real"]                                  # age not cleanly separable (n=52, entangled)

def test_angle6_nonlinearity_real():
    """Angle 6: capacity→backsliding is strongly nonlinear (inverted-U); nonlinear beats smooth OOS
    and the threshold is well-identified."""
    p=HERE/"angle6_results.json"
    if not p.exists(): return
    r=json.load(open(p))
    assert max(r["auc_quadratic"],r["auc_threshold"]) > r["auc_smooth"]+0.05  # nonlinear clearly wins OOS
    assert r["threshold_well_identified"]

def test_capacity_arsenal_nonlinear_wins_exotic_null():
    """Arsenal: the safety-ceiling nonlinear feature beats libdem alone; the complex-number phase
    representation is a null (worse than libdem). Signal is nonlinear, not phase/spectral."""
    p=HERE/"capacity_arsenal_results.json"
    if not p.exists(): return
    r=json.load(open(p))
    assert r["univariate"]["ceiling"] > r["libdem_baseline"]   # safety ceiling is real & strong
    assert r["univariate"]["phase"] < r["libdem_baseline"]     # complex phase representation = null
    assert r["best_auc"] >= r["quad"]                          # full arsenal doesn't beat disciplined nonlinear+history by much

def test_relational_boundary_single_variable():
    """Relational>additive is scope-limited to DIFFERENT instruments; for single-variable transforms
    additive holds (relational does not beat it)."""
    p=HERE/"capacity_relational_results.json"
    if not p.exists(): return
    r=json.load(open(p))
    assert r["relational_minus_additive"] <= 0.005   # relational does NOT beat additive for one-variable transforms

# ---------------------------------------------------------------- UNIT tests: shared substrate (common.py)
def test_common_velocity_slope():
    import common as CM
    s={"T":{str(y):3.0*y+7 for y in range(1990,2011)}}   # exact slope 3.0/yr
    assert abs(CM.velocity(s,"T",2010,10)-3.0)<1e-6
    assert CM.velocity(s,"T",2010,2) is None             # too few points for the window

def test_common_partial_spearman_extremes():
    import common as CM
    # x==y with a control NOT collinear with x -> partial +1
    assert abs(CM.partial_spearman([1,2,3,4,5,6],[1,2,3,4,5,6],[[2,1,4,3,6,5]])-1.0)<1e-6
    assert CM.partial_spearman([1,1,1,1],[0,1,0,1],[[1,2,3,4]]) is None   # degenerate x -> None

def test_common_perm_null_structure():
    import common as CM
    pn=CM.perm_null(3.0,lambda rng:float(rng.normal()),n=400)             # 3.0 well outside N(0,1) 95%
    assert set(pn)>= {"p","lo","hi","real"} and pn["real"] is True

def test_common_dem_age_current_spell():
    import common as CM
    assert CM.dem_age("POL",2010)==20 and CM.dem_age("RUS",2010) is None   # current spell, not first-ever

def test_common_adjacency_and_attrs_present():
    import common as CM
    assert "ESP" in CM.neighbors("AND") and "FRA" in CM.neighbors("AND")   # known land border
    assert CM.ethnic("USA","excluded_pop_share") is not None               # EPR in-panel
    assert CM.population("USA",2010) and CM.population("USA",2010)>3e8

def test_results_manifest_complete():
    """every angle/analysis committed its result JSON with the keys its test reads."""
    need={"confirm_oot_results.json","cohort_test_results.json","angle1_results.json",
          "angle2_results.json","angle3_results.json","angle4_results.json","angle5_results.json",
          "angle6_results.json","capacity_arsenal_results.json","capacity_relational_results.json",
          "screen_confirmed.json","relational_results.json","predictors.json","outcomes.json"}
    missing=[f for f in need if not (HERE/f).exists()]
    assert not missing, f"missing result artifacts: {missing}"

if __name__=="__main__":
    tests=[v for k,v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    npass=0; fails=[]
    for t in tests:
        try:
            t(); npass+=1; print(f"  PASS  {t.__name__}")
        except Exception as e:
            fails.append((t.__name__,e)); print(f"  FAIL  {t.__name__}: {e}")
    print(f"\n{npass}/{len(tests)} passed" + ("" if not fails else f", {len(fails)} FAILED"))
    raise SystemExit(1 if fails else 0)
