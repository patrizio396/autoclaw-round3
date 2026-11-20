# Sample Fixture 01 — Authorized Baseline (`PASS`)

> Sanitized fixture for **ScopeGuard Audit Studio**. Organizations, personnel, hosts and financial figures are replaced with `[REDACTED_ENTITY]` / `[REDACTED_AMOUNT]`; all infrastructure uses RFC 5737 documentation ranges (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24). Safe to publish, share and commit.

## Scenario

A multi-agent recon plan performs a strictly read-only baseline assessment. Every queued action stays inside `api.[REDACTED_ENTITY]` or the authorized `192.0.2.0/24` documentation range, respects the 60 rpm per-host rate cap, and runs inside the authorized window (Mon–Fri 09:00–17:00 UTC). This is the "everything correct" control case: the engine must approve the plan with a perfect score.

## Scope & Policy (fenced DSL consumed by the engine)

```scope
# Authorized Scope & Policy — Preset 1: Authorized Baseline
# Engagement [REDACTED_ENTITY] — read-only web/API baseline assessment
# Compensation ceiling: [REDACTED_AMOUNT] per signed terms

INCLUSION   api.[REDACTED_ENTITY]
INCLUSION   192.0.2.0/24
EXCLUSION   (none declared)
ALLOW       GET HEAD OPTIONS
RATE-LIMIT  60 rpm per host
WINDOW      Mon-Fri 09:00-17:00 UTC
NOTES       Baseline posture: everything must stay inside the two inclusion entries.
```

## Proposed Multi-Agent Action Queue

```queue
# Proposed Multi-Agent Action Queue — Preset 1
A1 | GET | https://api.[REDACTED_ENTITY]/v1/health | rate=1 | at=2026-11-19T14:00:00Z | agent=recon-alpha | notes=Health endpoint reachability probe
A2 | GET | https://192.0.2.10/api/v1/users?page=1 | rate=5 | at=2026-11-19T14:05:00Z | agent=recon-alpha | notes=Read-only pagination sweep of the user directory listing
A3 | HEAD | https://api.[REDACTED_ENTITY]/v1/version | rate=1 | at=2026-11-19T14:10:00Z | agent=recon-beta | notes=Version banner check with no payload
A4 | GET | https://192.0.2.55/status | rate=2 | at=2026-11-19T14:15:00Z | agent=recon-beta | notes=Node status read inside the authorized CIDR block
```

## Expected Pipeline Outcome

| Metric | Expected value |
|---|---|
| Compliance Score | 100/100 |
| Risk Exposure Index | 0/100 |
| Executive Verdict | APPROVED |
| Findings | 4 PASS / 0 WARN_HUMAN_REVIEW / 0 BLOCK_VIOLATION |

Every action must satisfy all eight policy rules (`POL-01`..`POL-08`).

## Rule walkthrough (why each action passes)

- **A1** — hostname `api.[REDACTED_ENTITY]` is an explicit inclusion entry (`POL-01` ok), no exclusions apply (`POL-02` ok), no IP to contain (`POL-03` n/a), GET is non-destructive (`POL-04` ok), 1 rpm ≤ 60 (`POL-05` ok), Thursday 14:00 UTC is inside the window (`POL-06` ok), no sensitive intent (`POL-07` ok), GET is allow-listed (`POL-08` ok).
- **A2** — IP literal 192.0.2.10 is contained in 192.0.2.0/24 (`POL-01`/`POL-03` ok by exact subnet-containment math), 5 rpm within cap, timestamp inside window.
- **A3, A4** — same posture as A1/A2; HEAD is allow-listed and read-only.

## Verification hooks

This fixture is asserted verbatim by `CHK-01` in `verify_engine.py` and by `J-CHK-01` in the in-app self-test log. Load it in the UI as **Preset 1 — Authorized Baseline**.
