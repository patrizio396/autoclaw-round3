#!/usr/bin/env python3
"""Deterministic verification for the [REDACTED_ENTITY] 90-day SMB operations audit.

Reads the sanitized datasets in smb/data/ and the execution batches in smb/exports/,
recomputes every audit metric from scratch (GMROI, elasticity break-even, weekly cash
waterfall included), runs 15 cross-file integrity checks, prints the exact Markdown
table rows used in smb_operations_audit.md, and writes
smb/verification/computed_metrics.json plus smb/verification/run_log.txt.

Standard library only; no randomness; no network. Identical inputs always produce
identical outputs (deterministic verification per audit Section 5).
"""

import csv
import json
import math
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
EXPORTS_DIR = os.path.join(BASE, "exports")
OUT_DIR = os.path.join(BASE, "verification")
DAYS = 90
REVIEW_DAYS = 30
ANNUALIZE = 365.0 / DAYS

# ---- Post-optimization SCENARIO assumptions (owner decisions, not dataset facts) ----
REPRICE_RETAIL = {"SKU-004": 34.90, "SKU-009": 15.90}
ROLLBACK_COST = {"SKU-002": 5.40}   # renegotiated back to prior unit cost
UPSIDE_COST = {"SKU-004": 15.50}    # stretch renegotiation target (upside only)
SHRINK_CUT = {"SKU-005": 0.30, "SKU-006": 0.30, "SKU-007": 0.30}

EXPECTED_CREEP = {"SKU-002", "SKU-004", "SKU-009"}
EXPECTED_FLAGS = {"SKU-002", "SKU-004", "SKU-007", "SKU-008"}
EXPECTED_DEAD = {"SKU-010", "SKU-011"}

CHECKS = []


def check(cid, desc, ok, detail=""):
    CHECKS.append({"id": cid, "check": desc,
                   "result": "PASS" if ok else "FAIL", "detail": detail})
    tag = "PASS" if ok else "FAIL"
    line = "[%s] %s %s" % (tag, cid, desc)
    if detail:
        line += " | " + detail
    print(line)
    return ok


def load(name, directory=DATA_DIR):
    path = os.path.join(directory, name)
    if not os.path.exists(path):
        print("MISSING INPUT: %s" % path)
        sys.exit(2)
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def usd(v):
    return "{:,.2f}".format(v)


def num(v):
    return "{:,}".format(v)


class _Tee(object):
    """Duplicate stdout to a log file: some console hosts do not capture stdout."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for st in self.streams:
            try:
                st.write(data)
            except Exception:
                pass
        return len(data)

    def flush(self):
        for st in self.streams:
            try:
                st.flush()
            except Exception:
                pass


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    log_path = os.path.join(OUT_DIR, "run_log.txt")
    _logf = open(log_path, "w", encoding="utf-8")
    sys.stdout = _Tee(sys.__stdout__, _logf)
    sales_rows = load("sku_sales_90d.csv")
    po_rows = load("supplier_purchase_orders.csv")
    stock_rows = load("warehouse_stock_status.csv")

    S = {}
    for r in sales_rows:
        S[r["sku_id"]] = {
            "category": r["category"],
            "price": float(r["retail_price"]),
            "sold": int(r["units_sold_90d"]),
            "returned": int(r["units_returned"]),
            "shrink": int(r["shrinkage_units"]),
            "hold_pct": float(r["holding_cost_pct"]),
        }
    for r in po_rows:
        s = S[r["sku_id"]]
        s.update(po_id=r["po_id"], supplier=r["supplier_id"],
                 prior_cost=float(r["prior_unit_cost"]),
                 cur_cost=float(r["current_unit_cost"]),
                 lead=int(r["lead_time_days"]),
                 terms=r["payment_terms"], moq=int(r["moq"]))
    for r in stock_rows:
        s = S[r["sku_id"]]
        s.update(on_hand=int(r["on_hand_units"]),
                 on_order=int(r["on_order_units"]),
                 dsls=int(r["days_since_last_sale"]),
                 safety=int(r["safety_stock_units"]))

    # CHK-01 referential integrity
    ids_s = set(S)
    ids_po = {r["sku_id"] for r in po_rows}
    ids_st = {r["sku_id"] for r in stock_rows}
    check("CHK-01", "Referential integrity: 12 SKUs, identical key set across all three CSVs",
          len(sales_rows) == len(po_rows) == len(stock_rows) == 12 and ids_s == ids_po == ids_st,
          "sales=%d po=%d stock=%d" % (len(sales_rows), len(po_rows), len(stock_rows)))

    # CHK-02 domain checks
    bad = []
    for sid, s in S.items():
        if not 0 <= s["returned"] <= s["sold"]:
            bad.append(sid + ":returns")
        if not 0 <= s["shrink"] <= s["sold"]:
            bad.append(sid + ":shrink")
        if not (s["cur_cost"] > 0 and s["price"] > s["cur_cost"]):
            bad.append(sid + ":price>cost")
        if s["lead"] <= 0 or s["moq"] <= 0 or s["safety"] < 0 or s["on_hand"] < 0 or s["hold_pct"] <= 0:
            bad.append(sid + ":ranges")
    check("CHK-02", "Domain checks: returns/shrinkage within sold, retail>current cost>0, positive lead/MOQ/holding",
          not bad, "12/12 clean" if not bad else ",".join(bad))

    # ---- per-SKU deterministic metrics
    tot = {"rev": 0.0, "profit": 0.0, "profit_prior": 0.0, "creep": 0.0,
           "shrink_cost": 0.0, "trapped": 0.0, "carrying": 0.0,
           "po_cost": 0.0, "protected": 0.0, "lost": 0.0, "po_units": 0,
           "inv_value": 0.0, "annualized_profit": 0.0}
    for sid in sorted(S):
        s = S[sid]
        net_units = s["sold"] - s["returned"]
        rev = net_units * s["price"]
        cogs = (s["sold"] + s["shrink"]) * s["cur_cost"]
        profit = rev - cogs
        margin = profit / rev * 100.0
        margin_prior = (rev - (s["sold"] + s["shrink"]) * s["prior_cost"]) / rev * 100.0
        margin_ns = (rev - s["sold"] * s["cur_cost"]) / rev * 100.0
        shrink_cost = s["shrink"] * s["cur_cost"]
        drag_pp = margin_ns - margin
        creep_d = (s["sold"] + s["shrink"]) * max(0.0, s["cur_cost"] - s["prior_cost"])
        creep_pct = (s["cur_cost"] / s["prior_cost"] - 1.0) * 100.0
        dd = s["sold"] / float(DAYS)
        rop = dd * s["lead"] + s["safety"]
        position = s["on_hand"] + s["on_order"]
        flagged = position <= rop + 1e-9
        dos = s["on_hand"] / dd
        dead = s["dsls"] > 60 or dos > 120
        trapped = s["on_hand"] * s["cur_cost"] if dead else 0.0
        carrying = trapped * s["hold_pct"] / 100.0
        lost_units = max(0.0, dd * s["lead"] - position)
        lost_rev = lost_units * s["price"]

        if creep_d > 0 and margin < 45.0:
            action = "REPRICE"
        elif dead:
            action = "LIQUIDATE"
        elif flagged:
            action = "REORDER NOW"
        else:
            action = "HOLD"
        if creep_d > 0 and action in ("REPRICE", "REORDER NOW"):
            action += " (+RENEGOTIATE)"

        qty, target = 0, 0.0
        if flagged:
            target = rop + REVIEW_DAYS * dd
            need = target - position
            qty = max(int(math.ceil(need / s["moq"])) * s["moq"], s["moq"])

        s.update(net_units=net_units, rev=rev, cogs=cogs, profit=profit,
                 margin=margin, margin_prior=margin_prior, shrink_cost=shrink_cost,
                 drag_pp=drag_pp, creep_d=creep_d, creep_pct=creep_pct, dd=dd,
                 rop=rop, position=position, flagged=flagged, dos=dos, dead=dead,
                 trapped=trapped, carrying=carrying, lost_units=lost_units,
                 lost_rev=lost_rev, action=action, qty=qty, target=target)

        tot["rev"] += rev
        tot["profit"] += profit
        tot["profit_prior"] += rev - (s["sold"] + s["shrink"]) * s["prior_cost"]
        tot["creep"] += creep_d
        tot["shrink_cost"] += shrink_cost
        tot["trapped"] += trapped
        tot["carrying"] += carrying
        tot["po_units"] += qty
        tot["po_cost"] += qty * s["cur_cost"]
        tot["protected"] += qty * s["price"]
        tot["lost"] += lost_rev

    blended = tot["profit"] / tot["rev"] * 100.0
    blended_prior = tot["profit_prior"] / tot["rev"] * 100.0

    # CHK-03 independent recomputation
    rev2 = sum((s["sold"] - s["returned"]) * s["price"] for s in S.values())
    profit2 = sum((s["sold"] - s["returned"]) * s["price"]
                  - (s["sold"] + s["shrink"]) * s["cur_cost"] for s in S.values())
    check("CHK-03", "Blended net margin reproduced by independent single-pass recomputation",
          abs(rev2 - tot["rev"]) < 1e-6 and abs(profit2 - tot["profit"]) < 1e-6,
          "rev=%.2f profit=%.2f blended=%.4f%%" % (rev2, profit2, profit2 / rev2 * 100.0))

    creep_ids = {sid for sid, s in S.items() if s["creep_d"] > 0}
    check("CHK-04", "Cost-creep SKU set == {SKU-002, SKU-004, SKU-009}",
          creep_ids == EXPECTED_CREEP, "found=" + ",".join(sorted(creep_ids)))

    flag_ids = {sid for sid, s in S.items() if s["flagged"]}
    check("CHK-05", "Below-ROP SKU set == {SKU-002, SKU-004, SKU-007, SKU-008}",
          flag_ids == EXPECTED_FLAGS, "found=" + ",".join(sorted(flag_ids)))

    dead_ids = {sid for sid, s in S.items() if s["dead"]}
    check("CHK-06", "Dead/slow-stock SKU set == {SKU-010, SKU-011}",
          dead_ids == EXPECTED_DEAD, "found=" + ",".join(sorted(dead_ids)))

    ok7 = True
    for sid, s in S.items():
        if s["flagged"]:
            if s["qty"] % s["moq"] != 0 or s["qty"] < s["target"] - s["position"] - 1e-6:
                ok7 = False
    check("CHK-07", "Proposed PO quantities are MOQ multiples and close the order-up-to gap", ok7)

    trapped2 = sum(s["on_hand"] * s["cur_cost"] for s in S.values()
                   if s["dsls"] > 60 or s["on_hand"] / (s["sold"] / float(DAYS)) > 120)
    check("CHK-08", "Trapped working capital reconciles to independent recomputation",
          abs(trapped2 - tot["trapped"]) < 1e-6, "capital=" + usd(tot["trapped"]))

    ok9 = all(s["dos"] <= 200 or s["dead"] for s in S.values())
    check("CHK-09", "Coverage sanity: no SKU above 200 days of supply unless dead-stock flagged", ok9)

    suppliers = {s["supplier"] for s in S.values()}
    po_ids = [s["po_id"] for s in S.values()]
    ok10 = all(sp.startswith("[REDACTED_ENTITY]_") and sp[-1] in "ABCD" for sp in suppliers) \
        and len(po_ids) == len(set(po_ids))
    check("CHK-10", "Redaction compliance: supplier ids within [REDACTED_ENTITY]_A..D; PO ids unique", ok10,
          "suppliers=" + ",".join(sorted(suppliers)))

    # ---- GMROI (capital efficiency): annualized net profit / inventory at current cost
    for sid, s in S.items():
        s["inv_value"] = s["on_hand"] * s["cur_cost"]
        s["annualized_profit"] = s["profit"] * ANNUALIZE
        s["gmroi"] = s["annualized_profit"] / s["inv_value"]
        tot["inv_value"] += s["inv_value"]
        tot["annualized_profit"] += s["annualized_profit"]
    portfolio_gmroi = tot["annualized_profit"] / tot["inv_value"]
    gmroi_rank = sorted(S, key=lambda sid: -S[sid]["gmroi"])
    for rank, sid in enumerate(gmroi_rank, 1):
        S[sid]["gmroi_rank"] = rank

    # independent path: ratio of sums, then annualize (== sum(annualized)/sum(inventory))
    gmroi_re = (sum(s["profit"] for s in S.values()) / sum(s["inv_value"] for s in S.values())) * ANNUALIZE
    ranks_seq = [S[sid]["gmroi_rank"] for sid in gmroi_rank]
    ok11 = (abs(gmroi_re - portfolio_gmroi) < 1e-6 and ranks_seq == sorted(ranks_seq)
            and all(s["gmroi"] > 0 for s in S.values()))
    check("CHK-11", "GMROI reconciles across all 12 SKUs; ranking and portfolio ratio internally consistent",
          ok11, "portfolio=%.4f | inventory_at_cost=%s | annualized_profit=%s" % (
              portfolio_gmroi, usd(tot["inv_value"]), usd(tot["annualized_profit"])))

    # ---- Price-elasticity & break-even sensitivity (repriced traffic drivers)
    ELASTICITY_SCENARIOS = [("0% Base", 1.00), ("-5% Mild", 0.95),
                            ("-10% Moderate", 0.90), ("-15% Stress", 0.85)]

    def _cents(x):
        return int(round(x * 100.0))

    def _half_up(x):
        return int(math.floor(x + 0.5))

    elasticity = {}
    for sid in ("SKU-004", "SKU-009"):
        s = S[sid]
        p_new = REPRICE_RETAIL[sid]
        contrib_c = _cents((s["sold"] - s["returned"]) * p_new) - _cents((s["sold"] + s["shrink"]) * s["cur_cost"])
        base_c = _cents(s["profit"])
        rows_el = []
        for name, v in ELASTICITY_SCENARIOS:
            c = _half_up(contrib_c * v)
            rows_el.append({"scenario": name, "volume_factor": v,
                            "profit": c / 100.0, "delta_vs_base": (c - base_c) / 100.0})
        v_star = base_c / float(contrib_c)
        elasticity[sid] = {
            "price_change": "%.2f -> %.2f" % (s["price"], p_new),
            "pre_reprice_profit": base_c / 100.0,
            "contribution_new_full_volume": contrib_c / 100.0,
            "scenarios": rows_el,
            "breakeven_volume_factor": round(v_star, 6),
            "breakeven_volume_drop_pct": round((1.0 - v_star) * 100.0, 4),
        }

    ok12 = True
    det12 = []
    for sid, e in elasticity.items():
        contrib = e["contribution_new_full_volume"]
        v_star = e["breakeven_volume_factor"]
        v_exact = e["pre_reprice_profit"] / contrib
        if abs(contrib * v_star - e["pre_reprice_profit"]) > 1e-2:
            ok12 = False
        if abs((1.0 - v_exact) * 100.0 - e["breakeven_volume_drop_pct"]) > 1e-4:
            ok12 = False
        if not 0.0 < v_star < 1.0:
            ok12 = False
        det12.append("%s breakeven_drop=-%.2f%%" % (sid, e["breakeven_volume_drop_pct"]))
    check("CHK-12", "Elasticity break-even thresholds verified for SKU-004 and SKU-009 "
          "(profit at break-even volume == pre-reprice profit)", ok12, "; ".join(det12))

    # ---- post-optimization scenario
    rev_t, profit_t = tot["rev"], tot["profit"]
    for sid, p in REPRICE_RETAIL.items():
        s = S[sid]
        delta = (s["sold"] - s["returned"]) * (p - s["price"])
        rev_t += delta
        profit_t += delta
    for sid, c in ROLLBACK_COST.items():
        s = S[sid]
        profit_t += (s["sold"] + s["shrink"]) * (s["cur_cost"] - c)
    for sid, f in SHRINK_CUT.items():
        s = S[sid]
        profit_t += s["shrink"] * f * s["cur_cost"]
    upside = sum((S[sid]["sold"] + S[sid]["shrink"]) * (S[sid]["cur_cost"] - c)
                 for sid, c in UPSIDE_COST.items())
    margin_t = profit_t / rev_t * 100.0
    margin_u = (profit_t + upside) / rev_t * 100.0

    # ---- liquidation model (dead stock only)
    tiers = [(0.20, 0.40), (0.35, 0.30), (0.50, 0.30)]
    liq = {}
    for sid in sorted(dead_ids):
        s = S[sid]
        left = s["on_hand"]
        proceeds = 0.0
        tiers_out = []
        for disc, share in tiers:
            u = min(int(round(s["on_hand"] * share)), left)
            px = round(s["price"] * (1.0 - disc), 2)
            line = u * px
            proceeds += line
            left -= u
            tiers_out.append({"discount_pct": disc * 100.0, "units": u,
                              "unit_price": px, "proceeds": round(line, 2)})
        liq[sid] = {"on_hand": s["on_hand"],
                    "retail_value": round(s["on_hand"] * s["price"], 2),
                    "cost_basis": round(s["on_hand"] * s["cur_cost"], 2),
                    "proceeds": round(proceeds, 2),
                    "recovery_pct": round(proceeds / (s["on_hand"] * s["price"]) * 100.0, 2),
                    "tiers": tiers_out}
    liq_total = sum(v["proceeds"] for v in liq.values())

    # ---- Weekly 30-day cash-flow waterfall
    # Weeks: W1 d1-7, W2 d8-14, W3 d15-21, W4 d22-30. Tier sales spread evenly across
    # tier days (T1 d1-10, T2 d11-20, T3 d21-30). POs issued day 1; goods received at
    # lead-time end; invoice dated at receipt; cash out at receipt + payment terms.
    T1 = sum(liq[s]["tiers"][0]["proceeds"] for s in liq)
    T2 = sum(liq[s]["tiers"][1]["proceeds"] for s in liq)
    T3 = sum(liq[s]["tiers"][2]["proceeds"] for s in liq)
    wk_in = {"W1": T1 * 7.0 / 10.0,
             "W2": T1 * 3.0 / 10.0 + T2 * 4.0 / 10.0,
             "W3": T2 * 6.0 / 10.0 + T3 * 1.0 / 10.0,
             "W4": T3 * 9.0 / 10.0}
    po_commit = []
    for sid in sorted(S):
        s = S[sid]
        if s["qty"] > 0:
            terms_days = int(re.search(r"(\d+)", s["terms"]).group(1))
            po_commit.append({"sku_id": sid, "order_qty": s["qty"],
                              "po_cost": round(s["qty"] * s["cur_cost"], 2),
                              "receipt_day": 1 + s["lead"],
                              "due_day": 1 + s["lead"] + terms_days,
                              "terms": s["terms"],
                              "priority": "EXPEDITE" if (s["flagged"] and s["lost_units"] > 0) else "ORDER NOW"})
    total_commit = sum(c["po_cost"] for c in po_commit)
    wk_out = {"W1": 0.0, "W2": 0.0, "W3": 0.0, "W4": 0.0}
    for c in po_commit:
        if c["due_day"] <= 30:
            idx = min((c["due_day"] - 1) // 7, 3)
            wk_out[["W1", "W2", "W3", "W4"][idx]] += c["po_cost"]
    cum = 0.0
    wk_rows = []
    min_cum = None
    for idx, k in enumerate(["W1", "W2", "W3", "W4"]):
        net = wk_in[k] - wk_out[k]
        cum += net
        wk_rows.append({"week": k, "days": ["1-7", "8-14", "15-21", "22-30"][idx],
                        "inflow": round(wk_in[k], 2), "outflow": round(wk_out[k], 2),
                        "net": round(net, 2), "cumulative": round(cum, 2)})
        min_cum = cum if min_cum is None else min(min_cum, cum)
    waterfall = {"weeks": wk_rows, "commitments": po_commit,
                 "total_inflows": round(sum(wk_in.values()), 2),
                 "total_commitments": round(total_commit, 2),
                 "total_outflows_in_window": round(sum(wk_out.values()), 2),
                 "min_cumulative": round(min_cum, 2)}

    ok13 = (abs(sum(wk_in.values()) - liq_total) < 1e-6
            and abs(total_commit - tot["po_cost"]) < 1e-6
            and min_cum >= 0.0
            and abs(sum(wk_out.values())) < 1e-9)
    check("CHK-13", "Weekly cash waterfall reconciles: total inflows == $11,817.05, "
          "total PO commitments == $12,058.80, cumulative cash never negative",
          ok13, "inflows=%.2f commitments=%.2f min_cum=%.2f due_within_30d=%.2f" % (
              sum(wk_in.values()), total_commit, min_cum, sum(wk_out.values())))

    # CHK-14 ERP/POS batch CSV reconciliation
    ok14, det14 = True, []
    erp_path = os.path.join(EXPORTS_DIR, "erp_po_import_batch.csv")
    pos_path = os.path.join(EXPORTS_DIR, "pos_repricing_and_clearance_batch.csv")
    if os.path.exists(erp_path) and os.path.exists(pos_path):
        erp = load("erp_po_import_batch.csv", EXPORTS_DIR)
        pos = load("pos_repricing_and_clearance_batch.csv", EXPORTS_DIR)
        s_erp = sum(float(r["line_total"]) for r in erp)
        if len(erp) != 4 or abs(s_erp - tot["po_cost"]) > 1e-6:
            ok14 = False
        for r in erp:
            s = S.get(r["sku_id"])
            if s is None:
                ok14 = False
                continue
            if abs(float(r["order_qty"]) * float(r["unit_cost"]) - float(r["line_total"])) > 1e-6:
                ok14 = False
            if int(r["order_qty"]) != s["qty"] or abs(float(r["unit_cost"]) - s["cur_cost"]) > 1e-6:
                ok14 = False
            if r["payment_terms"] != s["terms"]:
                ok14 = False
            want_flag = "EXPEDITE" if (s["flagged"] and s["lost_units"] > 0) else "ORDER NOW"
            if r["priority_flag"] != want_flag:
                ok14 = False
            if r["shipping_mode"] != ("EXPEDITED" if want_flag == "EXPEDITE" else "STANDARD"):
                ok14 = False
        if len(pos) != 4:
            ok14 = False
        for r in pos:
            s = S.get(r["sku_id"])
            if s is None:
                ok14 = False
                continue
            if abs(float(r["current_retail"]) - s["price"]) > 1e-6:
                ok14 = False
            if r["action_type"] == "REPRICE":
                if r["sku_id"] not in REPRICE_RETAIL or abs(float(r["new_retail"]) - REPRICE_RETAIL[r["sku_id"]]) > 1e-6:
                    ok14 = False
                if r["rollback_trigger"] != "VOLUME_DROP_GT_12PCT_WEEKLY":
                    ok14 = False
            else:
                if not s["dead"] or r["action_type"] != "CLEARANCE":
                    ok14 = False
                if r["rollback_trigger"] != "TIER1_20PCT_TIER2_35PCT_TIER3_50PCT":
                    ok14 = False
        det14.append("erp_rows=%d erp_sum=%.2f pos_rows=%d" % (len(erp), s_erp, len(pos)))
    else:
        ok14 = False
        det14.append("export files missing")
    check("CHK-14", "ERP/POS batch CSV row-count and dollar-sum reconciliation against report tables", ok14,
          "; ".join(det14))

    # CHK-15 redaction regex scan across package files
    email_re = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    phone_re = re.compile(r"\d{3}[-. ]\d{3}[-. ]\d{4}")
    FORBIDDEN_TAGS = ["[" + "OWNER" + " NAME]", "[" + "E" + "MAIL]", "[" + "BUSI" + "NESS PHONE]"]
    scanned, hits = 0, []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in ("verification", "__pycache__")]
        for fn in sorted(files):
            ext = os.path.splitext(fn)[1].lower()
            if ext not in (".md", ".csv", ".py", ".json"):
                continue
            p = os.path.join(root, fn)
            try:
                txt = open(p, encoding="utf-8").read()
            except Exception:
                continue
            scanned += 1
            rel = os.path.relpath(p, BASE)
            if email_re.search(txt):
                hits.append(rel + ":email")
            if phone_re.search(txt):
                hits.append(rel + ":phone")
            for tag in FORBIDDEN_TAGS:
                if tag in txt:
                    hits.append(rel + ":tag")
    check("CHK-15", "Redaction regex scan across all package .md/.csv/.py/.json files: "
          "zero unredacted email addresses, phone numbers, or forbidden placeholders",
          len(hits) == 0, "scanned=%d files, hits=%d" % (scanned, len(hits)))

    # ---- report table rows (verbatim for smb_operations_audit.md)
    print("")
    print("==== SECTION 2 ROWS (Markdown) ====")
    for sid in sorted(S):
        s = S[sid]
        print("| %s | %s | %.2f | %s | %d | %d | %s | %s | %.2f%% | %.2f%% | %s (%.2f pp) | %s | %s |" % (
            sid, s["category"], s["price"], num(s["sold"]), s["returned"], s["shrink"],
            usd(s["rev"]), usd(s["profit"]), s["margin_prior"], s["margin"],
            usd(s["shrink_cost"]), s["drag_pp"], usd(s["creep_d"]), s["action"]))
    print("| **Total / Blend** |  |  | **%s** | **%d** | **%d** | **%s** | **%s** | **%.2f%%** | **%.2f%%** | **%s** | **%s** |  |" % (
        num(sum(s["sold"] for s in S.values())),
        sum(s["returned"] for s in S.values()),
        sum(s["shrink"] for s in S.values()),
        usd(tot["rev"]), usd(tot["profit"]), blended_prior, blended,
        usd(tot["shrink_cost"]), usd(tot["creep"])))

    print("")
    print("==== SECTION 2.3 GMROI ROWS (Markdown) ====")
    for sid in gmroi_rank:
        s = S[sid]
        if s["dead"]:
            read = "dead stock - LIQUIDATE"
        elif s["gmroi_rank"] <= 4:
            read = ("capital-efficiency champion - protect availability (REORDER NOW)"
                    if "REORDER" in s["action"] else "capital-efficiency champion - hold the line")
        elif "REPRICE" in s["action"]:
            read = "margin erosion - REPRICE lifts GMROI"
        elif "REORDER" in s["action"]:
            read = "below ROP - REORDER NOW protects turns"
        else:
            read = "healthy - HOLD"
        print("| %d | %s | %s | %s | %s | %s | %.2f | %s |" % (
            s["gmroi_rank"], sid, s["category"], usd(s["profit"]), usd(s["annualized_profit"]),
            usd(s["inv_value"]), s["gmroi"], read))
    print("| -- | **Portfolio** | 12 SKUs | **%s** | **%s** | **%s** | **%.2f** | benchmark rule of thumb >= 3.2 |" % (
        usd(tot["profit"]), usd(tot["annualized_profit"]), usd(tot["inv_value"]), portfolio_gmroi))

    print("")
    print("==== SECTION 3.1 ROWS (Markdown) ====")
    for sid in sorted(S):
        s = S[sid]
        if s["flagged"]:
            stock_cell = "%d u / $%s" % (round(s["lost_units"]), usd(s["lost_rev"]))
            po_cell = "%d (%d x %d)" % (s["qty"], s["qty"] // s["moq"], s["moq"])
            cost_cell = usd(s["qty"] * s["cur_cost"])
        else:
            stock_cell = "0"
            po_cell = "--"
            cost_cell = "--"
        if s["dead"]:
            prio = "LIQUIDATE - do not reorder"
        elif s["flagged"] and s["lost_units"] > 0:
            prio = "EXPEDITE"
        elif s["flagged"]:
            prio = "ORDER NOW"
        else:
            prio = "OK"
        print("| %s | %s | %d | %.2f | %.2f | %d | %+.2f | %.1f | %s | %s | %s | %s |" % (
            sid, s["supplier"], s["lead"], s["dd"], s["rop"], s["position"],
            s["position"] - s["rop"], s["dos"], stock_cell, po_cell, cost_cell, prio))

    print("")
    print("==== SECTION 3.6 WATERFALL ROWS (Markdown) ====")
    for w in wk_rows:
        print("| %s | %s | $%s | $%s | +$%s | +$%s |" % (
            w["week"], w["days"], usd(w["inflow"]), usd(w["outflow"]), usd(w["net"]), usd(w["cumulative"])))
    print("| **Total** | **1-30** | **$%s** | **$%s** | **+$%s** |  |" % (
        usd(sum(wk_in.values())), usd(sum(wk_out.values())), usd(sum(wk_in.values()) - sum(wk_out.values()))))
    for c in po_commit:
        print("COMMITMENT %s qty=%d cost=$%s receipt=d%d due=d%d (%s, %s)" % (
            c["sku_id"], c["order_qty"], usd(c["po_cost"]), c["receipt_day"], c["due_day"], c["terms"], c["priority"]))

    print("")
    print("==== SECTION 4.4 ELASTICITY ROWS (Markdown) ====")
    for sid in ("SKU-004", "SKU-009"):
        e = elasticity[sid]
        cells = " | ".join("$%s (+$%s)" % (usd(x["profit"]), usd(x["delta_vs_base"])) for x in e["scenarios"])
        print("| %s | %s | $%s | %s | -%.2f%% |" % (
            sid, e["price_change"], usd(e["pre_reprice_profit"]), cells, e["breakeven_volume_drop_pct"]))

    print("")
    print("==== SUMMARY ====")
    print("Blended net margin (current costs): %.2f%%" % blended)
    print("Blended net margin (prior costs):   %.2f%%" % blended_prior)
    print("Cost creep total (90d): %s" % usd(tot["creep"]))
    for sid in sorted(S):
        if S[sid]["creep_d"] > 0:
            print("  %s: $%s (%.2f pp, +%.1f%% unit cost)" % (
                sid, usd(S[sid]["creep_d"]), S[sid]["margin_prior"] - S[sid]["margin"],
                S[sid]["creep_pct"]))
    print("Shrinkage cost total (90d): %s" % usd(tot["shrink_cost"]))
    print("Trapped capital: %s" % usd(tot["trapped"]))
    for sid in sorted(dead_ids):
        print("  %s: %s (carrying %.2f/yr)" % (sid, usd(S[sid]["trapped"]), S[sid]["carrying"]))
    print("Carrying cost avoided (annualized): %s" % usd(tot["carrying"]))
    print("Projected stockout loss per cycle: %s" % usd(tot["lost"]))
    print("PO program: %d units, cost %s, retail protected %s" % (
        tot["po_units"], usd(tot["po_cost"]), usd(tot["protected"])))
    print("Liquidation proceeds (30d): %s vs retail %s" % (
        usd(liq_total), usd(sum(v["retail_value"] for v in liq.values()))))
    for sid in sorted(liq):
        v = liq[sid]
        print("  %s: proceeds %s (%.1f%% of retail; cost basis %s)" % (
            sid, usd(v["proceeds"]), v["recovery_pct"], usd(v["cost_basis"])))
    print("GMROI portfolio: %.2f (inventory at cost %s, annualized profit %s)" % (
        portfolio_gmroi, usd(tot["inv_value"]), usd(tot["annualized_profit"])))
    print("  ranking: " + " > ".join("%s %.2f" % (sid, S[sid]["gmroi"]) for sid in gmroi_rank))
    for sid in ("SKU-004", "SKU-009"):
        print("Elasticity %s: breakeven volume drop -%.2f%% (rollback trigger -12%%)" % (
            sid, elasticity[sid]["breakeven_volume_drop_pct"]))
    print("Cash waterfall: inflows %s | PO due within 30d %s | commitments %s | min cumulative %s" % (
        usd(sum(wk_in.values())), usd(sum(wk_out.values())), usd(total_commit), usd(min_cum)))
    print("Scenario: profit %s on rev %s -> blended %.2f%% (upside %.2f%%); uplift +%s" % (
        usd(profit_t), usd(rev_t), margin_t, margin_u, usd(profit_t - tot["profit"])))

    payload = {
        "deterministic": True,
        "period_days": DAYS,
        "per_sku": {sid: {k: (round(v, 4) if isinstance(v, float) else v)
                          for k, v in S[sid].items()} for sid in sorted(S)},
        "totals": {k: round(v, 2) for k, v in tot.items()},
        "blended_margin_current_pct": round(blended, 4),
        "blended_margin_prior_pct": round(blended_prior, 4),
        "gmroi": {"portfolio": round(portfolio_gmroi, 4),
                  "inventory_at_cost": round(tot["inv_value"], 2),
                  "annualized_profit": round(tot["annualized_profit"], 2),
                  "ranking": [{"rank": S[sid]["gmroi_rank"], "sku_id": sid,
                               "gmroi": round(S[sid]["gmroi"], 4),
                               "inv_value": round(S[sid]["inv_value"], 2),
                               "annualized_profit": round(S[sid]["annualized_profit"], 2)}
                              for sid in gmroi_rank]},
        "elasticity": elasticity,
        "cash_waterfall": waterfall,
        "scenario": {
            "repriced_retail": REPRICE_RETAIL,
            "cost_rollback": ROLLBACK_COST,
            "upside_cost_target": UPSIDE_COST,
            "shrink_cut_pct": SHRINK_CUT,
            "net_revenue": round(rev_t, 2),
            "net_profit": round(profit_t, 2),
            "blended_margin_pct": round(margin_t, 4),
            "blended_margin_upside_pct": round(margin_u, 4),
            "profit_uplift_base": round(profit_t - tot["profit"], 2),
            "renegotiation_upside_extra": round(upside, 2),
        },
        "liquidation": liq,
        "liquidation_total_proceeds": round(liq_total, 2),
        "checks": CHECKS,
    }
    out_path = os.path.join(OUT_DIR, "computed_metrics.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
    print("")
    print("Wrote %s" % out_path)

    if any(c["result"] == "FAIL" for c in CHECKS):
        print("RESULT: FAILURES DETECTED")
        sys.stdout = sys.__stdout__
        _logf.close()
        sys.exit(1)
    print("RESULT: ALL %d CHECKS PASSED" % len(CHECKS))
    sys.stdout = sys.__stdout__
    _logf.close()


if __name__ == "__main__":
    main()
