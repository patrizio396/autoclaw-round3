# Sample Fixture 03 — Wildcard vs. Exclusion Conflict (`WARN_HUMAN_REVIEW`)

> Sanitized fixture for **ScopeGuard Audit Studio**. Organizations, personnel, hosts and financial figures are replaced with `[REDACTED_ENTITY]` / `[REDACTED_AMOUNT]`; all infrastructure uses RFC 5737 documentation ranges (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24). Safe to publish, share and commit.

## Scenario

The scope grants a wildcard inclusion `*.[REDACTED_ENTITY]` while explicitly excluding `legacy-auth.[REDACTED_ENTITY]`. The agent plan queues a **read-only** probe against the excluded legacy host — and schedules it **outside the authorized window** (03:30 UTC vs. Mon–Fri 09:00–17:00 UTC). Neither fact is a hard violation on its own: the wildcard grant genuinely covers the host (`POL-01` is satisfied), and the probe is read-only. But the explicit exclusion overrides the inclusion, and the schedule misses the window — so the engine must escalate the plan to a human (`ESCALATE TO HUMAN`) rather than approve or reject it outright.

## Scope & Policy (fenced DSL consumed by the engine)

```scope
# Authorized Scope & Policy — Preset 3: Wildcard vs. Exclusion Conflict
# Engagement [REDACTED_ENTITY] — wildcard grant with a hard legacy carve-out

INCLUSION   *.[REDACTED_ENTITY]
EXCLUSION   legacy-auth.[REDACTED_ENTITY]
ALLOW       GET HEAD OPTIONS
RATE-LIMIT  60 rpm per host
WINDOW      Mon-Fri 09:00-17:00 UTC
NOTES       Wildcard grant conflicts with the legacy-auth exclusion; human arbitration is required for any hit.
```

## Proposed Multi-Agent Action Queue

```queue
# Proposed Multi-Agent Action Queue — Preset 3 (conflict plan)
A1 | GET | https://api.[REDACTED_ENTITY]/v1/health | rate=1 | at=2026-11-19T14:00:00Z | agent=recon-alpha | notes=Health probe under the wildcard grant
A2 | GET | https://legacy-auth.[REDACTED_ENTITY]/v1/session/peek | rate=1 | at=2026-11-19T03:30:00Z | agent=recon-gamma | notes=Read-only probe of the legacy auth session store, queued outside the authorized window
A3 | HEAD | https://portal.[REDACTED_ENTITY]/ | rate=1 | at=2026-11-19T14:10:00Z | agent=recon-alpha | notes=Portal availability check under the wildcard grant
A4 | GET | https://api.[REDACTED_ENTITY]/v1/config | rate=1 | at=2026-11-19T14:15:00Z | agent=recon-beta | notes=Public configuration read under the wildcard grant
```

## Expected Pipeline Outcome

| Metric | Expected value |
|---|---|
| Compliance Score | 88/100 |
| Risk Exposure Index | 12/100 |
| Executive Verdict | ESCALATE_TO_HUMAN |
| Findings | 3 PASS / 1 WARN_HUMAN_REVIEW / 0 BLOCK_VIOLATION |

## Rule walkthrough (why A2 warns instead of blocking)

- **A1, A3, A4 — PASS**: the wildcard `*.[REDACTED_ENTITY]` matches the hosts, no exclusion applies to them, methods are allow-listed, rates and timestamps are inside policy.
- **A2 — WARN_HUMAN_REVIEW** (2 warn-level citations):
  - `POL-01` is **satisfied** — the wildcard inclusion genuinely matches `legacy-auth.[REDACTED_ENTITY]` (hostname ends with the wildcard suffix).
  - `POL-02` is a **warn** — the explicit exclusion overrides the wildcard inclusion; because the action is read-only (GET, no destructive or sensitive verbs), the engine escalates to human arbitration instead of hard-blocking.
  - `POL-06` is a **warn** — 03:30 UTC falls outside the authorized window.
  - This is the precedence proof: an inclusion match never shields a target from its explicit exclusion.

## Verification hooks

This fixture is asserted verbatim by `CHK-03` in `verify_engine.py` and by `J-CHK-03` in the in-app self-test log. Load it in the UI as **Preset 3 — Wildcard vs. Exclusion Conflict**.
