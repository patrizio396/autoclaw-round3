# Supplier Purchase Terms & Receiving Discrepancy Log (Redacted Source Extract)

**Entity:** [REDACTED_ENTITY] | **Window:** 90 days, 2026-08-20 through 2026-11-18 | **Extract prepared:** 2026-11-19
**Basis:** simulated redacted extracts of the purchase-term summaries and the POS receiving module underlying `smb_operations_audit.md`. All identifiers are redacted (`[REDACTED_ENTITY]`, `[REDACTED_AMOUNT]`); SKU-level unit costs, quantities and percentages are visible so every downstream figure reconciles. These extracts reconcile to CHK-04 (cost-creep set) and CHK-15 (redaction scan) in `compute_metrics.py`.

---

## 1. Contractual purchase terms per supplier (as signed)

| Supplier | SKUs | Agreed Payment Terms | Price-Change Notice Clause | MOQ (units) | Quoted Lead Time |
|---|---|---|---|---|---|
| [REDACTED_ENTITY]_A | 001, 003, 008 | Net 30 (SKU-003: Net 45) | 30-day written notice + Buyer's written approval required | 60 / 30 / 36 | 12-18 days |
| [REDACTED_ENTITY]_B | 002, 005, 006 | Net 15 | 30-day written notice + Buyer's written approval required | 48 / 40 / 50 | 4-10 days |
| [REDACTED_ENTITY]_C | 004, 009, 012 | Net 60 | 30-day written notice + Buyer's written approval required | 24 / 36 / 24 | 15-21 days |
| [REDACTED_ENTITY]_D | 007, 010, 011 | Net 30 (SKU-011: Net 45) | 30-day written notice + Buyer's written approval required | 20 / 20 / 12 | 25-30 days |

**Standard clause text (all four supplier agreements):**
> "Supplier shall provide thirty (30) days' advance written notice and obtain Buyer's written approval before any change to the agreed unit costs. Absent such notice and approval, the prior agreed unit cost remains binding for all shipments."

---

## 2. Receiving & invoice discrepancy log (events breaching the clause)

| Log ID | Date | Supplier | PO | SKU | Event | Clause Impact | Cost Impact (90d) |
|---|---|---|---|---|---|---|---|
| RCL-01 | 2026-09-12 | [REDACTED_ENTITY]_C | PO-1004 | SKU-004 | Receipt/invoice shows unit cost 16.90 vs contracted 14.20; no written notice on file | 30-day notice + written approval NOT obtained | +2.70/unit; 466 units consumed → $1,258.20 |
| RCL-02 | 2026-10-03 | [REDACTED_ENTITY]_C | PO-1009 | SKU-009 | Receipt/invoice shows unit cost 7.45 vs contracted 6.30; no written notice on file | Breach | +1.15/unit; 731 units consumed → $840.65 |
| RCL-03 | 2026-09-28 | [REDACTED_ENTITY]_B | PO-1002 | SKU-002 | Receipt/invoice shows unit cost 5.55 vs contracted 5.40; notice absent from Buyer records | Breach | +0.15/unit; 1,606 units consumed → $240.90 |

All other receipts in the window matched contracted unit costs; the full receiving log is retained in the POS receiving module. Annual spend per supplier is tracked in the buying office ledger at `[REDACTED_AMOUNT]` granularity and is not reproduced here.

---

## 3. Discrepancy disposition (owner actions per the audit)

- **[REDACTED_ENTITY]_C:** formal Price-Lock & Rebate Notice issued (audit Section 4.1) requesting rollback to prior unit costs or a retroactive rebate of $2,098.85, plus a 180-day written price lock.
- **[REDACTED_ENTITY]_B:** price-lock letter issued requesting rollback of SKU-002 to 5.40 or a $240.90 credit on future invoices.
- **[REDACTED_ENTITY]_A / _D:** no cost-clause breaches recorded; terms and claim-policy actions follow audit Section 3.3 and the Negotiation Playbook Matrix (Section 3.5).
