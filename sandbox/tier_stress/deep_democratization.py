#!/usr/bin/env python3
"""WHY did the slow capacity->democratization channel die after ~1945?
Two hypotheses, discriminated on the deep panel (imports deep_time):
  (H1 CEILING/CENSORING) high-capacity states became already-democratic -> can't democratize more.
  (H2 DECOUPLING) modern democratization went exogenous/wave-driven -> hits low-capacity states too.
Decisive test: among states with ROOM to democratize (libdem<0.5), does rol still predict it?
  H1 => signal REVIVES among low-baseline states.  H2 => stays dead even there.
Plus: rol-libdem coupling over time, prior-capacity of democratizers, and timing-synchrony (waves).
Generational horizon k=20. Descriptive, AR/persistence-aware."""
import numpy as np
from scipy import stats
import deep_time as DT

def rolz(iso,b):
    d=DT.ZPANEL[b].get(iso); return d[1].get("rol") if d else None
def lib(iso,b): return DT.near(DT.LIB,iso,b)
def dem(iso,b,k):
    a,c=DT.near(DT.LIB,iso,b),DT.near(DT.LIB,iso,b+k)
    return None if a is None or c is None else (1.0 if (c-a)>=0.05 else 0.0)

def partial(x,y,z):
    x,y,z=map(lambda a:np.array(a,float),(x,y,z))
    rx,ry,rz=stats.rankdata(x),stats.rankdata(y),stats.rankdata(z)
    Z=np.column_stack([np.ones(len(x)),rz]); ex=rx-Z@np.linalg.lstsq(Z,rx,rcond=None)[0]
    ey=ry-Z@np.linalg.lstsq(Z,ry,rcond=None)[0]
    return None if np.std(ex)<1e-9 or np.std(ey)<1e-9 else float(stats.pearsonr(ex,ey).statistic)

def era_stats(e0,e1,k):
    couplings=[]; frac_sat=[]; rho_all=[]; rho_room=[]; rates=[]; demgap=[]; yr_dummies=[]; yr_y=[]
    for b in DT.BASES:
        if not (e0<=b<=e1): continue
        rows=[(iso,rolz(iso,b),lib(iso,b),dem(iso,b,k)) for iso,_ in DT.PANEL[b]]
        rows=[r for r in rows if None not in r]
        if len(rows)<25: continue
        rz=[r[1] for r in rows]; lb=[r[2] for r in rows]; dy=[r[3] for r in rows]
        if len(set(dy))<2: continue
        couplings.append(stats.spearmanr(rz,lb).statistic)
        thr=np.percentile(rz,66.7); hi=[l for z,l in zip(rz,lb) if z>=thr]
        if hi: frac_sat.append(np.mean([l>0.5 for l in hi]))
        pa=partial(rz,dy,lb)
        if pa is not None: rho_all.append(pa)
        room=[(z,d,l) for z,l,d in zip(rz,lb,dy) if l<0.5]
        if len(room)>=20 and len(set(d for _,d,_ in room))>=2:
            pr=partial([z for z,_,_ in room],[d for _,d,_ in room],[l for _,_,l in room])
            if pr is not None: rho_room.append(pr)
        # prior-capacity gap: mean rol-z of (future) democratizers minus non-democratizers
        dz=[z for z,d in zip(rz,dy) if d==1]; nz=[z for z,d in zip(rz,dy) if d==0]
        if dz and nz: demgap.append(np.mean(dz)-np.mean(nz))
        rates.append(np.mean(dy))
        for d in dy: yr_dummies.append(b); yr_y.append(d)
    if yr_y and len(set(yr_dummies))>1:
        yb=np.array(yr_y); grp=np.array(yr_dummies); gm=np.array([yb[grp==g].mean() for g in grp])
        waveR2=1-np.sum((yb-gm)**2)/np.sum((yb-yb.mean())**2) if np.var(yb)>0 else 0
    else: waveR2=float('nan')
    m=lambda a: np.mean(a) if a else float('nan')
    return dict(coup=m(couplings),sat=m(frac_sat),rho_all=m(rho_all),rho_room=m(rho_room),
               rate=m(rates),wave=waveR2,demgap=m(demgap))

for K in [10,20]:
    print(f"\n{'='*104}\nGenerational horizon k={K}.  ρ = mean per-cohort partial(rol, democratize | libdem).")
    print("="*104)
    print(f"{'era':20} | {'corr(rol,lib)':>13} {'%hiCap already dem':>18} | {'ρ ALL':>7} {'ρ if lib<0.5':>12} {'demr̄izer capΔ':>14} | {'demr̄':>6} {'waveR²':>6}")
    print("-"*118)
    for elab,e0,e1 in DT.ERAS:
        s=era_stats(e0,e1,K)
        print(f"{elab:20} | {s['coup']:>+13.2f} {s['sat']*100:>17.0f}% | {s['rho_all']:>+7.2f} {s['rho_room']:>+12.2f} {s['demgap']:>+14.2f} | {s['rate']:>6.2f} {s['wave']:>6.2f}")

print("\nReading:")
print("  ρ ALL fades era to era (the puzzle).  If ρ(lib<0.5) ALSO fades -> H2 DECOUPLING (capacity")
print("  stopped selecting who democratizes).  If ρ(lib<0.5) stays strong -> H1 CENSORING (capacity")
print("  still drives it among those with room; pooled fade is just saturation).")
print("  corr(rol,lib)↑ and %hiCap-already-dem↑ across eras = the saturation mechanism.")
print("  wave R²↑ = democratization increasingly synchronized in time (exogenous waves).")
