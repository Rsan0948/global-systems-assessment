# Study 2E — Organizational scaling

Domain node for the inter-echelon scaling ratio of human organizations — how
many sub-units aggregate into the next level (squad→platoon→company; small
teams→departments). `org_node.build_node()`.

**Honest caveat (in code too):** organizations are *partly designed*
(span-of-control doctrine), so this domain sits between self-organizing and
engineered. It stays in the ladder, but its trivial null is a span-of-control
prior (Graicunas ~5–6); the organizational signal counts only if it departs
from that.

**Data (all free):** publicly downloadable doctrine manuals (e.g. US Army FM
7-0) for military inter-echelon ratios across countries/eras, plus published
team-performance meta-analysis tables (Hackman, Wheelan, Mueller) and Dunbar's
social-brain data.

```bash
pytest tests/ -q
```
