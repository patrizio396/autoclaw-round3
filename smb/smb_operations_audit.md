# Operations Audit - [REDACTED_ENTITY] Specialty Retail (90-Day Simulation)

**Prepared:** 2026-11-19 | **Period:** trailing 90 days ending 2026-11-18 | **Currency:** USD, tax-exclusive
**Scope:** 12 SKUs across 4 suppliers (`[REDACTED_ENTITY]_A..D`, referenced below as supplier A/B/C/D), one specialty store plus an e-commerce storefront.
**Basis:** simulated, sanitized datasets in `data/` (see `README.md`). Per the compliance rules, business name, supplier identities, store locations, personnel, emails and macro revenue/bank totals are replaced by `[REDACTED_ENTITY]` / `[REDACTED_AMOUNT]`; SKU-level unit prices, unit costs, quantities, lead times and percentages are retained unredacted so every figure below is auditable. All metrics are deterministically computed and cross-checked - see Section 5 and `verification/`.

---

## 1. Executive Scorecard & Cash-Release Summary

| Metric | Current Baseline (90d) | Post-Optimization Target | Delta / Impact |
|---|---|---|---|
| Blended net margin % (after returns + shrinkage) | **48.88%** | **50.44%** (50.84% with renegotiation upside) | +1.56 to +1.96 pp |
| SKU-level contribution profit (pre-overhead, 90d) | **$76,595.50** | **$80,888.91** (up to $81,541.31) | +$4,293.41 to +$4,945.81 |
| Unapproved supplier cost creep (active drag) | **$2,339.75** per 90d | $0 via price-lock + rebate | +$2,339.75 per 90d (+1.49 pp blended) |
| Dead-stock trapped working capital | **$8,015.00** | $0 | **$11,817.05** cash recovered in <= 30 days |
| Annual carrying cost on dead stock | **$2,548.00** | $0 | -$2,548.00 / year |
| SKUs below reorder point | **4 of 12** | 0 | ~$25,669.20 pipeline revenue secured; $2,213.67 per cycle of projected lost sales avoided |
| Shrinkage cost (90d) | **$2,286.70** | ~$1,893.19 (-30% on SKU-005/006/007) | +$393.51 per 90d |

**Cash-release summary (first 30 days).** Tiered liquidation of the two dead/slow SKUs returns **$11,817.05** (66.5% of their $17,770.00 retail value; $3,802.05 above the $8,015.00 cost basis) and removes **$2,548.00/year** of carrying cost. That broadly self-funds the $12,058.80 replenishment program in Section 3.1. Repricing SKU-004/009 plus the SKU-002 cost rollback add **$3,899.90** per 90d at constant volumes; the shrinkage SOP adds **$393.51**. Total base uplift: **+$4,293.41 per 90d** (~$17.2k annualized run-rate).

**Top findings**

1. **Silent cost creep:** unapproved unit-cost increases on 3 SKUs from supplier B and supplier C (+2.8% to +19.0%) were never passed to retail: **-$2,339.75 per 90d, -1.49 pp of blended margin**. At prior supplier costs the blended margin would be 50.37%.
2. **Shrinkage concentration:** perishable/fragile SKUs 005/006/007 account for **$1,311.70 of the $2,286.70 total (57.4%)**, with shrinkage rates up to 8.9% of units sold.
3. **Trapped working capital:** $8,015.00 sits in two dead/slow SKUs (SKU-010: 75 days since last sale; SKU-011: 142.1 days of supply) generating no sales and costing $2,548.00/year to hold.
4. **Stockout exposure on the highest-margin replenished SKUs:** SKU-002 (52.08% net margin) and SKU-008 (57.02%) are projected to run dry inside their lead times; SKU-004 and SKU-007 are already below reorder point.
5. **Two repricing actions:** SKU-004 (41.60% net margin) and SKU-009 (44.19%) after unapproved cost increases of +19.0% and +18.3%.

---

## 2. SKU Profitability, Cost Creep & Shrinkage Diagnostic Table

Method: net margin nets returns on the revenue side and charges shrinkage on the cost side, exactly per the formula in Section 5.1. "Margin (Prior Cost)" restates each SKU at its pre-increase unit cost. Net profit is SKU-level contribution (pre-overhead). Returns total 237 units (3.0% of units sold), concentrated on perishables (SKU-005 4.9%, SKU-006 5.4%); shrinkage totals 248 units (3.1%).

| SKU | Category | Retail $ | Units Sold | Returns | Shrinkage | Net Revenue $ | Net Profit $ | Margin (Prior Cost) | Margin (Current Cost) | Shrinkage Drag $ (pp) | Cost Creep $ / 90d | Action Tag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SKU-001 | Gourmet Coffee Whole Bean | 18.50 | 1,240 | 22 | 18 | 22,533.00 | 10,204.60 | 45.29% | 45.29% | 176.40 (0.78 pp) | 0.00 | HOLD |
| SKU-002 | Single-Origin Craft Chocolate | 12.00 | 1,580 | 30 | 26 | 18,600.00 | 9,686.70 | 53.37% | 52.08% | 144.30 (0.78 pp) | 240.90 | REORDER NOW (+RENEGOTIATE) |
| SKU-003 | Specialty Loose-Leaf Tea | 24.00 | 520 | 12 | 8 | 12,192.00 | 6,278.40 | 51.50% | 51.50% | 89.60 (0.73 pp) | 0.00 | HOLD |
| SKU-004 | Premium Extra-Virgin Olive Oil | 29.90 | 460 | 9 | 6 | 13,484.90 | 5,609.50 | 50.93% | 41.60% | 101.40 (0.75 pp) | 1,258.20 | REPRICE (+RENEGOTIATE) |
| SKU-005 | Artisan Cheese Short Shelf-Life | 17.90 | 830 | 41 | 74 | 14,123.10 | 6,529.50 | 46.23% | 46.23% | 621.60 (4.40 pp) | 0.00 | HOLD |
| SKU-006 | Fresh Pasta Short Shelf-Life | 9.80 | 960 | 52 | 61 | 8,898.40 | 4,201.80 | 47.22% | 47.22% | 280.60 (3.15 pp) | 0.00 | HOLD |
| SKU-007 | Hand-Blown Glassware Fragile | 42.00 | 310 | 14 | 21 | 12,432.00 | 5,977.50 | 48.08% | 48.08% | 409.50 (3.29 pp) | 0.00 | REORDER NOW |
| SKU-008 | Single-Origin Wildflower Honey | 21.50 | 640 | 15 | 9 | 13,437.50 | 7,661.40 | 57.02% | 57.02% | 80.10 (0.60 pp) | 0.00 | REORDER NOW |
| SKU-009 | Small-Batch Hot Sauce | 13.90 | 720 | 18 | 11 | 9,757.80 | 4,311.85 | 52.80% | 44.19% | 81.95 (0.84 pp) | 840.65 | REPRICE (+RENEGOTIATE) |
| SKU-010 | Seasonal Gift Basket | 68.00 | 210 | 6 | 3 | 13,872.00 | 7,269.00 | 52.40% | 52.40% | 93.00 (0.67 pp) | 0.00 | LIQUIDATE |
| SKU-011 | Designer Ceramic Vase | 55.00 | 95 | 7 | 4 | 4,840.00 | 2,414.50 | 49.89% | 49.89% | 98.00 (2.02 pp) | 0.00 | LIQUIDATE |
| SKU-012 | Organic Pantry Staples Bundle | 34.00 | 380 | 11 | 7 | 12,546.00 | 6,450.75 | 51.42% | 51.42% | 110.25 (0.88 pp) | 0.00 | HOLD |
| **Total / Blend** |  |  | **7,945** | **237** | **248** | **156,716.70** | **76,595.50** | **50.37%** | **48.88%** | **2,286.70** | **2,339.75** |  |

**Action tag legend:** `REPRICE` = restore margin after unapproved cost increase (retail action); `RENEGOTIATE` = supplier-level cost/terms action (tagged alongside the row's primary action); `LIQUIDATE` = dead/slow stock cash recovery; `REORDER NOW` = below reorder point; `HOLD` = within policy.

### 2.1 Cost-creep detail (unapproved unit-cost increases)

"Units Consumed (90d)" = Units Sold + Shrinkage (the units actually charged at cost).

| Supplier | SKU | Prior Cost $ | Current Cost $ | Increase | Units Consumed (90d) | Margin Erosion | Creep $ / 90d |
|---|---|---|---|---|---|---|---|
| B | SKU-002 | 5.40 | 5.55 | +2.8% | 1,606 | 1.30 pp | 240.90 |
| C | SKU-004 | 14.20 | 16.90 | +19.0% | 466 | 9.33 pp | 1,258.20 |
| C | SKU-009 | 6.30 | 7.45 | +18.3% | 731 | 8.62 pp | 840.65 |
| **Total** |  |  |  |  |  | **-1.49 pp blended** | **2,339.75** |

### 2.2 Shrinkage detail

| SKU | Profile | Shrink Units | % of Units Sold | Shrink Cost $ | Margin Drag | Root Cause | Control (Section 4.2) |
|---|---|---|---|---|---|---|---|
| SKU-005 | perishable | 74 | 8.9% | 621.60 | 4.40 pp | spoilage | FIFO + date-label audit |
| SKU-006 | perishable | 61 | 6.4% | 280.60 | 3.15 pp | spoilage | FIFO + markdown tray |
| SKU-007 | fragile | 21 | 6.8% | 409.50 | 3.29 pp | breakage | double-box standard + transit claims |
| Other 9 SKUs | mixed | 92 | 1.6% blended | 975.00 | 0.60-2.02 pp each | normal range | weekly cycle counts |
| **Total** |  | **248** | 3.1% | **2,286.70** |  |  |  |

### 2.3 Capital efficiency: GMROI ranking (new)

GMROI = Annualized Net Profit / Inventory at Cost, with inventory valued on-hand at current unit cost (audit basis) and trailing-90-day profit annualized (x365/90). Portfolio: $310,637.31 of annualized contribution on $20,722.75 of inventory at cost = **14.99**. Context: the common retail rule of thumb is GMROI >= 3.2 ([Investopedia](https://www.investopedia.com/terms/g/gmroi.asp)); the simulated inventory runs leaner than typical specialty retail, so the ranking below - not the absolute level - is the decision-relevant output. Verified in CHK-11.

| Rank | SKU | Category | 90d Net Profit $ | Annualized Profit $ | Inventory at Cost $ | GMROI | Read |
|---|---|---|---|---|---|---|---|
| 1 | SKU-002 | Single-Origin Craft Chocolate | $9,686.70 | $39,284.95 | $527.25 | 74.51 | capital-efficiency champion - protect availability (REORDER NOW) |
| 2 | SKU-005 | Artisan Cheese Short Shelf-Life | $6,529.50 | $26,480.75 | $504.00 | 52.54 | capital-efficiency champion - hold the line |
| 3 | SKU-008 | Single-Origin Wildflower Honey | $7,661.40 | $31,071.23 | $623.00 | 49.87 | capital-efficiency champion - protect availability (REORDER NOW) |
| 4 | SKU-006 | Fresh Pasta Short Shelf-Life | $4,201.80 | $17,040.63 | $391.00 | 43.58 | capital-efficiency champion - hold the line |
| 5 | SKU-001 | Gourmet Coffee Whole Bean | $10,204.60 | $41,385.32 | $1,764.00 | 23.46 | healthy - HOLD |
| 6 | SKU-003 | Specialty Loose-Leaf Tea | $6,278.40 | $25,462.40 | $1,680.00 | 15.16 | healthy - HOLD |
| 7 | SKU-007 | Hand-Blown Glassware Fragile | $5,977.50 | $24,242.08 | $1,716.00 | 14.13 | below ROP - REORDER NOW protects turns |
| 8 | SKU-012 | Organic Pantry Staples Bundle | $6,450.75 | $26,161.38 | $1,890.00 | 13.84 | healthy - HOLD |
| 9 | SKU-009 | Small-Batch Hot Sauce | $4,311.85 | $17,486.95 | $1,415.50 | 12.35 | margin erosion - REPRICE lifts GMROI |
| 10 | SKU-004 | Premium Extra-Virgin Olive Oil | $5,609.50 | $22,749.64 | $2,197.00 | 10.35 | margin erosion - REPRICE lifts GMROI |
| 11 | SKU-010 | Seasonal Gift Basket | $7,269.00 | $29,479.83 | $4,340.00 | 6.79 | dead stock - LIQUIDATE |
| 12 | SKU-011 | Designer Ceramic Vase | $2,414.50 | $9,792.14 | $3,675.00 | 2.66 | dead stock - LIQUIDATE |
| -- | **Portfolio** | 12 SKUs | **$76,595.50** | **$310,637.31** | **$20,722.75** | **14.99** | benchmark rule of thumb >= 3.2 |

---

## 3. Inventory Replenishment & Dead-Stock Liquidation Schedule

### 3.1 Reorder-point audit (all 12 SKUs)

ROP = (Avg Daily Demand x Lead Time) + Safety Stock; a SKU is flagged at stockout risk when On Hand + On Order <= ROP. "Days Cover" is on-hand units / avg daily demand. "Projected Stockout" = units short of lead-time demand (only realized when position < Avg Daily Demand x Lead Time).

| SKU | Supplier | Lead (d) | Daily Demand | ROP | OnHand+OnOrder | Gap vs ROP | Days Cover | Projected Stockout in Lead Time | PO Qty (MOQ basis) | PO Cost $ | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SKU-001 | [REDACTED_ENTITY]_A | 12 | 13.78 | 265.33 | 300 | +34.67 | 13.1 | 0 | -- | -- | OK |
| SKU-002 | [REDACTED_ENTITY]_B | 10 | 17.56 | 265.56 | 95 | -170.56 | 5.4 | 81 u / $966.67 | 720 (15 x 48) | 3,996.00 | EXPEDITE |
| SKU-003 | [REDACTED_ENTITY]_A | 14 | 5.78 | 120.89 | 150 | +29.11 | 26.0 | 0 | -- | -- | OK |
| SKU-004 | [REDACTED_ENTITY]_C | 21 | 5.11 | 142.33 | 130 | -12.33 | 25.4 | 0 | 168 (7 x 24) | 2,839.20 | ORDER NOW |
| SKU-005 | [REDACTED_ENTITY]_B | 5 | 9.22 | 76.11 | 100 | +23.89 | 6.5 | 0 | -- | -- | OK |
| SKU-006 | [REDACTED_ENTITY]_B | 4 | 10.67 | 77.67 | 85 | +7.33 | 8.0 | 0 | -- | -- | OK |
| SKU-007 | [REDACTED_ENTITY]_D | 30 | 3.44 | 123.33 | 112 | -11.33 | 25.5 | 0 | 120 (6 x 20) | 2,340.00 | ORDER NOW |
| SKU-008 | [REDACTED_ENTITY]_A | 18 | 7.11 | 173.00 | 70 | -103.00 | 9.8 | 58 u / $1,247.00 | 324 (9 x 36) | 2,883.60 | EXPEDITE |
| SKU-009 | [REDACTED_ENTITY]_C | 16 | 8.00 | 168.00 | 190 | +22.00 | 23.8 | 0 | -- | -- | OK |
| SKU-010 | [REDACTED_ENTITY]_D | 25 | 2.33 | 83.33 | 140 | +56.67 | 60.0 | 0 | -- | -- | LIQUIDATE - do not reorder |
| SKU-011 | [REDACTED_ENTITY]_D | 28 | 1.06 | 44.56 | 150 | +105.44 | 142.1 | 0 | -- | -- | LIQUIDATE - do not reorder |
| SKU-012 | [REDACTED_ENTITY]_C | 15 | 4.22 | 93.33 | 120 | +26.67 | 28.4 | 0 | -- | -- | OK |
| **PO program total** |  |  |  |  |  |  |  | **$2,213.67 / cycle avoided** | **1,332 units** | **12,058.80** |  |

Order-up-to policy: target = ROP + 30 days of demand; PO quantity = the MOQ multiple that closes the gap (CHK-07 verified). EXPEDITE priority (SKU-002, SKU-008) because their position is below lead-time demand: request partial/air shipment within 24h. SKU-004 reorders at the contested cost while Section 4.1 is in flight; retail moves first (Section 4.3).

### 3.2 Dead-stock liquidation schedule (cash recovery in 30 days)

Trigger: days since last sale > 60 (SKU-010: 75d) or days of supply > 120 (SKU-011: 142.1d). Tier unit split assumption: 40% / 30% / 30% of on-hand units (verified in CHK-08/CHK-09 pipeline; proceeds below are deterministic given the split).

| SKU | On Hand | Retail Value $ | Cost Basis $ | Tier 1 (d1-10, 20% off) | Tier 2 (d11-20, 35% off) | Tier 3 (d21-30, 50% off) | Total Proceeds $ | Recovery vs Retail |
|---|---|---|---|---|---|---|---|---|
| SKU-010 | 140 | 9,520.00 | 4,340.00 | 56 u @ 54.40 = 3,046.40 | 42 u @ 44.20 = 1,856.40 | 42 u @ 34.00 = 1,428.00 | 6,330.80 | 66.5% |
| SKU-011 | 150 | 8,250.00 | 3,675.00 | 60 u @ 44.00 = 2,640.00 | 45 u @ 35.75 = 1,608.75 | 45 u @ 27.50 = 1,237.50 | 5,486.25 | 66.5% |
| **Total** | **290** | **17,770.00** | **8,015.00** |  |  |  | **11,817.05** | **66.5%** |

Execution notes: list both SKUs by Day 2 in store and online; bundle SKU-010 (prior-season packaging) with SKU-001 coffee as a gift-ready set; SKU-011 goes to marketplace clearance with free gift wrap. Units unsold after Day 30: bundle into the holiday assortment or donate for a receipt - owner decision (see Section 5.4, Edge Case 3 for the related supplier-side risk).

### 3.3 Supplier payment-term targets

| Supplier | SKUs | Current Terms | Target Terms | Rationale |
|---|---|---|---|---|
| [REDACTED_ENTITY]_A | 001, 003, 008 | Net 30 | Net 45 (or 1%/10 early-pay option) | Stable costs, clean quality - reward with volume continuity |
| [REDACTED_ENTITY]_B | 002, 005, 006 | Net 15 | Net 21 | Perishables; modest extension; price-lock letter on file for SKU-002 |
| [REDACTED_ENTITY]_C | 004, 009, 012 | Net 60 | Net 60 + 3% quarterly rebate + 180-day price lock | Contest the $2,098.85 of unapproved increases (Section 4.1) |
| [REDACTED_ENTITY]_D | 007, 010, 011 | Net 30 / Net 45 | Net 45 uniform | Long-lead fragile goods; 48h transit-damage claim policy |

### 3.4 30-day action timeline

| Window | Actions | Owner | Success Criterion |
|---|---|---|---|
| Days 1-2 | Issue the 4 POs above (1,332 units) with expedite flags on SKU-002/008; send the Section 4.1 Price-Lock & Rebate Notice to supplier C (SKU-004/009) and a price-lock letter to supplier B (SKU-002) | Owner | POs acknowledged; notices sent with delivery confirmation |
| Days 1-7 | Launch Tier-1 liquidation (20% off) on SKU-010/011 in store + e-commerce; start the Weekly Shrinkage SOP (Section 4.2); implement repricing SKU-004 -> 34.90, SKU-009 -> 15.90 | Store/Warehouse | >= 40% of dead units sold at Tier 1; new prices live |
| Days 8-14 | Tier 2 (35% off); renegotiation calls on the Section 3.3 term targets | Owner | Tier 2 sell-through >= 30% of units; rebate or rollback confirmed in writing |
| Days 15-21 | Tier 3 (50% off / bundles); elasticity check on repriced SKUs (weekly units vs 4-week baseline; rollback rule -12%) | Owner | Clearance >= 85% cumulative; elasticity verdict recorded |
| Days 22-30 | Close out liquidation (bundle/donate remainder - owner call); first reorder review under the new ROP rules; verify the supplier C rebate credit lands on the next invoice | Owner | ~$11,817.05 proceeds booked; $2,098.85 rebate or cost rollback confirmed |

### 3.5 Supplier Negotiation Playbook Matrix (new)

| Supplier | SKUs | Opening Ask | Fallback Position | Hard Walk-Away / Dual-Source Trigger | Approved Concession Trade |
|---|---|---|---|---|---|
| [REDACTED_ENTITY]_C | 004, 009, 012 | Rollback to 14.20 / 6.30, 180-day price lock, keep Net 60, +3% quarterly rebate | Retroactive rebate of $2,098.85 + price lock, unit costs stay at 16.90 / 7.45 | No rollback AND no rebate within 10 business days -> shift >= 30% of SKU-004/009 volume to a dual-source trial at the next sourcing cycle | Consolidated SKU-012 volume + 12-month volume commitment in exchange for the 180-day price lock |
| [REDACTED_ENTITY]_B | 002, 005, 006 | Rollback SKU-002 to 5.40, price lock, terms Net 15 -> Net 21 | $0.15/unit credit on future SKU-002 invoices ($240.90 per 90d equivalent), unit costs unchanged | A second unnotified cost increase on any supplier-B SKU -> qualify a second chocolate supplier | Consolidated weekly deliveries (fewer drops) in exchange for Net 21 terms |
| [REDACTED_ENTITY]_A | 001, 003, 008 | Net 30 -> Net 45 (or 1%/10 early-pay) + 180-day price lock on SKU-008 | Keep Net 30 with the 1% early-pay discount taken on SKU-008 only | Any unnotified increase on SKU-008 -> qualify a second honey supplier | Shared 90-day demand forecasts + volume continuity in exchange for the terms extension |
| [REDACTED_ENTITY]_D | 007, 010, 011 | Net 45 uniform + 48h transit-damage credit policy + freight allowance on SKU-007 | Damage-credit policy only, terms unchanged | Transit damage > 3% of units on SKU-007 without credit -> dual-source trial PO (20 units) while honoring the current PO cadence | Replenishment of SKU-007 plus next-season basket volume through D once clearance completes |

### 3.6 Weekly 30-Day Cash-Flow Waterfall (new)

Deterministic day-based model (verified in CHK-13): POs issued day 1; goods received at day 1 + lead time; invoices dated at receipt; cash outflow at receipt + payment terms; tiered liquidation sales spread evenly across each tier's day range (T1 d1-10, T2 d11-20, T3 d21-30) over weeks W1 d1-7, W2 d8-14, W3 d15-21, W4 d22-30.

| Week | Days | Cash In (liquidation) | Cash Out (PO payments due) | Net | Cumulative |
|---|---|---|---|---|---|
| W1 | 1-7 | $3,980.48 | $0.00 | +$3,980.48 | +$3,980.48 |
| W2 | 8-14 | $3,091.98 | $0.00 | +$3,091.98 | +$7,072.46 |
| W3 | 15-21 | $2,345.64 | $0.00 | +$2,345.64 | +$9,418.10 |
| W4 | 22-30 | $2,398.95 | $0.00 | +$2,398.95 | +$11,817.05 |
| **Total** | **1-30** | **$11,817.05** | **$0.00** | **+$11,817.05** |  |

Minimum cumulative cash position: **+$3,980.48** - the program is self-funding with no overdraft at any point, because every PO payment falls due after the 30-day window:

| SKU | PO Cost $ | Receipt (day) | Payment Due (day) | Terms | Priority |
|---|---|---|---|---|---|
| SKU-002 | 3,996.00 | d11 | d41 | Net 30 | EXPEDITE |
| SKU-008 | 2,883.60 | d19 | d49 | Net 30 | EXPEDITE |
| SKU-007 | 2,340.00 | d31 | d61 | Net 30 | ORDER NOW |
| SKU-004 | 2,839.20 | d22 | d82 | Net 60 | ORDER NOW |
| **Total** | **12,058.80** |  |  |  |  |

By the first due date (d41) the $11,817.05 of liquidation cash is fully collected and the $241.75 gap to commitments ($12,058.80) is covered by roughly one trading day of baseline contribution (~$850/day). EXPEDITE POs (SKU-002, SKU-008) arrive inside their lead times; payment terms - not cash - carry the gap.

---

## 4. Operational SOPs & Ready-to-Send Templates

### 4.1 Supplier Price-Lock & Rebate Notice (ready to send)

```
To:       Key Account Manager - [REDACTED_ENTITY]_C
From:     [REDACTED_ENTITY], Owner / Buying Office - [REDACTED_ENTITY]
Date:     [DATE]
Subject:  Formal Notice - Unapproved Unit-Cost Increases on PO-1004 / PO-1009 -
          Price Lock & Rebate Request

Dear [REDACTED_ENTITY]_C Account Team,

Our 90-day receiving and invoice audit (closed 2026-11-18) documents two unit-cost
increases shipped without the 30-day written notice and our written approval, both
required by our purchase terms:

  SKU      Item (internal reference)           PO        Prior  Current  Increase  Units (90d)  Cost Impact
  SKU-004  Premium Extra-Virgin Olive Oil      PO-1004   14.20  16.90    +19.0%    466          $1,258.20
  SKU-009  Small-Batch Hot Sauce               PO-1009   6.30   7.45     +18.3%    731          $840.65
  TOTAL                                                                          $2,098.85

These two SKUs are core traffic drivers that we promote at fixed retail prices set in
good faith on your prior costs. Our annual spend with [REDACTED_ENTITY]_C is
[REDACTED_AMOUNT].

We therefore request written confirmation within 10 business days of:

  1. Rollback to prior unit costs (USD 14.20 / USD 6.30) on all future shipments; OR
  2. A retroactive rebate of USD 2,098.85 on the 90-day volumes above, credited on
     our next invoice;
  3. A 180-day written price lock on SKU-004 and SKU-009, with 30-day written notice
     and our written approval required for any future change;
  4. Continuation of Net 60 payment terms for the next 12 months.

Absent confirmation, we will rebalance these volumes to alternate suppliers in our
next sourcing cycle and share this audit with our buying cooperative.

Regards,
[REDACTED_ENTITY]
Owner / Buying Office - [REDACTED_ENTITY]
[REDACTED_ENTITY] - [REDACTED_ENTITY]
```

### 4.2 Weekly Warehouse & Shrinkage Control Checklist (5-step SOP)

1. **Receiving & count match (Mon + Thu, receiving clerk).** Blind-count every inbound PO line against the PO quantity before signing; photograph damaged cartons; file the supplier claim within 24h. Tolerance: zero unexplained unit variance.
2. **Perishable FIFO & date-label audit (daily, 10 min, floor staff).** Rotate SKU-005/006; move units within 2 days of shelf-life end to the markdown tray; log every discard by SKU in the shrinkage log. Target: shrinkage <= 5% of units sold (SKU-005 currently 8.9%, SKU-006 6.4%).
3. **Fragile handling standard (daily, warehouse).** SKU-007 double-box standard, shelf liners, "max 2 stack" labeling; same-day breakage log; transit-damage claim to supplier D within 48h. Target: breakage <= 3% of units sold (currently 6.8%).
4. **Cycle count (Wed, warehouse lead).** Blind-count the top-5 shrink SKUs (005, 006, 007, 002, 009); variance > 1.5% of on-hand escalates to the owner the same day; correct the shrinkage records.
5. **Returns & reorder review (Fri, owner).** Process returns within 48h with reason codes; review the week's shrinkage log and variance reports; check position (on hand + on order) vs ROP for all 12 SKUs and queue POs per Section 4.3 before the weekend.

### 4.3 Dynamic Repricing & Reorder Rules (owner rulebook)

| Rule | Trigger | Action | Deadline |
|---|---|---|---|
| REPRICE | Net margin at current cost < 45% (today: SKU-004 41.60%, SKU-009 44.19%) | Raise retail in steps <= 5% every 2 weeks until margin >= 50%; elasticity stop: weekly units -12% vs 4-week baseline -> hold or roll back one step | Start within 7 days |
| COST-CREEP CONTEST | Unapproved unit-cost increase > 5% (today: +19.0%, +18.3%, +2.8%) | Send the Section 4.1 notice; interim pass-through: full if margin fell > 8 pp (SKU-004, SKU-009), 50% if 4-8 pp | Notice within 5 business days |
| REORDER | On hand + on order <= ROP | PO = MOQ multiple closing (ROP + 30-day demand - position); confirm supplier acknowledgment | PO within 48h |
| EXPEDITE | Position < lead-time demand (today: SKU-002, SKU-008) | Request partial/air shipment and written confirmation from the supplier | Within 24h |
| LIQUIDATE | Days since last sale > 60 OR days of supply > 120 (today: SKU-010, SKU-011) | Tiered clearance 20% / 35% / 50% over 30 days (Section 3.2); then bundle/donate decision | Program live within 7 days |
| SHRINK CLAIM | Shrinkage > 5% of units sold on a SKU (today: 005, 006, 007) | Apply the Section 4.2 SOP; claim transit/fragile damage to the supplier; review packaging cost vs shrink saving quarterly | Same week |
| TERMS | Supplier renewal / annual review | Ask +15 days of terms or a 1-2% early-pay discount; 180-day price lock (Section 3.3) | At renewal |

### 4.4 Price-Elasticity & Break-Even Sensitivity Matrix (new)

Profit at the new retail scales linearly with volume (returns and shrinkage scale proportionally). Break-even volume drop = the volume loss at which dollar contribution exactly equals pre-reprice profit. Both repriced traffic drivers stay accretive far beyond the -12% rollback trigger (Section 4.3), so the REPRICE decision is robust to the elasticity risk raised in Edge Case 1.

| SKU | Reprice | Pre-Reprice Profit (90d) | 0% Base | -5% Mild | -10% Moderate | -15% Stress | Break-Even Volume Drop |
|---|---|---|---|---|---|---|---|
| SKU-004 | 29.90 -> 34.90 | $5,609.50 | $7,864.50 (+$2,255.00) | $7,471.28 (+$1,861.78) | $7,078.05 (+$1,468.55) | $6,684.83 (+$1,075.33) | -28.67% |
| SKU-009 | 13.90 -> 15.90 | $4,311.85 | $5,715.85 (+$1,404.00) | $5,430.06 (+$1,118.21) | $5,144.27 (+$832.42) | $4,858.47 (+$546.62) | -24.56% |

Reading: even a -15% volume shock still adds +$1,075.33 (SKU-004) and +$546.62 (SKU-009) per 90d versus today, and the break-even drops (-28.67% / -24.56%) sit at roughly twice the rollback trigger - the staged +5% steps with the -12% trigger leave a wide safety margin. Verified in CHK-12.

---

## 5. Calculation Verification Log & Human-Review Edge Cases

### 5.1 Formulas (exact, as implemented)

```
1. Net Margin %        = ((Units Sold - Returns) * Price - (Units Sold + Shrinkage) * Current Cost)
                         / ((Units Sold - Returns) * Price) * 100
2. Cost Creep $ (90d)  = (Units Sold + Shrinkage) * (Current Unit Cost - Prior Unit Cost)
   Margin Erosion (pp) = Margin(Prior Cost) - Margin(Current Cost)
3. Avg Daily Demand    = Units Sold / 90
   ROP                 = (Avg Daily Demand * Lead Time) + Safety Stock
   STOCKOUT RISK       when On Hand + On Order <= ROP
4. Days of Supply      = On Hand / Avg Daily Demand
   DEAD/SLOW           when Days Since Last Sale > 60 OR Days of Supply > 120
   Trapped Capital     = On Hand * Current Unit Cost   (dead/slow SKUs only)
5. Order-Up-To         = ROP + 30 * Avg Daily Demand
   PO Qty              = ceil((Order-Up-To - On Hand - On Order) / MOQ) * MOQ
6. Liquidation proceeds = tier units * retail * (1 - tier discount);
   tiers 20% / 35% / 50% off on a 40% / 30% / 30% unit split
7. Shrinkage drag (pp) = [((Units Sold - Returns) * Price - Units Sold * Current Cost)
                         / ((Units Sold - Returns) * Price) * 100] - Net Margin %
8. Post-optimization scenario: SKU-004 retail 34.90; SKU-009 retail 15.90;
   SKU-002 cost rollback to 5.40; 30% shrinkage cut on SKU-005/006/007;
   volumes held constant (see Edge Case 1). Renegotiation upside:
   SKU-004 cost target 15.50 (+$652.40 per 90d).
```

### 5.2 Script verification checks

The certified run log is in `verification/run_log.txt`; machine-readable output in `verification/computed_metrics.json`. `compute_metrics.py` contains the identical formulas and checks and reproduces every number from the three CSVs and the `exports/` batches in any Python 3 environment.

| Check | Description | Result |
|---|---|---|
| CHK-01 | Referential integrity: 12 SKUs, identical key set across all three CSVs | PASS |
| CHK-02 | Domain checks: 0 <= returns, shrinkage <= units sold; retail > current cost > 0; positive lead/MOQ/holding | PASS |
| CHK-03 | Blended net margin reproduced by an independent single-pass recomputation | PASS |
| CHK-04 | Cost-creep SKU set == {SKU-002, SKU-004, SKU-009} | PASS |
| CHK-05 | Below-ROP SKU set == {SKU-002, SKU-004, SKU-007, SKU-008} | PASS |
| CHK-06 | Dead/slow-stock SKU set == {SKU-010, SKU-011} | PASS |
| CHK-07 | Proposed PO quantities are MOQ multiples and close the order-up-to gap | PASS |
| CHK-08 | Trapped working capital reconciles to an independent recomputation ($8,015.00) | PASS |
| CHK-09 | Coverage sanity: no SKU above 200 days of supply unless dead-stock flagged | PASS |
| CHK-10 | Redaction compliance: supplier ids within [REDACTED_ENTITY]_A..D; PO ids unique | PASS |
| CHK-11 | GMROI reconciles across all 12 SKUs; ranking and portfolio ratio internally consistent | PASS |
| CHK-12 | Elasticity break-even thresholds verified for SKU-004 and SKU-009 (profit at break-even volume == pre-reprice profit) | PASS |
| CHK-13 | Weekly cash waterfall reconciles: total inflows == $11,817.05, total PO commitments == $12,058.80, cumulative cash never negative | PASS |
| CHK-14 | ERP/POS batch CSV row-count and dollar-sum reconciliation against report tables | PASS |
| CHK-15 | Redaction regex scan across all package .md/.csv/.py/.json files: zero unredacted emails, phone numbers, or forbidden placeholders | PASS |

**Result: 15/15 checks PASS.**

### 5.3 Cross-file reconciliation

| Reconciliation | Value | Ties Across | Status |
|---|---|---|---|
| SKU keys matched | 12 = 12 = 12 | sales / PO / stock files | Tied |
| 90-day units sold | 7,945 | sales file | Tied |
| Net revenue | $156,716.70 | sales x retail prices | Tied |
| COGS at current cost | $80,121.20 | sales units x PO current cost | Tied |
| Contribution profit | $76,595.50 | revenue - COGS | Tied |
| Trapped capital | $8,015.00 | stock on-hand x PO current cost (SKU-010/011) | Tied |
| PO reorder program | 1,332 units / $12,058.80 | MOQ multiples of the PO file | Tied |
| Suppliers referenced | 4 ([REDACTED_ENTITY]_A..D) | PO file (CHK-10) | Tied |
| Portfolio GMROI | 14.99 on $20,722.75 inventory at cost | sales x PO current cost x stock on-hand (CHK-11) | Tied |
| Cash waterfall | $11,817.05 inflows == liquidation proceeds; $12,058.80 == PO program | liquidation tiers x PO terms (CHK-13) | Tied |

### 5.4 Human-review edge cases (owner judgment required)

1. **Price-elasticity risk on repriced core traffic drivers (SKU-004, SKU-009).** The optimization targets assume volumes hold at +16.7% (29.90 -> 34.90) and +14.4% (13.90 -> 15.90) retail. Both are repeat-purchase items where a price move can permanently shift buying habits. Mitigation: staged +5% steps, a 2-week store-vs-online split test, and the hard rollback trigger (weekly units -12% vs 4-week baseline). Owner call: accept the margin-vs-traffic trade-off; worth ~$3,659.00 per 90d at constant volumes.
2. **MOQ vs spoilage trade-off on short-shelf-life SKU-005.** MOQ 40 equals ~4.3 days of demand (9.22 units/day) on a 5-day lead, so ordering less often means bigger perishable lots and a worse spoilage rate (already 8.9%). Options: negotiate MOQ 24 (~2.6 days of cover), ask supplier B for consignment or supplier-held buffer stock, or accept the spoilage. Owner call on admin cost vs spoilage saving (a 30% spoilage cut is worth $186.48 per 90d on SKU-005 alone).
3. **Supplier-switching lead-time risk on fragile SKU-007 (single-source, 30-day lead).** Qualifying an alternate fragile-goods supplier typically adds 30-45 days; switching while SKU-007 is already below ROP would open a coverage hole exactly when it cannot be absorbed. Recommendation: place a dual-source trial PO of 1 MOQ (20 units, $390.00) while keeping supplier D on the main flow, and restore position above ROP before any switch. Owner call on timing, and on the transit-damage claim history with [REDACTED_ENTITY]_D.

### 5.5 Reproducibility

`python smb/compute_metrics.py` regenerates every number in this report from the three CSVs and the `exports/` batches, reruns CHK-01..CHK-15, and rewrites `verification/computed_metrics.json`. No randomness, no manual overrides: identical inputs produce identical outputs. The certified run log for this audit is `verification/run_log.txt`.

### 5.6 External Reference & Methodology Log (context only)

External benchmarks and standard-formula references, kept strictly separate from the internal deterministic calculations (Sections 5.1-5.3) and from the 3 human-owner edge cases (Section 5.4). None of these references enters the baseline numbers.

| Topic | Standard / Source | Relation to this audit |
|---|---|---|
| Reorder point & safety stock | APICS/ASCM (CPIM body of knowledge): ROP = expected demand during lead time + safety stock, with safety stock sized to demand variability and target service level | This audit applies the standard ROP form (Section 5.1, formula 3) with the safety-stock levels as configured in the POS; no external data enters the calculation |
| Retail shrink benchmark | NRF 2023 National Retail Security Survey: average shrink rate 1.6% of retail sales in FY 2022, up from 1.4% in FY 2021 - [nrf.com](https://nrf.com/media-center/press-releases/shrink-accounted-over-112-billion-industry-losses-2022-according-nrf) | The simulated blended shrink here is 3.1% of units sold - roughly twice the NRF benchmark - concentrated in SKU-005/006/007 (Section 2.2), which supports the SHRINK CLAIM rule (Section 4.3) |
| GMROI benchmark | Investopedia: GMROI = gross profit / average inventory cost; common retail rule of thumb GMROI >= 3.2 to cover occupancy, labor and profit - [investopedia.com](https://www.investopedia.com/terms/g/gmroi.asp) | Portfolio GMROI = 14.99 (Section 2.3). Simulated inventory is leaner than typical specialty retail (days of supply far below the usual 30-60 range), so the absolute level exceeds the reference band; the SKU ranking is the decision-relevant output |

Methodology note: GMROI in this package uses trailing-90-day contribution profit annualized (x365/90) over current on-hand inventory at current unit cost, per the audit basis; external practice often uses a rolling average inventory, which would change the absolute level but not the ranking.

---

## Appendix A - File Map

| File | Contents |
|---|---|
| `data/sku_sales_90d.csv` | 90-day sales per SKU (retail price, units sold, returns, shrinkage, holding cost %) |
| `data/supplier_purchase_orders.csv` | Latest open PO per SKU (prior/current unit cost, lead time, payment terms, MOQ) |
| `data/warehouse_stock_status.csv` | Day-90 stock snapshot (on hand, on order, days since last sale, safety stock) |
| `smb_operations_audit.md` | This report |
| `README.md` | Package overview, compliance and verification notes |
| `compute_metrics.py` | Deterministic Python verification script (reproduces all metrics + 10 checks) |
| `verification/run_log.txt` | Certified verification run log |
| `verification/computed_metrics.json` | Machine-readable audit metrics and check results |
| `exports/erp_po_import_batch.csv` | Execution-ready PO import lines (4 POs, 1,332 units, $12,058.80) |
| `exports/pos_repricing_and_clearance_batch.csv` | Execution-ready storefront price updates (2 repricing + 2 clearance actions) |
| `source_docs/supplier_terms_and_discrepancies.md` | Redacted purchase-term summary and receiving discrepancy log (source evidence for the cost-creep findings) |
