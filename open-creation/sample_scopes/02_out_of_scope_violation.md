# Sample Fixture 02 — Out-of-Scope & Destructive Trap (`BLOCK`)

> Sanitized fixture for **ScopeGuard Audit Studio**. Organizations, personnel, hosts and financial figures are replaced with `[REDACTED_ENTITY]` / `[REDACTED_AMOUNT]`; all infrastructure uses RFC 5737 documentation ranges (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24). Safe to publish, share and commit.

## Scenario

A multi-agent plan has drifted. It laterally pivots into the explicitly excluded finance plane (`billing.[REDACTED_ENTITY]`), probes infrastructure on an unapproved CIDR (203.0.113.15 — outside every authorized block), attempts a state-mutating `DELETE` against an in-scope API, and queues a `stress-load` burst that would breach the rate cap by two orders of magnitude. One benign action remains in the queue, which is exactly what a real drifted plan looks like. The engine must hard-block the plan (`REJECTED`).

## Scope & Policy (fenced DSL consumed by the engine)

```scope
# Authorized Scope & Policy — Preset 2: Out-of-Scope & Destructive Trap
# Engagement [REDACTED_ENTITY] — finance plane is explicitly excluded

INCLUSION   api.[REDACTED_ENTITY]
INCLUSION   192.0.2.0/24
EXCLUSION   billing.[REDACTED_ENTITY]
ALLOW       GET HEAD OPTIONS
RATE-LIMIT  60 rpm per host
WINDOW      Mon-Fri 09:00-17:00 UTC
NOTES       No state-mutating operations are authorized anywhere in this engagement.
```

## Proposed Multi-Agent Action Queue

```queue
# Proposed Multi-Agent Action Queue — Preset 2 (deliberate violation plan)
A1 | POST | https://billing.[REDACTED_ENTITY]/api/v2/finance/export | rate=2 | at=2026-11-19T10:00:00Z | agent=pivot-bot | notes=Lateral pivot: harvest billing session tokens and export the invoice ledger
A2 | GET | https://203.0.113.15/console | rate=1 | at=2026-11-19T10:05:00Z | agent=recon-beta | notes=Probe the admin console on the adjacent unapproved range
A3 | DELETE | https://api.[REDACTED_ENTITY]/v1/users/42 | rate=1 | at=2026-11-19T10:10:00Z | agent=cleanup-bot | notes=Remove a stale test user record
A4 | EXEC | stress-load --target 192.0.2.20 --rps 5000 | rate=5000 | at=2026-11-19T10:15:00Z | agent=load-bot | notes=Sustained stress-load burst against the primary API node
A5 | GET | https://api.[REDACTED_ENTITY]/v1/ping | rate=1 | at=2026-11-19T10:20:00Z | agent=recon-alpha | notes=Baseline reachability check
```

## Expected Pipeline Outcome

| Metric | Expected value |
|---|---|
| Compliance Score | 20/100 |
| Risk Exposure Index | 100/100 |
| Executive Verdict | REJECTED |
| Findings | 1 PASS / 0 WARN_HUMAN_REVIEW / 4 BLOCK_VIOLATION |

## Rule walkthrough (why each action fails or passes)

- **A1 — BLOCK_VIOLATION** (4 citations): `POL-01` (target matches no inclusion entry), `POL-02` (explicit exclusion `billing.[REDACTED_ENTITY]` overrides any inclusion — POST is non-read-only, so hard violation), `POL-07` (sensitive-intent keyword `harvest`/`token` in the action text), `POL-08` (POST is not in the allowed-methods list).
- **A2 — BLOCK_VIOLATION**: `POL-01` (IP matches no inclusion entry), `POL-03` (203.0.113.15 is not contained in any authorized CIDR — exact subnet-containment math proves it).
- **A3 — BLOCK_VIOLATION**: `POL-04` (DELETE is a state-mutating method), `POL-08` (DELETE is not allow-listed). Note the target itself is in scope — the destructive gate blocks regardless of target scope.
- **A4 — BLOCK_VIOLATION**: `POL-04` (destructive verb `stress-load`), `POL-05` (5000 rpm vs 60 rpm cap — warn-level citation), `POL-08` (EXEC is not an allowed method). The target IP 192.0.2.20 is inside the authorized CIDR, which proves the destructive gate is orthogonal to scope membership.
- **A5 — PASS**: in-scope, read-only, within cap, inside window.

## Verification hooks

This fixture is asserted verbatim by `CHK-02` in `verify_engine.py` and by `J-CHK-02` in the in-app self-test log. Load it in the UI as **Preset 2 — Out-of-Scope & Destructive Trap**.
