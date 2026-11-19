# Comparative Redline Review — Master Services Agreement

**v1 Original (Vendor paper) vs. v2 Counterparty Markup**

| | |
|---|---|
| Review date | 19 November 2026 |
| Reviewer posture | Senior commercial counsel for the **Vendor** (original drafter of v1). Counterparty is the **Customer** who returned v2. |
| Materials | [MSA_v1_Original.md](contracts/MSA_v1_Original.md) · [MSA_v2_Counterparty_Markup.md](contracts/MSA_v2_Counterparty_Markup.md) |
| Provenance | The two MSA files were not attached. On instruction, two realistic simulated drafts (vendor v1 vs. customer v2) were generated and then comparatively audited. They are not a live third-party paper. Party names, emails, addresses, and monetary figures in v1/v2 are replaced with `[REDACTED_ENTITY]` / `[REDACTED_AMOUNT]`. |
| v1 governing law / forum | Delaware law; AAA arbitration, Wilmington, Delaware; jury/class waiver (v1 §14, p. 11) |
| v2 governing law / forum | California law; exclusive state/federal courts, Santa Clara County; jury/class waiver; arbitration deleted (v2 §14, pp. 11–12) |
| Overall recommendation | **Do not sign v2.** Restore v1 architecture on IP ownership, mutual caps, and mutual termination. Concede limited points (audit, insurance certificates, notice mechanics). Escalate IP assignment of background tools and the uncapped one-sided risk shift — those are walk-away items. |

---

## 1. Redline Comparison Table

Risk is assessed from the Vendor's side. **Legal Impact** is grouped to the requested focus areas: IP ownership, indemnification, liability caps, termination, and jurisdiction, plus payment/acceptance where the commercial effect is equivalent to a risk shift.

### 1.1 High and Medium deltas

| Clause | Original text (v1) | Modified text (v2) | Risk | Legal Impact |
|---|---|---|---|---|
| **§1.1** Background IP<br>v1 p. 2 / v2 p. 2 | Each party retains pre-existing IP, including Vendor Tools and pre-existing libraries. | Any Vendor Background IP “used, incorporated, adapted, or relied upon” in the Services or any Deliverable “is included in ‘Deliverables’ and is assigned to Customer under Section 5.” | **High** | **IP ownership.** Converts a retention clause into a present assignment of the Vendor’s platform. “Relied upon” captures tools that are not even embedded (e.g., internal CI/CD, pretrained models). This is an alienation of the Vendor’s going-concern assets, not a work-product grant. |
| **§1.2** Deliverables<br>v1 p. 2 / v2 p. 2 | Work product expressly identified in an SOW, **excluding** Vendor Tools, Background IP, generic methodologies, and residual know-how. | “All work product… source code, object code, models, weights, configurations… improvements, modifications, derivatives,” **including Vendor Tools and Background IP used or incorporated**, excluding only separately licensed third-party materials. | **High** | **IP ownership.** The defined term swallows the tools. Combined with §5.2, every engagement becomes a de facto acquisition of the Vendor’s stack. Weights and models also raise export-control and OSS issues (see Edge Case 3). |
| **§1.3** IP; moral rights<br>v1 p. 2 / v2 p. 2 | Standard IP definition. | Adds a blanket waiver of “all rights of attribution and integrity… as to all Deliverables.” | **Medium** | **IP ownership.** U.S. moral rights (VARA, 17 U.S.C. §106A) generally do not attach to computer programs or works made for hire (17 U.S.C. §101, “work of visual art” exclusion). The waiver is mostly surplus, but the drafting signals Customer will resist any residual authorship claim. Human counsel should confirm no state-law moral-rights overlay is intended. |
| **§1.4** Services<br>v1 p. 2 / v2 p. 2 | Professional services described in an SOW. | Includes “all invention, authorship, and development activity… whether during or outside normal business hours, and whether or not using Vendor resources.” | **High** | **IP ownership.** Reaches off-hours and non-Vendor-resource work. If any Vendor author is a California employee, Cal. Lab. Code § 2870(a) makes that assignment unenforceable as to inventions developed entirely on the employee’s own time without employer resources, except the two statutory carve-outs; § 2870(b) declares a contrary covenant void as against public policy. See Edge Case 1. |
| **§1.5** Vendor Tools<br>v1 p. 2 / v2 p. 2 | Vendor’s proprietary software, SDKs, agents, pipelines, pretrained models, including improvements. | Adds: “Vendor Tools created, improved, or refined in the course of the Services are Deliverables.” | **High** | **IP ownership.** Any improvement to a tool while a SOW is open — even a general-purpose improvement — becomes Customer-owned. This is how a services customer acquires the product. |
| **§2.2** Order of precedence<br>v1 p. 2 / v2 p. 2 | Agreement > SOW > exhibits; a SOW may override a specified Section only if it identifies the Section by number. | SOW > Agreement; a SOW controls “even if it does not identify the overridden Section.” | **Medium** | Opens the MSA to silent override by a business-side SOW. Commercial, not doctrinal, but it is how IP and liability protections die in the exhibit. |
| **§3.1–3.4** Acceptance<br>v1 p. 3 / v2 p. 3 | 10 Business Days; deemed acceptance if no written rejection; one resubmission cycle; production use = acceptance. | 30 Business Days, extendable for “additional testing” or incomplete documentation; **no deemed acceptance**; a further 30-Business-Day window after production use for “previously undiscoverable” defects; **unlimited** rejection cycles; written acceptance may be withheld in Customer’s “reasonable discretion”; production use ≠ acceptance. | **High** | **Payment trigger / termination analogue.** Without deemed acceptance, Vendor can be held in an endless pre-revenue loop. Fees in v2 are invoiced “upon Acceptance” (§4.1), so acceptance failure is a payment failure. This is a concealed termination and cash-flow weapon. |
| **§4.1–4.2** Fees; net terms<br>v1 pp. 3–4 / v2 pp. 3–4 | Monthly in advance (fixed-fee) or monthly in arrears (T&M); **net 30**; disputes must be noticed in 15 days with particularity. | Invoiced **upon Acceptance** of the milestone/Deliverable; **net 90**; Customer may dispute “at any time before payment” and withhold anything “reasonably related to a rejection, dispute, open defect, or pending audit.” | **High** | **Payment triggers.** Shifts working capital from Vendor to Customer by up to a quarter, and the withhold is not limited to the disputed line item. Combined with §3, Vendor can deliver and still not be entitled to invoice. |
| **§4.3** Late payment / suspension<br>v1 p. 4 / v2 p. 4 | 1.5%/month; suspend on 10 days’ notice if undisputed amounts remain unpaid. | 1%/month, only after a **second** notice plus 15 further days; suspend on 30 days’ notice, and not if Customer has invoked dispute, audit, or rejection. | **Medium** | Removes the only practical self-help remedy. A customer that perpetualizes “dispute” or “rejection” is immunized from suspension. |
| **§4.5** Set-off<br>v1 p. 4 / v2 p. 4 | No set-off except amounts finally determined by a court or tribunal. | Unlimited good-faith set-off, “whether or not liquidated,” including refund, indemnity, warranty, and audit claims. | **High** | Converts every invoice into an unsecured, self-help recovery account for unadjudicated claims. Collides with the (already one-sided) liability architecture in §10. |
| **§4.7–4.8** Audit; holdback *(new in v2)*<br>v2 p. 4 | *(not present)* | Audit on 10 days’ notice, twice per year, for 3 years post-term; Vendor pays audit cost if overcharge > 5%. **20% holdback** on each fixed-fee invoice until 90 days after final Acceptance. | **High** | **Payment triggers.** A 20% holdback on an [REDACTED_AMOUNT] fixed fee is material float. Release is conditioned on “no open defects,” which Customer controls under §3. |
| **§5.1** Assignment of Background IP / Tools<br>v1 p. 4 / v2 p. 4 | Each party retains its Background IP and Vendor Tools; only limited licenses are granted. | Vendor “hereby assigns” to Customer all right, title, and interest in Vendor Background IP and Vendor Tools “used, incorporated, adapted, or relied upon” in the Services or any Deliverable, “including all improvements, derivatives, and modifications… whether created before, during, or after the term.” | **High** | **IP ownership — walk-away.** A present assignment of pre-existing tools, plus future improvements “after the term,” is an acquisition of the Vendor’s product, not a services deal. Written-instrument issues under 17 U.S.C. §204(a) do **not** save the commercial intent; they only create a later enforceability fight (Edge Case 1). |
| **§5.2** Work product / work made for hire<br>v1 p. 4 / v2 p. 5 | Assignment of **Deliverables only**, upon payment; WMFH “to the extent required to effect the assignment.” | All Deliverables are WMFH with Customer as author; fallback irrevocable assignment of **all** IP including patents, trade secrets, trademarks, and moral rights; Customer appointed attorney-in-fact if Vendor does not sign within 10 days; no additional payment. | **High** | **IP ownership.** (a) Independent-contractor software is usually **not** WMFH: 17 U.S.C. §101(2) confines commissioned WMFH to nine enumerated categories and requires a signed written instrument; a general “software implementation” is not on the list (Edge Case 1). (b) The attorney-in-fact appointment plus “unreasonably requested” documents is a red flag. (c) Assignment “upon payment” in v1 was a security interest analogue; v2 strips that condition. |
| **§5.3** License to Customer *(deleted)*<br>v1 p. 5 / v2 p. 5 | Perpetual, non-exclusive, internal-use license to Vendor Tools/Background IP **as embedded**, no source, no reverse engineering. | **[DELETED — “Customer receives ownership, not a license.”]** | **High** | **IP ownership.** Even if Customer “owns” Deliverables, Vendor still needs a license **back** to its own tools to serve other customers and to support this one. Deletion of the grant-back is how a vendor is locked out of its own platform. |
| **§5.4** Residual knowledge *(deleted)*<br>v1 p. 5 / v2 p. 5 | Vendor may use Residual Knowledge (unaided memory; excludes Customer CI and source). | **[DELETED]** | **High** | **IP ownership / confidentiality.** Residual-knowledge clauses are the standard accommodation for the fact that engineers cannot unlearn. Deleting them, and then treating unaided-memory use as a **breach of confidentiality** (v2 §7.4), criminalizes ordinary professional experience. |
| **§5.5** Open source<br>v1 p. 5 / v2 p. 5 | OSI OSS permitted; no copyleft contamination of Customer-proprietary code; OSS notice. | **No OSS without prior written consent, withholdable in sole discretion**; warranty that no Deliverable is subject to copyleft; **uncapped** indemnity for any OSS claim. | **High** | **IP ownership + indemnification.** A “no OSS” warranty is often factually impossible for a modern stack. Assignment of tools that contain OSS may deliver Customer code subject to GPL/AGPL rather than proprietary title (Edge Case 3). Uncapped indemnity for “any OSS claim” is an open-ended IP risk shift. |
| **§5.6–5.7** Feedback; reservation<br>v1 p. 5 / v2 p. 5 | Perpetual license to Vendor to use Feedback; rights not granted are reserved. | Customer owns Feedback (assignment); reservation runs “by Customer.” | **Medium** | Feedback assignment is usually acceptable if confined to Customer-specific Feedback and if Vendor retains the right to use generic know-how. As drafted, it is another leak into §5.4’s deletion. |
| **§6.2–6.3, 6.5** Security; breach notice; return<br>v1 p. 6 / v2 p. 6 | Industry-standard safeguards; 72-hour notice of **confirmed** breach; DPA if required. | NIST CSF + SOC 2 Type II + “any standard specified by Customer in writing”; 24-hour notice of **suspected or confirmed** breach, including constructive knowledge; return/delete Customer Data in 5 Business Days. | **Medium** | A Customer-written security exhibit that Vendor has never seen is an open-ended warranty. 24-hour “should have known” notice of a **suspected** incident is operationally unrealistic and feeds the uncapped §9.1(b) data indemnity. |
| **§7.2, 7.4–7.5** Confidentiality<br>v1 p. 6 / v2 pp. 6–7 | 5-year survival; trade secrets for so long as they remain trade secrets; residual knowledge excluded. | **Perpetual**; residual knowledge **not** excluded; unaided-memory use “is a breach”; all Customer information treated as Confidential whether or not marked. | **High** | Perpetual contractual confidentiality for non-trade-secrets is overbroad and can conflict with employee mobility. Treating professional skill as Customer CI is an IP grab by another name. |
| **§8.2, 8.4** Warranties<br>v1 p. 7 / v2 p. 7 | 90-day material-conformity warranty; exclusive remedy re-perform or refund the non-conforming Deliverable. | **24 months**, “conform **in all respects**,” “highest standards of the industry”; exclusive remedy is re-performance **or refund of all fees paid under the SOW plus cover costs**, at **Customer’s** option. New warranty of non-infringement and compliance with “all applicable laws… of each jurisdiction in which Customer operates or sells.” | **High** | “In all respects” + 24 months + full-SOW refund is a disguised performance bond. The multi-jurisdiction compliance warranty is an export/sanctions/privacy trap (Edge Case 3). It also feeds uncapped §9.1. |
| **§9.1** Vendor indemnity<br>v1 pp. 7–8 / v2 p. 8 | Defend/indemnify for third-party claims that a Deliverable **as delivered and used in accordance with the Agreement** infringes IP; **subject to §10** (cap at 2× Liability Cap). | Defend/indemnify for **any** third-party claim arising out of the Services or Deliverables (IP **or any other right**), Personal Data Breach / privacy law, bodily injury/property damage on Customer sites, and **any act or omission of Vendor personnel**; **all** damages including attorneys’ fees; **“without any cap or limitation.”** | **High** | **Indemnification — walk-away.** Four expansions, each independently material: (1) from IP infringement to **any** third-party claim; (2) from deliverable-infringement to **any act or omission of personnel** (a negligence indemnity); (3) uncapped; (4) covers affiliates and officers. This is not an IP indemnity. It is a wholesale transfer of operational risk. |
| **§9.2** Indemnity exclusions<br>v1 p. 7 / v2 p. 8 | No obligation to the extent the claim arises from Customer Data/specs/combinations, out-of-scope use, third-party modifications, or conforming OSS. | No obligation **only** to the extent the claim is **solely and directly** caused by Customer’s **willful misconduct**, and only if Customer gave notice within 10 days of first knowledge. | **High** | **Indemnification.** Ordinary Customer-caused infringement (Customer specs, Customer Data, Customer combinations) is now Vendor’s uncapped problem. The “solely and directly” + “willful” + 10-day-notice triple condition makes the exclusion illusory. |
| **§9.3** Customer indemnity<br>v1 p. 8 / v2 p. 8 | Customer indemnifies for Customer Data, Customer specs/instructions, and out-of-scope use; subject to §10. | Narrowed to Customer Data “to the extent caused by Customer Data”; **capped at the Liability Cap**; no defense obligation stated for specs or misuse. | **High** | **Indemnification.** The reciprocal is gutted and then capped, while Vendor’s side is uncapped. Asymmetric indemnity is a classic later-stage unenforceability / unconscionability fact, but the first-order commercial problem is the risk shift itself. |
| **§9.4** Procedure<br>v1 p. 8 / v2 p. 8 | Prompt notice, cooperation, indemnifying party controls defense; no settlement imposing non-monetary obligations without consent. | Notice within **10 days of first knowledge or the indemnity is forfeited**; Customer may **assume control of any claim at any time**; **no settlement on any terms** without Customer’s prior written consent. | **High** | **Indemnification.** A forfeiture clause tied to 10-day actual knowledge is a trap (claims often arrive as vague letters). Customer control of Vendor’s defense, including of claims Vendor is paying, is incompatible with privilege and with Vendor’s insurance. |
| **§9.5** Infringement remedy *(deleted)*<br>v1 p. 8 / v2 p. 8 | Procure / replace / terminate-and-refund; exclusive remedy for IP infringement. | **[DELETED]** | **High** | **IP + indemnification.** The exclusive-remedy structure is what keeps an IP claim from becoming an unlimited direct-damages claim. Deleting it, while expanding §9.1, removes the design. |
| **§10.1** Consequential damages<br>v1 p. 8 / v2 p. 9 | **Mutual** exclusion of indirect, incidental, special, consequential, punitive damages, lost profits. | **One-way** (Vendor → Customer only), and the exclusion **does not apply** to indemnity, warranty, IP, confidentiality, data-protection, **or negligence**, or any claim for which **insurance is required** under §12. | **High** | **Liability caps.** The negligence and insurance carve-outs swallow the rule. Almost every commercial damages theory can be pled as negligence, and §12 now requires large cyber/E&O towers, so “claims covered by insurance” is nearly everything. Vendor remains exposed to lost-profits claims. |
| **§10.2** Liability cap<br>v1 p. 9 / v2 p. 9 | **Mutual** cap = fees paid or payable under the applicable SOW in the 12 months preceding the first event. Carve-outs: fraud/willful misconduct; IP infringement/misappropriation of the **other party’s** IP; Customer’s payment obligations; Vendor’s §9.1 indemnity **capped at 2×**. | **Vendor’s** liability **uncapped** for: (a) all indemnity; (b) any breach of §§5, 6, 7, or 8; (c) gross negligence or willful misconduct; (d) **any claim covered by insurance**; (e) “Customer’s direct damages of any kind.” **Customer’s** liability capped, carve-out only for fraud. | **High** | **Liability caps — walk-away.** Clause (e) (“direct damages of any kind” uncapped) nullifies the cap for the claims Customer actually brings. Clause (d) outsources the cap to an insurer’s coverage decision. The “applicable SOW” base is also smaller than an Agreement-wide 12-month lookback, so even the residual cap is thin. |
| **§11.1** Term / non-renewal<br>v1 p. 9 / v2 p. 9 | Initial term 24 months; auto-renew 12; 60 days’ non-renewal notice. | Initial term **12 months**; auto-renew 12; **90 days’** non-renewal notice. | **Medium** | Shorter committed term increases Vendor’s revenue volatility; longer non-renewal notice is a modest operational cost, not a legal defect. Acceptable if the rest of §11 is repaired. |
| **§11.2** Termination for convenience<br>v1 p. 9 / v2 p. 10 | **Either** party, **90 days’** notice; Customer pays for work performed; prepaid fees for undelivered fixed-fee Deliverables **non-refundable**. | **Customer only**, **15 days’** notice; Vendor **may not** terminate for convenience; refund of **all prepaid fees including work in process within 10 Business Days**; Vendor waives wind-down costs, lost profits, and termination fees. | **High** | **Termination.** A 15-day unilateral off-ramp plus a full refund is an option, not a commitment. Combined with §5.2 (assignment not conditioned on full payment) and §11.4(e) (deliver incomplete work), Customer can take the work product and walk. |
| **§11.3** Termination for cause<br>v1 p. 10 / v2 p. 10 | Either party; 30-day cure after particularized notice; immediate for insolvency. | **Customer:** immediate, **no notice, no cure**, for any material breach, **any** breach of §§5/6/7 whether or not material, insolvency, **or any act Customer “reasonably determines” puts its systems, data, or reputation at risk.** **Vendor:** 60-day cure, **SOW-only**, not the Agreement. | **High** | **Termination.** The “reputation at risk” trigger is a subjective termination right. Deleting cure for IP/confidentiality/data breaches means a good-faith dispute about whether a breach occurred becomes an immediate kill switch — which then triggers the §11.4 refund and free-transition machinery. |
| **§11.4** Effect of termination<br>v1 p. 10 / v2 p. 10 | Embedded-tool license survives; pay accrued fees in 30 days; return CI; specified survival. | All Customer licenses survive in perpetuity; pay accepted-work fees in **90 days**; Customer may retain archival/litigation-hold copies; **Vendor must deliver all work in process, source, credentials, and incomplete items within 5 Business Days**; **Vendor shall not delete, encrypt, or withhold any Customer system or Deliverable as self-help.** | **High** | **Termination + IP.** Forced delivery of incomplete work and a ban on self-help (even for non-payment) leaves Vendor with an accounts-receivable claim and no leverage. Survival of §§5/6/7/8/9/10 means the uncapped risk shift **outlives** the deal. |
| **§11.5** Transition<br>v1 p. 10 / v2 p. 10 | 30 days, at then-current rates, reasonable assistance. | **90 days, at no charge**, up to **40 hours per week**, including knowledge transfer, meetings, and engineering support. | **High** | **Termination.** Unpaid 90-day / 40-hour-per-week transition is a second, involuntary SOW. At senior-engineer rates this is a material uncompensated cost, and it is available even after Customer’s no-fault walk. |
| **§12** Insurance<br>v1 p. 10 / v2 p. 11 | CGL and cyber/E&O of [REDACTED_AMOUNT] each; 2-year tail; certificates on request; insurance does not cap liability except as in §10. | CGL [REDACTED_AMOUNT], cyber/E&O [REDACTED_AMOUNT], umbrella [REDACTED_AMOUNT]; 5-year tail; Customer as additional insured; primary/non-contributory; 30 days’ cancellation notice; certified policy copies; **insurance does not cap liability.** | **Medium** | Additional-insured status and primary/non-contributory wording are negotiable and often insurable. The interaction with v2 §10.2(d) (uncapped for “any claim covered by insurance”) is the real problem: it makes the existence of coverage a reason to **remove** the cap, which is backwards. |
| **§13.2** Non-solicit<br>v1 p. 10 / v2 p. 11 | 12 months; standard general-solicitation carve-out. | 24 months; Customer may hire any Vendor contractor/employee who applies generally or whom Vendor has terminated. | **Low** | California enforced non-solicits narrowly even before the 2023–24 employee-mobility statutes; a 24-month covenant is likely unenforceable as to California workers. Low commercial priority. |
| **§14.1** Governing law<br>v1 p. 11 / v2 p. 12 | Delaware law, excluding conflicts and CISG. | **California** law, excluding conflicts and CISG. | **High** | **Jurisdiction.** California choice of law plus California forum is a package. It imports Cal. Civ. Code §1668 (no contractual exemption for fraud, willful injury, or violation of law), employee-invention statutes, and **Grafton Partners** (no pre-dispute jury waiver). See Edge Case 2. |
| **§14.3–14.5** Forum; fees<br>v1 p. 11 / v2 p. 12 | Informal escalation (15 days); **binding AAA arbitration** in Wilmington; jury and class waiver; injunctive-relief carve-out; proceedings confidential. | Informal escalation retained; **exclusive state/federal courts in Santa Clara County**; **jury waiver**; class waiver; arbitration **deleted**; **prevailing-party attorneys’ fees**. | **High** | **Jurisdiction.** Losing confidential arbitration and gaining a public Santa Clara docket plus fee-shifting is a strategic loss. The jury waiver is likely **void** under *Grafton Partners L.P. v. Superior Court*, 36 Cal. 4th 944 (2005), and *In re County of Orange*, 784 F.3d 520 (9th Cir. 2015) (federal court sitting in diversity applies California law and holds the waiver unenforceable). v2 therefore gives Customer a California jury **and** a fee-shifting clause, the opposite of what the waiver paper implies. See Edge Case 2. |
| **§15.2** Assignment<br>v1 p. 12 / v2 p. 12 | Either party may assign to a successor in a sale/merger upon notice; otherwise with consent not unreasonably withheld. | **Vendor may not assign**, including by change of control, without consent **withholdable in sole discretion**. **Customer may assign freely** to affiliates or acquirers upon notice. Purported Vendor assignment is void. | **High** | Blocks a sale of the Vendor (the very exit the IP grab makes more likely). Change-of-control consent in “sole discretion” is a poison pill in the M&A context. |
| **§15.6** Force majeure<br>v1 p. 12 / v2 p. 13 | Payment and performance excused (except payment) for events beyond reasonable control. | Force majeure “does not excuse Vendor’s data-protection, confidentiality, or indemnity obligations.” | **Medium** | A ransomware event or nation-state incident is exactly when a vendor needs force majeure. Refusing to excuse data/confidentiality duties during force majeure collides with the uncapped §9.1(b) indemnity. |

### 1.2 Low deltas (for completeness)

| Clause | Delta | Risk | Legal Impact |
|---|---|---|---|
| §2.1 professional standard | “generally accepted” → “highest standards” | Low | Marketing language that becomes a warranty through §8. |
| §4.4 taxes | Adds cooperation on withholding | Low | Acceptable. |
| §5.2 attorney-in-fact | Customer may sign assignment documents if Vendor misses a 10-day window | High (already in §5.2) | Prefer a bilateral “further assurances” clause with a reasonable cure. |
| §6.4 DPA | Vendor’s form → Customer’s form | Medium | Paper choice often decides breach-notice, audit, and subprocessor terms. |
| §7.1 care standard | “reasonable care” → “highest degree of care” | Low | Feeds the perpetual-CI breach theory in §7.4. |
| §15.1 notices | Customer requires copy to [REDACTED_ENTITY] and forbids individual-only notice | Low | Acceptable; update the notice block. |

### 1.3 Quantitative Risk & Cash-Flow Comparison (v1 vs. v2)

Day-count assumptions: 1 Business Day = 1 weekday; 30 Business Days = 42 calendar days (no holiday adjustment). Monetary amounts are `[REDACTED_AMOUNT]`. “Full cash” means the last dollar of a milestone invoice, including holdback release.

| Dimension | v1 Original | v2 Counterparty Markup | Delta (Vendor) |
|---|---|---|---|
| **(a) IP Ownership Scope** | Custom Deliverables assigned **upon payment**; Vendor Tools and Background IP **retained**; grant-back license to Customer for embedded tools; residual-knowledge clause; OSI OSS permitted | Present assignment of Background IP and Vendor Tools “used, incorporated, adapted, or relied upon,” including improvements **after the term**; off-hours / non-Vendor-resource work; no grant-back; residual knowledge deleted; no OSS without sole-discretion consent | **Walk-away.** Services deal becomes a product acquisition. WMFH recital is the wrong Copyright Act box (*Reid*). Cal. Lab. Code § 2870 independently voids the off-hours grab as to California employees. |
| **(b) Liability Cap & Carve-Outs** | **Mutual** cap = 12 months’ fees under the applicable SOW. Mutual consequential exclusion. Carve-outs: fraud / willful misconduct; IP of the other party; Customer’s payment; Vendor IP indemnity **capped at 2×** | **One-way.** Vendor uncapped for indemnity, §§5/6/7/8, gross negligence, **insurance-covered claims**, and “direct damages of any kind.” Customer still capped; carve-out only for fraud. Consequential exclusion does not apply to negligence or insured claims | **Walk-away.** Clause (e) nullifies the cap on the claims Customer actually brings. Clause (d) outsources the cap to coverage. Cal. Civ. Code § 1668 independently voids any exculpation for fraud, willful injury, or violation of law. |
| **(c) Indemnification Scope** | Vendor: third-party IP infringement by a Deliverable **as delivered and used in accordance with the Agreement**, subject to §10 (2× cap); standard exclusions; exclusive procure/replace/refund remedy. Customer: reciprocal for Customer Data, specs, out-of-scope use | Vendor: **any** third-party claim (IP **or any other right**), data/privacy, bodily injury, **any act or omission of personnel**; **uncapped**. Exclusions nearly eliminated. Customer indemnity gutted and **capped**. 10-day notice **forfeits** the indemnity. Customer may seize defense | **Walk-away.** Not an IP indemnity. It is a wholesale operational-risk transfer. |
| **(d) Termination & Transition Cost** | Either party, **90 days’** convenience; pay for work performed; prepaid non-refundable; 30-day cure; 30-day **paid** transition | Customer only, **15 days’** convenience; refund of **all prepaid including work in process in 10 Business Days**; no-cure immediate cause (including “reputation at risk”); **90 days unpaid** transition up to 40 h/week; deliver incomplete work in 5 Business Days; no self-help | **Walk-away.** Option, not a commitment. Combined with §5.2, Customer can take the work product and walk. |
| **(e) Dispute Forum & Fee-Shifting** | Delaware law; confidential AAA arbitration, Wilmington; jury/class waiver; each party bears own costs | California law; exclusive Santa Clara state/federal courts; jury waiver (**void** under *Grafton* and *In re County of Orange*); class waiver; **prevailing-party fees**; public docket | **High.** Jury waiver is void even in federal diversity court. Fee-shifting plus a jury is a litigation-finance gift. |
| **(f) Working-Capital Conversion Cycle** | Fixed-fee invoiced **monthly in advance**; **net 30**; deemed acceptance at **10 Business Days** (does not gate invoicing); **no holdback**. First cash ≈ invoice + 30 calendar days. Cash can precede delivery. | Invoice **only upon Acceptance**; **net 90**; **20% holdback** until **90 days after final Acceptance**; no deemed acceptance; unlimited rejection. First cash (80% of first milestone) ≈ delivery + 42 + 90 = **132 calendar days (~4.4 months)**. Last cash (holdback on early invoices of a 180-day SOW) ≈ project start + 180 + 42 + 90 = **312 calendar days (~10.4 months)**. See cash math below. | **High.** Vendor funds the build. Customer controls the Acceptance gate. |

**Working-capital day-count (fixed-fee SOW, Vendor cash).**

**v1.** Invoice monthly in advance → cash at invoice + 30 calendar days. Acceptance (10 Business Days, deemed if silent) is a quality gate, not an invoicing gate. No holdback. On a 180-day SOW the Vendor is paid in advance monthly; last invoice can precede final delivery.

**v2, first 80% of first milestone (clean cycle, no rejection, no extension).**

| Step | Clock | Calendar days from delivery |
|---|---|---|
| Delivery | T0 | 0 |
| Acceptance Period (30 Business Days) | T0 → T+42 | 42 |
| Invoice issued | T+42 | 42 |
| 80% paid (net 90) | T+42+90 | **132 (~4.4 months)** |

**v2, last 20% (holdback), single-Deliverable SOW.** Holdback releases 90 days after **final** Acceptance. If the only Acceptance is T+42, holdback release is T+42+90 = **132 days**, coincident with the 80% payment.

**v2, last 20% (holdback), 180-day SOW (SOW-001 shape).** Work starts 1 March 2027. Final delivery ≈ 28 August 2027 (180 calendar days). Final Acceptance if timely ≈ 28 August + 42 calendar days ≈ 9 October 2027. Holdback on **all** invoices releases ≈ 9 October + 90 = **7 January 2028**. From project start to last cash ≈ **312 days (~10.4 months)**. Holdback on an early invoice waits for that date; it does not ride that invoice’s own net-90.

**Sequential vs. parallel.** 30 Business Days + net-90 run in series (Acceptance gates the invoice). The 90-day holdback runs **in parallel** with net-90 from final Acceptance, and **in series after** earlier Acceptances. Adding 30+90+90 as if all three were sequential overstates a single-milestone cycle and understates a multi-milestone holdback tail.

**Customer lever.** Every extra rejection cycle restarts the 30 Business Days. Every “additional testing” extension does the same. Unlimited set-off (§4.5) can stop even the 80%.

---

## 2. Fact & Obligation Timeline

All items below are extracted from **v2 only**. Dates marked *relative* run from a trigger (Effective Date, invoice, Acceptance, termination notice, first knowledge). SOW-001 target start is 1 March 2027 with an estimated 180-day duration (v2 p. 14); no calendar deadlines can be fixed until the Effective Date and each Acceptance date are known.

| # | When / trigger | Obligation, deadline, notice, or payment trigger | Source | Type |
|---|---|---|---|---|
| 1 | Effective Date | Agreement commences; initial term of **12 months** begins | v2 §11.1, p. 9 | Term |
| 2 | On or before Effective Date | Vendor may not use **any OSS** in a Deliverable without Customer’s **prior written consent** | v2 §5.5, p. 5 | Condition / consent |
| 3 | During performance | Vendor must meet NIST CSF, SOC 2 Type II, and any Customer-specified security standard | v2 §6.2, p. 6 | Standing covenant |
| 4 | Annually | Vendor shall complete a SOC 2 Type II audit and deliver the report | v2 §6.2, p. 6 | Recurring deliverable |
| 5 | **24 hours** after Vendor knew or reasonably should have known of a suspected or confirmed Personal Data Breach | Written notice to Customer | v2 §6.3, p. 6 | Notice period |
| 6 | **10 days** after Customer request | Vendor must execute IP assignment documents, failing which Customer may sign as attorney-in-fact | v2 §5.2, p. 5 | Deadline / fallback authority |
| 7 | Each Deliverable submission | **30 Business Day** Acceptance Period begins, extendable for additional testing or incomplete documentation | v2 §3.1, p. 3 | Review window |
| 8 | Within the Acceptance Period, **or 30 Business Days after production use** | Customer may reject (no deemed acceptance; unlimited cycles) | v2 §3.2–3.3, p. 3 | Rejection / payment blocker |
| 9 | Upon Customer Acceptance of a milestone / Deliverable | Fixed-fee milestone **invoiced** (not before) | v2 §4.1, p. 3 | **Payment trigger** |
| 10 | Invoice date | Payment due **net 90 days** | v2 §4.2, p. 3 | **Payment deadline** |
| 11 | Any time before payment | Customer may dispute and withhold amounts related to rejection, dispute, open defect, or pending audit | v2 §4.2, p. 3 | Withhold right |
| 12 | Each fixed-fee invoice | Customer withholds **20% holdback** until **90 days after final Acceptance** of the SOW, and only if no open defects remain | v2 §4.8, p. 4 | **Payment trigger / hold** |
| 13 | Second written past-due notice + **15 additional days** | 1% monthly interest begins on undisputed past-due amounts | v2 §4.3, p. 4 | Interest trigger |
| 14 | **30 days’** written notice, and only if Customer has not invoked dispute/audit/rejection | Vendor may suspend Services for non-payment | v2 §4.3, p. 4 | Suspension notice |
| 15 | **10 days’** notice; max **twice per year**; books retained **3 years** after term | Customer audit of fee-related records | v2 §4.7, p. 4 | Audit notice |
| 16 | **24 months** after Acceptance of a Deliverable | Conformity warranty runs (material → “in all respects”); exclusive remedy includes full-SOW refund plus cover | v2 §8.2, p. 7 | Warranty window |
| 17 | **10 days** after a Party first knew of a third-party claim | Indemnity notice, **or the indemnity is forfeited** | v2 §9.4, p. 8 | Notice period / forfeiture |
| 18 | Any time | Customer may assume control of any indemnified claim; no settlement without Customer consent | v2 §9.4, p. 8 | Defense control |
| 19 | **15 days** of executive escalation | Informal dispute conference | v2 §14.2, p. 11 | Pre-suit step |
| 20 | **90 days** before the end of the then-current term | Written notice of non-renewal (else auto-renews 12 months) | v2 §11.1, p. 9 | Notice period |
| 21 | **15 days’** prior written notice (**Customer only**) | Termination for convenience; Vendor has no convenience right | v2 §11.2, p. 10 | Termination notice |
| 22 | **10 Business Days** after convenience termination | Vendor shall refund **all prepaid fees, including work in process** | v2 §11.2, p. 10 | **Payment trigger (refund)** |
| 23 | Immediate, **no notice, no cure** | Customer may terminate for material breach, any breach of §§5/6/7, insolvency, or any act Customer reasonably determines puts its systems, data, or reputation at risk | v2 §11.3, p. 10 | Termination trigger |
| 24 | **60 days** after particularized notice | Vendor’s only cause remedy: terminate the **affected SOW** for Customer’s uncured material breach | v2 §11.3, p. 10 | Cure period |
| 25 | **5 Business Days** after termination | Vendor shall deliver all work in process, source code, credentials, documentation, including incomplete items; return or delete Customer Data and certify | v2 §11.4(e), p. 10; §6.5, p. 6 | Delivery / deletion deadline |
| 26 | **90 days** after termination | Customer pays accrued unpaid fees for **accepted** Deliverables | v2 §11.4(b), p. 10 | **Payment deadline** |
| 27 | **90 days** after termination notice, **at no charge**, up to **40 hours/week** | Transition assistance (knowledge transfer, meetings, engineering) | v2 §11.5, p. 10 | Uncompensated obligation |
| 28 | During term + **5 years** | Maintain CGL, cyber/E&O, umbrella; Customer additional insured; **30 days’** notice of cancellation | v2 §12.1, p. 11 | Insurance covenant / notice |
| 29 | During term + **24 months** | Non-solicit (with Customer hiring carve-outs) | v2 §13.2, p. 11 | Post-term covenant |
| 30 | Perpetual | Confidentiality obligations; residual-knowledge use is a breach | v2 §7.2, 7.4, pp. 6–7 | Survival |
| 31 | Perpetual | Survival of §§5, 6, 7, 8, 9, 10, 11.4, 12, 14, 15 (uncapped risk shift outlives the deal) | v2 §11.4(d), p. 10 | Survival |
| 32 | SOW-001 target start **1 March 2027**; estimated duration **180 days** | Illustrative engagement; fees invoiced on Acceptance, subject to 20% holdback | v2 p. 14 | Project dates |
| 33 | Any purported Vendor assignment | Void unless Customer consents in its sole discretion | v2 §15.2, p. 12 | Restriction on exit |

**Cash-conversion sketch (Vendor, v2, fixed-fee SOW).** Deliver → wait for discretionary Acceptance (30 Business Days, extendable, no deemed acceptance) → invoice → wait net 90 → 20% remains held until 90 days after *final* Acceptance. In a clean cycle that is **132 calendar days (~4.4 months) from delivery on a single milestone, and up to 312 calendar days (~10.4 months) from project start to final holdback release on a 180-day SOW (see §1.3)**, before any rejection cycle, audit, or set-off. Under v1 the same cycle was invoice monthly in advance / net 30, with deemed acceptance at day 10.

---

## 3. Redacted Executive Memo

> **Privileged and confidential — attorney work product.**
> Prepared for the Vendor board / deal team. All legal-entity names, personal names, email addresses, street addresses, and financial figures are redacted. Entity/contact/address placeholders are `[REDACTED_ENTITY]`; monetary figures are `[REDACTED_AMOUNT]`. Roles (“Vendor” / “Customer”) are retained for readability. The same redaction is applied inside v1 and v2, not only in this memo.

**To:** Deal team, [REDACTED_ENTITY]  
**From:** Commercial counsel  
**Date:** 19 November 2026  
**Re:** v2 markup of the Master Services Agreement — do not sign; counter on the following terms  

### 3.1 Bottom line

v2 is not a markup. It is a purchase agreement for the Vendor’s platform, with an uncapped operational-risk transfer, a one-sided kill switch, and a California public forum. If the business wants a services relationship, we should say so and send the fallbacks below. If the business wants to sell the product, that is a different deal, at a different price, on different paper.

Three facts drive the recommendation:

1. **IP.** v2 §5.1–5.2 and the §1 definitions assign pre-existing tools, improvements “after the term,” and all off-hours work to the Customer, and they delete the grant-back and residual-knowledge clauses. That is an acquisition, not a services grant. A substantial part of the assignment is also on shaky Copyright Act ground (Edge Case 1), which means we would sign a fight, not a clean title transfer.
2. **Risk shift.** v2 §9.1 makes the Vendor the uncapped insurer of “any third-party claim” arising out of the deal, including personnel negligence and data incidents. v2 §10 then removes the cap for indemnity, IP, data, confidentiality, warranties, gross negligence, insurance-covered claims, **and “direct damages of any kind.”** The Customer’s own liability is capped. This is not a negotiated allocation.
3. **Exit and cash.** The Customer can leave on 15 days’ notice, take the incomplete work, obtain a full refund of prepaid amounts, receive 90 days of free engineering, and pay net-90 with a 20% holdback and unlimited set-off. Acceptance never occurs by default. That combination is a walk-away.

### 3.2 What we can give them

We should not open with “v1 or nothing.” Reasonable concessions that cost us little and buy credibility:

- Net-60 instead of net-30, on undisputed invoices, with deemed acceptance restored.
- A Customer audit right, twice per year, 10 days’ notice, independent accountant, cost-shift only on a material overcharge.
- Insurance: we will use commercially reasonable towers and name the Customer additional insured on CGL/cyber, primary and non-contributory, with 30 days’ cancellation notice if the carrier will give it.
- Confidentiality survival of five years, and perpetual for trade secrets.
- A data-processing addendum on a mutually acceptable form; 72-hour confirmed-breach notice; SOC 2 Type II annually if the fees support the cost.
- California **or** Delaware as a neutral; we will discuss forum. We will not accept California law **and** Santa Clara courts **and** fee-shifting as a package.
- Mutual prevailing-party fees **only** inside a confidential arbitration.

### 3.3 High-Risk items and fallback counter-clauses

Walk-away means we escalate to the business sponsor and do not keep negotiating that point downward without a documented commercial decision. Preferred language is the opening counter. Fallback is the last acceptable position.

---

#### HR-1 — IP ownership of Background IP, Vendor Tools, and “all” work product
**v2 §§1.1, 1.2, 1.4, 1.5, 5.1, 5.2, 5.3, 5.7 (pp. 2, 4–5) — High — walk-away if they insist on assignment of pre-existing tools.**

**Why it matters.** v2 converts the engagement into a transfer of the Vendor’s product, including improvements made after the term and work done off-hours. The deleted grant-back (v1 §5.3) would otherwise have let us keep using our own tools. The WMFH recital is the wrong legal box for independent-contractor software (Edge Case 1).

**Preferred counter (restore v1 architecture, with a cleaner assignment of true custom work).**

> **5.1 Ownership.** As between the Parties, Vendor owns and retains all Vendor Tools and Vendor Background IP. Customer owns and retains all Customer Background IP and Customer Data. Upon payment of the fees for the applicable Deliverable, Vendor assigns to Customer the custom Deliverables identified as such in the SOW, excluding (i) Vendor Tools, (ii) Background IP, (iii) generic methodologies, and (iv) Residual Knowledge.
>
> **5.2 Work made for hire.** The Parties acknowledge that the Deliverables are not works made for hire under 17 U.S.C. §101(2). Title passes by the assignment in Section 5.1, which is intended to satisfy 17 U.S.C. §204(a).
>
> **5.3 License to Customer.** Vendor grants Customer a perpetual, irrevocable, non-exclusive, non-transferable (except to a successor) royalty-free license to use Vendor Tools and Background IP solely as embedded in the Deliverables and solely for Customer’s internal business operations.
>
> **5.4 License to Vendor.** Customer grants Vendor a perpetual, irrevocable, non-exclusive, royalty-free license to use Customer-owned Deliverables to provide and support the Services and to improve Vendor Tools, provided Vendor does not disclose Customer Confidential Information or Customer Data.

**Fallback.** Assign custom Deliverables (not tools). Grant a **perpetual internal-use license** (not ownership) to embedded tools. Permit Vendor to reuse generic improvements to Vendor Tools that do not disclose Customer CI. No assignment of pre-existing Background IP. No attorney-in-fact. No “whether or not using Vendor resources” clause. Further-assurances within 15 Business Days, with a second notice before any attorney-in-fact mechanic.

**Walk-away.** Any present assignment of Vendor Tools or pre-existing Background IP; any assignment of improvements “after the term”; any claim on off-hours / non-Vendor-resource work of Vendor personnel.

---

#### HR-2 — Residual knowledge deleted; perpetual confidentiality; unaided-memory use as breach
**v2 §§5.4, 7.2, 7.4, 7.5 (pp. 5–7) — High.**

**Preferred counter.**

> **Residual knowledge.** Nothing in this Agreement restricts either Party from using Residual Knowledge. “Residual Knowledge” means ideas, concepts, know-how, and techniques retained in unaided memory, excluding the other Party’s Confidential Information and source code.
>
> **Confidentiality term.** Five (5) years after termination; for trade secrets, for so long as they remain trade secrets under applicable law. Information not marked and not reasonably identifiable as confidential at disclosure is not Confidential Information.

**Fallback.** Restore residual knowledge at least for Vendor (one-way is acceptable if we must). Seven-year CI term. Unmarked information is CI only if a reasonable person would understand it to be confidential.

**Walk-away.** Treating professional skill or unaided-memory know-how as a confidentiality breach.

---

#### HR-3 — Open-source ban and uncapped OSS indemnity
**v2 §5.5 (p. 5) — High.**

**Preferred counter.** Restore v1 §5.5 (OSI OSS permitted; no copyleft in a manner that would require distribution of Customer-proprietary code; OSS notice). OSS indemnity sits inside the ordinary IP indemnity and the ordinary cap.

**Fallback.** Vendor will not introduce **new** copyleft components (GPL, AGPL) into Customer-proprietary Deliverables without notice. Customer consent right limited to copyleft, not to all OSS. Indemnity for OSS **only** if the claim is that Customer’s proprietary code must be disclosed, and subject to the §10 cap.

**Walk-away.** A representation that the Deliverable contains **no** OSS, or uncapped indemnity for “any OSS claim.”

---

#### HR-4 — Uncapped, any-claim, one-sided indemnity
**v2 §§9.1–9.5 (pp. 8) — High — walk-away on uncapped “any third-party claim” and on personnel-negligence indemnity.**

**Preferred counter.** Restore v1 §9: Vendor indemnifies for third-party claims that a Deliverable **as delivered and used in accordance with this Agreement** infringes IP; standard exclusions (Customer Data, Customer specs, combinations, out-of-scope use, modifications); exclusive remedy of procure / replace / refund; **mutual** indemnities; **subject to §10**, with the IP indemnity capped at 2× the Liability Cap. Restore the procedure in v1 §9.4 (prompt notice, no forfeiture, indemnifying party controls the defense).

**Fallback.** Vendor IP + data-breach indemnity (confirmed incidents caused by Vendor’s material failure to meet the agreed security standard), capped at **2×** the Liability Cap, with v1 exclusions and exclusive remedy. Customer indemnity for Customer Data, Customer specs, and out-of-scope use, **mutual and uncapped only for those categories**. Notice is a condition to recover **damages caused by the delay**, not a forfeiture of the indemnity. Settlement consent only for non-monetary terms or admissions.

**Walk-away.** Uncapped indemnity; indemnity for “any act or omission of Vendor personnel”; 10-day forfeiture; Customer control of Vendor’s defense as a default; deletion of the exclusive IP remedy.

---

#### HR-5 — One-sided, effectively unlimited liability
**v2 §§10.1–10.2 (p. 9) — High — walk-away on uncapped “direct damages of any kind” and on the insurance-coverage carve-out.**

**Preferred counter.** Restore v1 §10 in full: mutual consequential-damages exclusion; mutual cap at 12 months’ fees paid or payable **under this Agreement** (not “the applicable SOW”); carve-outs limited to fraud, willful misconduct, IP misappropriation of the other party’s IP, and Customer’s payment obligations; IP indemnity at 2×.

**Fallback.** Mutual cap at 12 months’ Agreement fees. Vendor’s IP and confirmed-data indemnity at **2×**. Uncapped only for a Party’s fraud or willful misconduct, and for Customer’s unpaid fees. No “insurance-covered claims” carve-out. No “direct damages of any kind” clause. Mutual — not one-way — consequential exclusion.

**Walk-away.** Asymmetric caps; deletion of the consequential-damages exclusion for negligence; any formulation that makes the cap inapplicable to ordinary direct damages.

---

#### HR-6 — Acceptance, net-90, holdback, set-off, suspension
**v2 §§3, 4.1–4.5, 4.8 (pp. 3–4) — High.**

**Preferred counter.** Restore v1 §§3–4: 10-Business-Day deemed acceptance; production use = acceptance; net-30; no set-off except adjudicated amounts; no holdback; suspend on 10 days’ notice for undisputed past-due amounts.

**Fallback.** Net-60; 15-Business-Day Acceptance Period with deemed acceptance; one resubmission cycle, then executive escalation; production use = acceptance after 5 Business Days; holdback capped at **10%**, released on the earlier of final Acceptance or 90 days after delivery; set-off only for liquidated, undisputed credits; suspend on 15 days’ notice notwithstanding a “dispute” if the invoice line is not the subject of a particularized written dispute.

**Walk-away.** No deemed acceptance; net-90 combined with invoice-on-Acceptance; unlimited set-off; a holdback whose release is in Customer’s sole control.

---

#### HR-7 — 24-month “in all respects” warranty and multi-jurisdiction compliance
**v2 §§8.2, 8.4 (p. 7) — High.**

**Preferred counter.** Restore v1 §8: 90-day **material** conformity to written SOW specifications; exclusive remedy re-perform or refund the non-conforming Deliverable; malicious-code warranty; full disclaimer of implied warranties.

**Fallback.** 12-month material-conformity warranty; exclusive remedy re-perform or refund **the non-conforming Deliverable** (not the SOW). Compliance warranty limited to U.S. federal law and the laws of the jurisdiction in which the Services are performed, excluding Customer’s downstream resale markets.

**Walk-away.** “Conform in all respects”; full-SOW refund plus cover; warranty of compliance with “all applicable laws” of every jurisdiction in which Customer “operates or sells.”

---

#### HR-8 — Unilateral 15-day convenience termination, refund, no-cure cause, free transition, forced delivery
**v2 §§11.2–11.5 (pp. 10) — High — walk-away on refund of work in process and on unpaid 40-hour transition.**

**Preferred counter.** Restore v1 §11: mutual 90-day convenience; pay for work performed; prepaid non-refundable; 30-day cure; ordinary effect-of-termination; 30-day paid transition at then-current rates.

**Fallback.** Customer convenience on **60 days’** notice; pay for all work performed and non-cancellable third-party commitments; **no refund of earned or in-process fees**; optional wind-down fee of a stated percentage of remaining SOW value. Cause: 30-day cure for both; immediate for insolvency. Transition: 30 days, paid, capped hours. Delivery of accepted Deliverables and Customer Data; **no** obligation to deliver incomplete work or internal tooling. Self-help (suspension, not deletion of Customer production systems) remains available for undisputed non-payment.

**Walk-away.** Convenience termination measured in days rather than months; refund of work in process; no-cure termination for a good-faith IP/data dispute; uncompensated transition measured in hundreds of hours.

---

#### HR-9 — California law, Santa Clara courts, jury waiver, prevailing-party fees; arbitration deleted
**v2 §§14.1–14.5 (pp. 11–12) — High.**

**Preferred counter.** Restore v1 §14: Delaware law; AAA Commercial Arbitration in Wilmington; confidential; jury/class waiver; injunctive-relief carve-out. (Delaware is the Vendor’s state of incorporation and a commercially neutral corporate-law jurisdiction.)

**Fallback.** Delaware law, AAA arbitration in a mutually convenient city (Chicago or New York). Alternatively: Delaware law, exclusive courts in the District of Delaware or S.D.N.Y. We will accept a **mutual** waiver of class actions. We will not accept California law plus California courts. If they insist on California, we re-trade IP and liability — California §1668 and *Grafton Partners* make several of their other asks either void or more dangerous (Edge Case 2).

**Walk-away.** California law + Santa Clara forum + prevailing-party fees, with arbitration deleted. That package is a litigation-finance gift, not a dispute-resolution clause.

---

#### HR-10 — Assignment lock on Vendor; free assignability for Customer
**v2 §15.2 (p. 12) — High.**

**Preferred counter.** Restore v1 §15.2 (either party may assign to a successor in a sale/merger upon notice; otherwise consent not unreasonably withheld).

**Fallback.** Vendor may assign to an affiliate or to a successor in a change of control upon notice; Customer consent required only for assignment to a **competitor** of Customer, not to be unreasonably withheld.

**Walk-away.** Sole-discretion consent to a change-of-control assignment of the Vendor.

---

### 3.4 Negotiation sequence and escalation

Send a single counter-draft, not a issues list, so they have to re-mark a coherent paper.

1. **Open** with HR-1 (IP), HR-4 (indemnity), HR-5 (cap), HR-8 (termination), HR-9 (forum). These five are the deal.
2. **Trade** HR-6 (payment/acceptance) and HR-7 (warranty) against a shorter committed term or a modest fee increase. Cash mechanics are where commercial people have authority.
3. **Give** the items in §3.2 (audit, insurance certificates, notice mechanics, DPA form, SOC 2) without a corresponding concession if they are still on v2 paper — they are table stakes, not value.
4. **Escalate to the sponsor** before any movement on: assignment of Vendor Tools, uncapped indemnity, uncapped direct damages, refund of work in process, or California-law-plus-Santa-Clara.
5. **Do not** let a business-side SOW (v2 §2.2) override the MSA. If they need SOW flexibility, require the Section number.

**Status: changes required. Do not proceed to signature on v2.**

*This memo is a negotiation draft, not legal advice of record and not a risk-acceptance decision.*

### 3.5 Deal-desk playbook matrix (HR-1 through HR-10)

Use this table live on a call. Opening = first counter. Fallback = last acceptable position. Hard walk-away = escalate to the sponsor; do not keep moving. “Approved concession trade” is what we may give to buy the corresponding High-Risk point.

| Issue ID | v2 Clause | Opening Counter | Fallback Position | Hard Walk-Away Trigger | Approved Concession Trade |
|---|---|---|---|---|---|
| **HR-1** | §§1.1, 1.2, 1.4, 1.5, 5.1, 5.2, 5.3, 5.7 | Restore v1: Vendor keeps Tools/Background IP; assign **custom Deliverables upon payment**; grant-back license; further assurances (no attorney-in-fact) | Assign custom Deliverables only; perpetual **internal-use license** (not ownership) to embedded tools; Vendor may reuse generic tool improvements that do not disclose Customer CI | Any present assignment of Vendor Tools or pre-existing Background IP; assignment of improvements “after the term”; claim on off-hours / non-Vendor-resource work | Net-60 and a 10% holdback **only if** title architecture is restored. Do not trade IP for cash terms. |
| **HR-2** | §§5.4, 7.2, 7.4, 7.5 | Restore residual knowledge; 5-year CI; trade secrets for so long as they remain trade secrets; unmarked info is CI only if reasonably identifiable | One-way residual knowledge for Vendor; 7-year CI term | Treating professional skill or unaided-memory know-how as a confidentiality breach | Marking protocol (Customer may mark; Vendor treats marked + obviously confidential information as CI). |
| **HR-3** | §5.5 | Restore v1 OSS clause (OSI OK; no copyleft contamination; OSS notice); OSS indemnity inside ordinary IP indemnity and cap | No **new** copyleft (GPL/AGPL) in Customer-proprietary Deliverables without notice; consent limited to copyleft | Representation that the Deliverable contains **no** OSS; uncapped indemnity for “any OSS claim” | Annual OSS notice/scan if they fund it. Do not give a “no OSS” warranty. |
| **HR-4** | §§9.1–9.5 | Restore v1 §9: IP infringement of Deliverable as delivered/used in accordance; exclusions; exclusive remedy; mutual; 2× cap; indemnifying party controls defense | Vendor IP + confirmed-data indemnity at **2×**; Customer indemnity for Data/specs/out-of-scope, mutual; notice delay cuts damages, does not forfeit | Uncapped indemnity; “any act or omission of personnel”; 10-day forfeiture; Customer default control of Vendor’s defense | Broader data-breach indemnity if they accept a **mutual** cap and exclusive IP remedy. |
| **HR-5** | §§10.1–10.2 | Restore v1 §10 in full: mutual consequential exclusion; mutual 12-month **Agreement** cap; carve-outs = fraud, willful misconduct, other party’s IP, Customer’s payment; IP indemnity at 2× | Mutual 12-month Agreement cap; Vendor IP/data indemnity at 2×; uncapped only for fraud/willful misconduct and unpaid fees; **no** insurance carve-out; **no** “direct damages of any kind” | Asymmetric caps; deletion of consequential exclusion for negligence; cap inapplicable to ordinary direct damages | 2× super-cap on IP/data indemnity as the price of keeping the base cap mutual. |
| **HR-6** | §§3, 4.1–4.5, 4.8 | Restore v1: 10-BD deemed acceptance; production use = acceptance; net-30; no set-off except adjudicated amounts; no holdback; suspend on 10 days | Net-60; 15-BD deemed acceptance; one resubmission then executive escalation; 10% holdback released on earlier of final Acceptance or 90 days after delivery; set-off only for liquidated undisputed credits | No deemed acceptance; net-90 **plus** invoice-on-Acceptance; unlimited set-off; holdback release in Customer’s sole control | Net-60 is the cash concession. Do not give both net-90 and holdback. |
| **HR-7** | §§8.2, 8.4 | Restore v1: 90-day **material** conformity; exclusive remedy re-perform or refund **the Deliverable**; malicious-code warranty; full disclaimer | 12-month material conformity; refund the non-conforming Deliverable (not the SOW); compliance warranty = U.S. federal law + law of the jurisdiction where Services are performed | “Conform in all respects”; full-SOW refund plus cover; “all applicable laws” of every jurisdiction Customer “operates or sells” | SOC 2 Type II annually if fees support the cost — not a 24-month “in all respects” warranty. |
| **HR-8** | §§11.2–11.5 | Restore v1: mutual 90-day convenience; pay work performed; prepaid non-refundable; 30-day cure; 30-day **paid** transition | Customer convenience on **60 days**; pay work performed + non-cancellable third-party spend; no refund of earned/in-process fees; 30-day paid transition, capped hours; no delivery of incomplete work | Convenience measured in days; refund of work in process; no-cure kill for a good-faith IP/data dispute; uncompensated transition in the hundreds of hours | Wind-down fee of a stated % of remaining SOW value, in exchange for a 60-day (not 90-day) convenience notice. |
| **HR-9** | §§14.1–14.5 | Restore v1: Delaware law; AAA Wilmington; confidential; jury/class waiver; injunctive carve-out | Delaware law; AAA in Chicago or New York; **or** Delaware law + D. Del. / S.D.N.Y. courts; mutual class waiver | California law + Santa Clara forum + prevailing-party fees, with arbitration deleted | Confidential arbitration in a mutually convenient city. Do not accept CA law + CA courts as a “compromise.” |
| **HR-10** | §15.2 | Restore v1: either party may assign to a successor in a sale/merger upon notice; otherwise consent not unreasonably withheld | Vendor may assign to affiliate or change-of-control successor upon notice; Customer consent only for assignment to a **competitor**, not unreasonably withheld | Sole-discretion consent to a change-of-control assignment of the Vendor | Notice-plus-competitor-consent is the give. Do not give sole-discretion consent. |

---

## 4. Source & Verification Log

### 4.1 Contract locators

Every finding above is located to the section and the page marker in the workspace copies. Page markers are explicit (`[Page N]`) so they survive reflow.

| Finding theme | v1 locator | v2 locator |
|---|---|---|
| Parties, addresses, notice emails | v1 p. 1, preamble | v2 p. 1, preamble |
| Background IP / Deliverables / Tools definitions | v1 §1.1–1.5, p. 2 | v2 §1.1–1.5, p. 2 |
| Order of precedence | v1 §2.2, p. 2 | v2 §2.2, p. 2 |
| Acceptance mechanics | v1 §3.1–3.4, p. 3 | v2 §3.1–3.4, p. 3 |
| Fees, net terms, set-off, suspension | v1 §4.1–4.5, pp. 3–4 | v2 §4.1–4.5, pp. 3–4 |
| Audit; holdback | *(none)* | v2 §4.7–4.8, p. 4 |
| Background IP retention | v1 §5.1, p. 4 | v2 §5.1, p. 4 (assignment) |
| Work product / WMFH | v1 §5.2, p. 4 | v2 §5.2, p. 5 |
| Grant-back license | v1 §5.3, p. 5 | v2 §5.3, p. 5 (deleted) |
| Residual knowledge | v1 §5.4, p. 5 | v2 §5.4, p. 5 (deleted) |
| Open source | v1 §5.5, p. 5 | v2 §5.5, p. 5 |
| Customer Data / security / breach notice | v1 §6.1–6.4, p. 6 | v2 §6.1–6.5, p. 6 |
| Confidentiality term and residual-knowledge-as-breach | v1 §7.1–7.4, p. 6 | v2 §7.1–7.5, pp. 6–7 |
| Warranties | v1 §8.1–8.4, p. 7 | v2 §8.1–8.5, p. 7 |
| Vendor indemnity / exclusions / Customer indemnity / procedure / exclusive IP remedy | v1 §9.1–9.5, pp. 7–8 | v2 §9.1–9.4, p. 8 (§9.5 deleted) |
| Consequential damages; cap; carve-outs | v1 §10.1–10.3, pp. 8–9 | v2 §10.1–10.2, p. 9 |
| Term; convenience; cause; effect; transition | v1 §11.1–11.5, pp. 9–10 | v2 §11.1–11.5, pp. 9–10 |
| Insurance | v1 §12.1–12.2, p. 10 | v2 §12.1–12.2, p. 11 |
| Governing law; arbitration / courts | v1 §14.1–14.5, p. 11 | v2 §14.1–14.5, pp. 11–12 |
| Assignment | v1 §15.2, p. 12 | v2 §15.2, p. 12 |
| Force majeure | v1 §15.6, p. 12 | v2 §15.6, p. 13 |
| SOW-001 fee / holdback / dates | v1 p. 13, Exhibit A | v2 p. 14, Exhibit A |

### 4.2 External authorities consulted (19 November 2026)

**Verified this session** (statutory text or judicial holding retrieved from a primary or well-known legal archive). Quoted statutory text is verbatim. Case holdings are paraphrases of the official headnote/opinion, not inventions.

| Authority | Status | Verified text / holding | Used for | Locator |
|---|---|---|---|---|
| 17 U.S.C. §101 (Definitions), U.S. House Office of the Law Revision Counsel, preliminary edition | **Verified** | “Work made for hire” ¶(2) applies only to a work specially ordered or commissioned for use as a contribution to a **collective work, motion picture or other audiovisual work, translation, supplementary work, compilation, instructional text, test, answer material for a test, or atlas**, and only if the parties expressly agree in a **written instrument signed by them**. A “transfer of copyright ownership” is an assignment or exclusive license, not a nonexclusive license. | Edge Case 1; HR-1 | [§101](https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title17-section101&num=0&edition=prelim) |
| 17 U.S.C. §204(a) (Execution of transfers), same source | **Verified** | A transfer of copyright ownership, other than by operation of law, “is not valid unless an instrument of conveyance, or a note or memorandum of the transfer, is in writing and signed by the owner of the rights conveyed or such owner’s duly authorized agent.” | Edge Case 1; HR-1 | [§204](https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title17-section204&num=0&edition=prelim) |
| *Community for Creative Non-Violence v. Reid*, 490 U.S. 730 (1989) (Marshall, J., unanimous) | **Verified** | To decide whether a work is WMFH, a court first applies **general common law of agency** (not a single state’s law) to determine employee vs. independent contractor, then applies §101(1) or §101(2). On the facts, the sculptor was an independent contractor (skilled occupation; own tools; worked off-site without daily supervision; short engagement; controlled his own hours; hired his own assistants; no payroll taxes, benefits, or right to assign more projects). The work was therefore not WMFH under §101(1); it also failed §101(2) (sculpture is not one of the nine categories; no signed writing). Joint-authorship remanded. | Edge Case 1; HR-1 | [Justia, 490 U.S. 730](https://supreme.justia.com/cases/federal/us/490/730/) |
| Cal. Civ. Code § 1668 (current through FindLaw snapshot as of 1 January 2023) | **Verified** | “All contracts which have for their object, directly or indirectly, to exempt anyone from responsibility for his own fraud, or willful injury to the person or property of another, or violation of law, whether willful or negligent, are against the policy of the law.” | Edge Case 2; HR-5; §10 | [FindLaw CIV § 1668](https://codes.findlaw.com/ca/civil-code/civ-sect-1668.html) |
| Cal. Lab. Code § 2870 (FindLaw snapshot as of 1 January 2019) | **Verified** | (a) An employment-agreement assignment of inventions “shall not apply to an invention that the employee developed entirely on his or her own time without using the employer’s equipment, supplies, facilities, or trade secret information” except inventions that (1) relate to the employer’s business or actual or demonstrably anticipated R&D, or (2) result from work performed for the employer. (b) A provision that requires assignment of an otherwise excluded invention “is against the public policy of this state and is unenforceable.” | Edge Case 1; HR-1; v2 §1.4 | [FindLaw LAB § 2870](https://codes.findlaw.com/ca/labor-code/lab-sect-2870.html) |
| Cal. Lab. Code § 2871 (same snapshot) | **Verified** | “No employer shall require a provision made void and unenforceable by Section 2870 as a condition of employment or continued employment.” Disclosure-and-review mechanics are permitted if received in confidence. | Edge Case 1; HR-1 | [FindLaw LAB § 2871](https://codes.findlaw.com/ca/labor-code/lab-sect-2871.html) |
| Cal. Lab. Code § 2872 (same snapshot) | **Verified** | If a post-1 January 1980 employment agreement requires assignment of inventions, the employer **must at the time the agreement is made give written notice** that the agreement does not apply to a § 2870 invention. In any suit, the **burden of proof is on the employee** claiming § 2870. | Edge Case 1; HR-1 | [FindLaw LAB § 2872](https://codes.findlaw.com/ca/labor-code/lab-sect-2872.html) |
| *Grafton Partners L.P. v. Superior Court* (Cal. 2005) 36 Cal. 4th 944, 116 P.3d 479, docket S123344, filed 4 August 2005; CourtListener index | **Verified (holding context)** | California Supreme Court, published; cited by 100+ opinions; concurrence references Cal. Const. art. I, §16. Holding context confirmed: **pre-dispute jury waivers are unenforceable in California** unless a statute expressly authorizes the waiver. Full opinion body was not pulled into the workspace; the holding is used as confirmed by *In re County of Orange* (next row), which quotes and applies it. | Edge Case 2; HR-9 | [CourtListener search](https://www.courtlistener.com/?q=Grafton+Partners+jury+waiver&type=o) |
| *In re County of Orange* (County of Orange v. United States District Court), 784 F.3d 520 (9th Cir. 2015), No. 14-72343, filed 16 April 2015 | **Verified** | Ninth Circuit, published, cited by 89 opinions. **Holding:** Under *Erie*, a federal court sitting in diversity must import state law governing pre-dispute jury-trial waivers when state law is **more protective** of the jury right than federal law. Applying California law, the contractual jury waiver was **unenforceable** under *Grafton*. Mandamus granted. The underlying contract was a professional-services agreement with a California choice-of-law clause and a jury waiver — structurally the same package as v2 §14. | Edge Case 2; HR-9; v2 §14.3 | [Justia, 14-72343](https://law.justia.com/cases/federal/appellate-courts/ca9/14-72343/14-72343-2015-04-16.html) |

**Still requiring human verification (not applied as settled law).** These are fact or technical items, not missing statutes.

| Item | Why it stays human | Owner |
|---|---|---|
| OSS license scan of Vendor Tools and Deliverable repos | Technical workstream; cannot be answered from statutes. Determines whether an “all IP assigned” clause delivers copyleft-contaminated code. | Engineering + open-source counsel |
| W-2 vs. 1099 classification of Vendor authors, and whether any author is a California employee | *Reid* is a multi-factor agency test on facts. Lab. Code §§ 2870–2872 apply only if an employment agreement exists. | HR / employment counsel |
| Separate patent assignment for Vendor Tools | 17 U.S.C. §204(a) is a copyright formality; patent title does not move by a copyright recital. | Patent counsel |
| Current AAA Commercial Rules; EAR/OFAC texts | Not retrieved this session; not needed to reject v2, needed only if a compliance warranty is re-traded. | Trade counsel if HR-7 fallback is used |

### 4.3 Three edge cases requiring manual human counsel verification

These are the points on which this review should **not** be the last word. Verified law is stated as verified. Unverified facts are named as such.

**Edge Case 1 — Does v2’s “work made for hire” recital actually vest title to the software in the Customer, and does the in-contract assignment of pre-existing Vendor Tools satisfy 17 U.S.C. §204(a)?**

**Verified law.** 17 U.S.C. §101(2) confines commissioned WMFH to nine enumerated categories plus a signed writing. Independently contracted software implementation is not on that list. *Reid*, 490 U.S. 730, holds that “employee” in §101(1) means common-law agency employee, applied on a multi-factor test (skill, tools, location, duration, control over hours, right to assign more work, benefits, payroll taxes). A services vendor whose engineers supply their own tools, work from their own offices, and are paid as contractors is on the *Reid* independent-contractor side of the line. 17 U.S.C. §204(a) still requires a signed writing for any copyright assignment, including of pre-existing tools. Patent title does not move by a copyright recital.

**Human verification remaining.** Pull the actual employment/contractor agreements. If any author is a California **employee**, Cal. Lab. Code § 2870(a) voids v2 §1.4’s off-hours assignment as to inventions developed entirely on the employee’s own time without employer resources, except the two statutory carve-outs; § 2870(b) makes a contrary covenant unenforceable as against public policy; § 2871 forbids requiring such a provision as a condition of employment; § 2872 requires contemporaneous written notice of the § 2870 carve-out and puts the burden of proof on the employee. Whether those statutes apply is a workforce-classification question (*Reid* facts; W-2 vs. 1099), not a drafting question. If tools really will be transferred, prepare a short-form IP assignment and a separate patent assignment.

**Human counsel should:** classify the workforce; decide WMFH vs. assignment; paper any true transfer with a bill of sale plus patent assignment; and add a Lab. Code § 2870 notice if California employees are in the authorship chain.

**Edge Case 2 — If California law and Santa Clara courts apply (v2 §14), is the jury waiver void, and do Cal. Civ. Code §1668 / unconscionability doctrines limit the one-sided cap and indemnity?**

**Verified law.** *Grafton Partners L.P. v. Superior Court*, 36 Cal. 4th 944 (2005), holds that a **pre-dispute** contractual jury waiver is unenforceable in California unless a statute expressly authorizes it (Cal. Const. art. I, §16). *In re County of Orange*, 784 F.3d 520 (9th Cir. 2015), holds that a federal court sitting in diversity must apply that California rule when it is more protective of the jury right than federal law, and that a professional-services jury waiver governed by California law is therefore **unenforceable in federal court**. v2 §14.3’s waiver is void in both the Santa Clara Superior Court and the federal court in the same county. Cal. Civ. Code § 1668 (text quoted in §4.2) voids contracts that exempt a party from responsibility for its own **fraud**, **willful injury**, or **violation of law**, whether willful or negligent. v2 §10.2’s remaining cap (fraud only, for Customer) does not create a § 1668 problem by itself; v2’s attempt to keep Vendor exposed to “direct damages of any kind” is commercially extreme but is not a § 1668 violation — § 1668 is a shield-killer, not a sword-grant. What § 1668 **does** do is prevent Vendor from ever relying on a cap or consequential-damages waiver to escape fraud, willful injury, or statutory violation. That is already consistent with v1’s fraud/willful-misconduct carve-out.

**Human verification remaining.** Whether a negotiated B2B MSA between sophisticated entities can (a) cap ordinary negligence and (b) exempt Vendor from force majeure on data/confidentiality duties, under current California unconscionability doctrine, is a case-law question. Retrieve the current leading California case on one-sided technology-services caps if California remains the choice of law.

**Human counsel should:** delete the jury waiver (it is void and misleading); if California stays, rewrite §10 carve-outs to match § 1668 (fraud / willful injury / violation of law) rather than “direct damages of any kind”; and do not rely on the waiver to keep a case out of a California jury — *In re County of Orange* closes that door in federal court too.

**Edge Case 3 — What happens if Vendor Tools that are assigned under v2 §5.1 contain copyleft OSS, and how far does the “all applicable laws of each jurisdiction in which Customer operates or sells” warranty reach?**

**Verified law.** None of the OSS-license or export-control texts were retrieved this session. This edge case remains a **human** workstream.

**Why it matters.** v2 §5.5 warrants that no Deliverable is subject to any copyleft license and shifts “any OSS claim” into the uncapped indemnity. If Vendor Tools already contain GPL/AGPL components, assigning those tools to Customer may deliver code that **must** be distributed under the copyleft terms — i.e., Customer may not receive the proprietary title v2 promises. A clean-room / OSS-scan of the actual repos is a technical workstream, not a drafting workstream. Separately, v2 §8.4 warrants compliance with **all** laws of **every** jurisdiction in which Customer operates **or sells**. That is an export-control (EAR/OFAC), privacy, and consumer-protection exposure that a services vendor cannot honestly give without a scope cut.

**Human counsel should:** commission an OSS scan of Vendor Tools before any assignment discussion; have export/sanctions counsel define a lawful compliance warranty (typically: Vendor will not cause Customer to violate U.S. export controls by the Deliverable as delivered); and delete “or sells” from the compliance warranty.

---

### 4.4 Research gaps and assumptions

- **Assumption — review side.** No side was stated in the objective. This review is from the Vendor’s side (drafter of v1). A Customer-side review would still reject several v2 asks as overreach, but the walk-away set would differ.
- **Assumption — simulated papers.** The two MSA files were created in this session at the user’s direction because no attachments arrived. They are realistic commercial papers, not a live counterparty draft.
- **Verified this session.** 17 U.S.C. §§ 101, 204(a); *Reid*; Cal. Civ. Code § 1668; Cal. Lab. Code §§ 2870–2872; *Grafton* (holding context); *In re County of Orange*. FindLaw California-code snapshots are dated 1 January 2023 (Civ.) and 1 January 2019 (Lab.). Human counsel should confirm those sections have not been amended since those snapshots before relying on them in a filing.
- **Still not retrieved.** Current AAA Commercial Rules; EAR/OFAC texts; current California unconscionability case law on one-sided B2B caps. None of these is applied as settled law.
- **Not reviewed.** No playbook, approval matrix, or insurance policy was supplied. Fallbacks above are market, not client-mandated. The “Approved Concession Trade” column in §3.5 is counsel’s recommendation, not a board-approved authority matrix.
- **Open facts.** Whether Vendor personnel who will author Deliverables are California employees (Edge Case 1); whether Vendor Tools already contain copyleft OSS (Edge Case 3); whether any SOW will be a 180-day multi-milestone engagement (cash tail in §1.3).

---

*End of review. Simulated, redacted v1/v2 papers: [MSA_v1_Original.md](contracts/MSA_v1_Original.md) · [MSA_v2_Counterparty_Markup.md](contracts/MSA_v2_Counterparty_Markup.md).*
