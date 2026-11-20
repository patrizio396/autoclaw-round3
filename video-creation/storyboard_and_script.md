# [REDACTED_ENTITY] — Multi-Agent Data Ingestion Pipeline
## 45.000 s · 1080p60 · 3D Technical Explainer — Master Storyboard & Voiceover Script

> **Redaction notice.** Every organization name, pipeline identifier, endpoint, personnel
> reference and financial metric in this production is redacted as `[REDACTED_ENTITY]` or
> `[REDACTED_AMOUNT]` across the storyboard, voiceover script, on-screen HUD overlays,
> subtitles and documentation. Compliance is machine-checked by `CHK-10`.

---

## 1. Master format contract

| Parameter | Value |
|---|---|
| Resolution | 1920 x 1080 internal canvas buffer (responsive CSS scale in viewport) |
| Frame rate | 60 fps — fully deterministic, frame-index driven |
| Total frames | 2700 (frame indices 0–2699) |
| Duration | 45.000 s exactly |
| Look | Dark-mode broadcast palette, emissive wireframe 3D, sRGB |
| Captions | Burned-in HUD captions (renderer) + `pipeline/subtitles.srt` (identical text) |
| Audio | `pipeline/ambient_cues.wav` — 44.1 kHz · 16-bit PCM · stereo · 1,984,500 frames · 45.000 s |
| Renderer | `renderer/index.html` — 100% self-contained, zero external dependencies, offline-capable |
| Determinism | Seeded PRNG only; `window.renderAtFrame(frameIndex)` reproduces any frame bit-identically |

## 2. Deterministic scene map

| Scene | Start TC | End TC | Frames | Duration |
|---|---|---|---|---|
| Scene 1 | 00:00:00.000 | 00:00:10.000 | 0-600 | 10.000 s |
| Scene 2 | 00:00:10.000 | 00:00:24.000 | 600-1440 | 14.000 s |
| Scene 3 | 00:00:24.000 | 00:00:36.000 | 1440-2160 | 12.000 s |
| Scene 4 | 00:00:36.000 | 00:00:45.000 | 2160-2700 | 9.000 s |

**Audio chime markers** (`ambient_cues.wav`): 0.000 s (frame 0), 10.000 s (frame 600),
24.000 s (frame 1440), 36.000 s (frame 2160), 44.500 s (frame 2670, closing marker).
Scene cuts land exactly on chime frames; camera trajectories are continuous across cuts
(a 4-frame screen flash accents each cut).

---

## 3. Scene 1 — Unstructured Data Chaos (00:00:00.000 – 00:00:10.000 · frames 0-600)

### Beat sheet
| Frames | Beat |
|---|---|
| 0-90 | Void fades up; starfield of document cards (PDF / CSV / API payloads) materializes on tilted elliptical orbits. |
| 90-240 | Cards orbit a central congestion knot; first deterministic collision sparks between seeded card pairs. |
| 240-420 | Error storm: red flashes ripple through the cloud; latency and error-rate HUD metrics spike. |
| 420-560 | Ingestion bottleneck: cards pile toward the knot; backlog counter climbs; rings pulse from the core. |
| 560-600 | Camera settles toward the knot; hard cut locked at frame 600 on the 10.000 s chime. |

### Camera (cubic-bezier eased keyframes; yaw/pitch in degrees)
| Frame | Yaw | Pitch | Dist | Target | FOV |
|---|---|---|---|---|---|
| 0 | -31.5 | 24.0 | 980 | (0, 0, 0) | 55 |
| 300 | -8.6 | 19.4 | 880 | (20, 0, 0) | 55 |
| 600 | 5.7 | 14.3 | 840 | (40, 0, 20) | 55 |

### Lighting & palette
Void navy base gradient (#0a0e1a to #131a2e); document cards in desaturated slate (#cfd8ea),
CSV amber (#ffb020), API cyan (#35d0ff); error red (#ff4757) hazard flashes with soft bloom;
cool rim tone, no hard shadows — pure emissive wireframe look. Perspective grid floor at 10% alpha.

### HUD callouts (sanitized)
- `RAW INTAKE STREAM · [REDACTED_ENTITY] FEED`
- `BACKLOG: 41,000–53,000 DOCS` (sine + deterministic per-frame jitter)
- `PARSE ERROR RATE: 18–30 %` (storm spike frames 240–420)
- `AVG LATENCY: 6,200–9,400 MS`
- Persistent: SMPTE `00:00:SS:FF`, `FRAME NNNN / 2700`, `1080P60 · DETERMINISTIC`

### Voiceover — cues 1–3 (verbatim match with `pipeline/subtitles.srt`)

---

## 4. Scene 2 — Map-Reduce Multi-Agent Routing (00:00:10.000 – 00:00:24.000 · frames 600-1440)

### Beat sheet
| Frames | Beat |
|---|---|
| 600-700 | Chaos cloud compresses into an intake mouth stage-left; orchestrator core ignites. |
| 700-840 | Orchestrator octahedron spins up; partition map draws three parallel worker lanes. |
| 840-1200 | Packets stream along the three rails; agent nodes pulse on arrival; throughput telemetry climbs. |
| 1200-1440 | Sustained parallel flow; all lanes saturated; cut locked at frame 1440 on the 24.000 s chime. |

### Camera
| Frame | Yaw | Pitch | Dist | Target | FOV |
|---|---|---|---|---|---|
| 600 | 5.7 | 14.3 | 840 | (40, 0, 20) | 55 |
| 900 | 1.1 | 10.3 | 860 | (120, -10, 0) | 55 |
| 1200 | -3.4 | 8.0 | 800 | (160, 0, 40) | 55 |
| 1440 | -6.9 | 5.7 | 760 | (180, 0, 60) | 52 |

### Lighting & palette
Deep petrol gradient (#040910 to #081426); orchestrator core cyan (#35d0ff); lane identity colors —
Parser Agent blue (#4fc3f7), Schema Normalizer purple (#b388ff), Policy Auditor orange (#ffb74d);
packets white-cyan with motion trails; grid dimmed to 8% alpha.

### HUD callouts
- `ORCHESTRATOR: ACTIVE · MAP-REDUCE PARTITION x3`
- `LANES: PARSER AGENT / SCHEMA NORMALIZER / POLICY AUDITOR`
- `THROUGHPUT: 1,100–1,400 PKT/S` (animated, deterministic)
- `SYNC: LOCKED · REAL-TIME TELEMETRY`

### Voiceover — cues 4–8

---

## 5. Scene 3 — Deterministic Verification Gate (00:00:24.000 – 00:00:36.000 · frames 1440-2160)

### Beat sheet
| Frames | Beat |
|---|---|
| 1440-1520 | Crystalline hex verification wall crystallizes; rule assertions CHK-01..CHK-10 arm in sequence. |
| 1520-1900 | Packets traverse converging rails; the gate renders verdicts: verified packets flash green and lock into the right-hand slot wall; malformed packets deflect into the amber/red quarantine bin. |
| 1900-2100 | Quarantine population visible; rule tick panel fills green; assert counters settle (~72% deterministic pass rate). |
| 2100-2160 | Gate saturated; verified wall near complete; cut locked at frame 2160 on the 36.000 s chime. |

### Camera
| Frame | Yaw | Pitch | Dist | Target | FOV |
|---|---|---|---|---|---|
| 1440 | -6.9 | 5.7 | 760 | (180, 0, 60) | 52 |
| 1700 | 2.9 | 3.4 | 700 | (200, -10, 60) | 52 |
| 2000 | -2.3 | 5.7 | 730 | (190, 0, 60) | 52 |
| 2160 | 10.3 | 9.2 | 900 | (120, 20, 40) | 55 |

### Lighting & palette
Crystalline ice-cyan lattice (#7fe9ff) with per-hex shimmer; verified packets/blocks green (#2ee66b);
quarantine amber (#ff9f1a) decaying to red (#ff4757); white verdict flash at the gate plane;
bin outlined in red with amber label.

### HUD callouts
- `GATE: CHK-01..CHK-10 ARMED`
- `ASSERTIONS PASSED: N/10` (rule tick panel, per-rule status)
- `QUARANTINED: M PKT` · `VERIFIED LOCKS: G PKT`
- `MALFORMED / HALLUCINATED -> QUARANTINE (AMBER-RED)`

### Voiceover — cues 9–13

---

## 6. Scene 4 — Structured Output & Audit Ledger (00:00:36.000 – 00:00:45.000 · frames 2160-2700)

### Beat sheet
| Frames | Beat |
|---|---|
| 2160-2260 | Release: verified blocks leave the slot wall and fly along bezier arcs toward the ledger matrix. |
| 2260-2470 | 4x3x2 immutable cube-matrix assembles with staggered lock pops; ledger slab glows. |
| 2470-2560 | JSON ledger lines print row by row; executive scorecard counts up to 99.98% schema accuracy. |
| 2560-2700 | `[REDACTED_AMOUNT]` savings banner locks; audit coverage 100%; camera pulls back to hero framing; closing chime at frame 2670 (44.500 s); fade-out. |

### Camera
| Frame | Yaw | Pitch | Dist | Target | FOV |
|---|---|---|---|---|---|
| 2160 | 10.3 | 9.2 | 900 | (120, 20, 40) | 55 |
| 2450 | 19.5 | 11.5 | 1020 | (100, 30, 20) | 55 |
| 2700 | 24.1 | 13.7 | 1100 | (100, 30, 10) | 55 |

### Lighting & palette
Deep void gradient (#030509 to #0b1120); ledger green (#2ee66b) block matrix; gold accent (#ffd166)
for the savings banner; panel cyan for the scorecard; end vignette strengthens from frame 2620.

### HUD callouts
- `LEDGER: IMMUTABLE JSON/SQL`
- `SCHEMA ACCURACY: 99.98 %`
- `OPERATIONAL SAVINGS UNLOCKED: [REDACTED_AMOUNT]`
- `AUDIT COVERAGE: 100 %`
- `EXECUTIVE SCORECARD · [REDACTED_ENTITY] · VERIFIED OUTPUT`

### Voiceover — cues 14–16

---

## 7. Voiceover master script (107 words · cues 1–16 · matches `pipeline/subtitles.srt` verbatim)

| Cue | Timecode | Line |
|---|---|---|
| 1 | 00:00:00.500 – 00:00:03.400 | Every single day, enterprise data<br>arrives chaotic: |
| 2 | 00:00:03.500 – 00:00:07.500 | Unstructured PDFs, messy CSVs,<br>and raw API payloads collide in transit. |
| 3 | 00:00:07.600 – 00:00:09.900 | Unverified, untrusted,<br>and costly to ingest. |
| 4 | 00:00:10.500 – 00:00:14.700 | A central orchestrator partitions every<br>payload across parallel worker lanes: |
| 5 | 00:00:14.800 – 00:00:17.100 | A Parser Agent extracts clean structure, |
| 6 | 00:00:17.200 – 00:00:19.800 | a Schema Normalizer aligns each<br>and every field, |
| 7 | 00:00:19.900 – 00:00:22.200 | and a Policy Auditor screens for risk, |
| 8 | 00:00:22.300 – 00:00:23.900 | all synchronized in real time. |
| 9 | 00:00:24.500 – 00:00:27.900 | At the deterministic verification gate,<br>ten rule assertions |
| 10 | 00:00:28.000 – 00:00:29.500 | examine every single packet. |
| 11 | 00:00:29.600 – 00:00:31.700 | Malformed and hallucinated records |
| 12 | 00:00:31.800 – 00:00:33.500 | are deflected into quarantine. |
| 13 | 00:00:33.600 – 00:00:35.900 | while verified packets lock<br>into green blocks. |
| 14 | 00:00:36.600 – 00:00:39.600 | Verified blocks assemble into<br>an immutable audit ledger, |
| 15 | 00:00:39.700 – 00:00:42.300 | unlocking [REDACTED_AMOUNT]<br>in annual savings, |
| 16 | 00:00:42.400 – 00:00:44.800 | at 99.98% schema accuracy,<br>and fully auditable. |

Pacing: 107 words / 45.000 s = 2.38 words/s — inside the 105–135 word broadcast window
(checked by CHK-08). Peak subtitle reading speed 19.6 chars/s, under the 20 chars/s cap (CHK-03).

## 8. Redaction & compliance policy

1. Only the canonical tokens `[REDACTED_ENTITY]` and `[REDACTED_AMOUNT]` may appear.
2. No emails, no unredacted organization names, no currency figures anywhere under `video-creation/`
   (machine-enforced by CHK-10 across every text deliverable).
3. Percentages and abstract counters (99.98%, packet counts, latency ms) are sanctioned metrics.

## 9. Production determinism notes

- All stochastic parameters derive from a seeded PRNG (mulberry32) initialized once at load;
  no `Math.random()`, no wall-clock state in the render path.
- `window.renderAtFrame(frameIndex)` renders any frame 0–2699 identically on every machine —
  the contract used by headless capture and the in-browser 1-click `.webm` recorder.
- Scene cuts, chime markers, caption cues, camera keyframes and HUD counter formulas all
  reconcile to the frame indices published in Section 2.

## 10. Deliverable map

```
video-creation/
  storyboard_and_script.md      <- this document
  renderer/index.html           <- self-contained 3D engine + HUD + recorder
  pipeline/subtitles.srt        <- 16 cues, 00:00:00,000 - 00:00:45,000
  pipeline/build_and_verify.py  <- WAV synth + ffmpeg command + CHK-01..CHK-10
  pipeline/ambient_cues.wav     <- 45.000 s stereo master bed (generated)
  pipeline/ffmpeg_command.txt   <- exact mux command (generated)
  verification/run_log.txt      <- 10/10 PASS verification log (generated)
  verification/report.json      <- machine-readable check report (generated)
  README.md                     <- operations manual
```
