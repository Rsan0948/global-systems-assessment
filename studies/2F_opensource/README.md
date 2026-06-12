# Study 2F — Open-source forks (boundary probe)

Domain node for viable forks (a fork that itself passed a popularity threshold,
e.g. >100 stars) per parent project. `oss_node.build_node()`.

**Registered as a boundary probe, not a core confirmation.** Software has
near-zero marginal replication cost — a regime the theory predicts it should
*not* cleanly govern. Viable-fork counts are expected to be heavy-tailed
(preferential attachment), with high variance, plausibly *not* a tight law. The
trivial null here is the preferential-attachment process itself, so a
non-trivial result would require the observed concentration to *beat*
preferential attachment — the honest high bar for this domain.

**Data — no Crunchbase, no GHTorrent (defunct).** Use the **free** GitHub
REST/GraphQL API (rate-limited) or **GH Archive** (free bulk event data). Wire
via `oss_node.ingest_github`.

```bash
pytest tests/ -q
```
