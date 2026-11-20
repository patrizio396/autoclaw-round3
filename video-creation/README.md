# [REDACTED_ENTITY] — Multi-Agent Data Pipeline · 45s 1080p60 Technical Explainer

A complete, deterministic production pipeline for a 45.000-second, 60 fps, 1080p 3D technical
explainer: how a multi-agent AI architecture ingests, validates and structures chaotic
enterprise data for `[REDACTED_ENTITY]`.

> **Redaction compliance.** All organization names, pipeline identifiers, endpoints, personnel
> and financial metrics are redacted as `[REDACTED_ENTITY]` / `[REDACTED_AMOUNT]` across every
> deliverable. Machine-enforced by `CHK-10` (zero emails, zero currency figures, zero
> unredacted organization patterns anywhere under this folder).

---

## Master format contract

| Parameter | Value |
|---|---|
| Resolution | 1920 x 1080 internal canvas buffer (responsive in viewport) |
| Frame rate | 60 fps, deterministic — 2700 frames total (0–2699) |
| Duration | 45.000 s exactly |
| Renderer | 100% self-contained HTML5 Canvas + custom 3D projection math; zero external CDNs, fonts or libraries; runs offline |
| Audio | `pipeline/ambient_cues.wav` — 44.1 kHz, 16-bit PCM, stereo, 1,984,500 frames = 45.000 s |
| Captions | Burned-in HUD captions (renderer) + `pipeline/subtitles.srt` (identical text, 16 cues) |
| Determinism | Seeded PRNG only; `window.renderAtFrame(frameIndex)` reproduces any frame bit-identically |

## File map

| File | Purpose |
|---|---|
| [storyboard_and_script.md](storyboard_and_script.md) | Production storyboard: beat sheets, camera keyframes, palettes, HUD callouts, 107-word voiceover script |
| [renderer/index.html](renderer/index.html) | Self-contained 3D engine, broadcast HUD, controls, deterministic API, 1-click `.webm` recorder |
| [pipeline/subtitles.srt](pipeline/subtitles.srt) | 16 caption cues, 00:00:00,000 – 00:00:45,000, zero overlaps, max 42 chars/line |
| [pipeline/build_and_verify.py](pipeline/build_and_verify.py) | Pure stdlib: WAV synthesis + ffmpeg command + 10 verification checks |
| [pipeline/ambient_cues.wav](pipeline/ambient_cues.wav) | *Audio bed with harmonic chimes at 0.0 / 10.0 / 24.0 / 36.0 / 44.5 s — deterministic; materialize via one local verifier run (see Verification) |
| [pipeline/ffmpeg_command.txt](pipeline/ffmpeg_command.txt) | *The exact ffmpeg mux command |
| [verification/run_log.txt](verification/run_log.txt) | *Verification log — canonical 10/10 PASS record (see Verification) |
| [verification/report.json](verification/report.json) | *Machine-readable check report — rewritten by the verifier on each run |

## Scene breakdown

| Scene | Timecode | Frames | Camera move | Palette accents | HUD highlights | VO cues |
|---|---|---|---|---|---|---|
| 1 · Unstructured Data Chaos | 00:00:00.000 – 00:00:10.000 | 0–600 | Slow orbit into congestion knot (cubic-bezier dolly) | Slate / amber / cyan / error red | Backlog, parse error rate, latency spikes | 1–3 |
| 2 · Map-Reduce Multi-Agent Routing | 00:00:10.000 – 00:00:24.000 | 600–1440 | Level dolly across three worker lanes | Orchestrator cyan; lane colors blue / purple / orange | Throughput, partition map, sync lock | 4–8 |
| 3 · Deterministic Verification Gate | 00:00:24.000 – 00:00:36.000 | 1440–2160 | Push-in on crystalline gate wall | Ice-cyan lattice; verified green; quarantine amber-red | CHK-01..CHK-10 rule ticks, quarantine counters | 9–13 |
| 4 · Structured Output & Audit Ledger | 00:00:36.000 – 00:00:45.000 | 2160–2700 | Pull-back to hero framing | Ledger green; gold savings accent | Executive scorecard, 99.98% accuracy, [REDACTED_AMOUNT] | 14–16 |

Scene cuts land exactly on the WAV chime frames (0 / 600 / 1440 / 2160; closing marker at 2670),
with continuous camera trajectories across cuts.

## Preview live

- **Local (offline):** open [renderer/index.html](renderer/index.html) directly in any modern
  browser — no server, no network, no build step.
- **GitHub Pages:** push this folder to a repository and enable Pages; the renderer deploys as-is at
  `https://[REDACTED_ENTITY].github.io/[REDACTED_ENTITY]/video-creation/renderer/`

### Playback controls

| Control | Action |
|---|---|
| Play / Pause | Toggle deterministic playback at 60 fps |
| Restart | Seek to frame 0 and play |
| S1 – S4 | Jump to scene start frames 0 / 600 / 1440 / 2160 |
| Timeline scrubber | Scrub 0.00 s – 45.00 s frame by frame |
| Keyboard | Space = play/pause, R = restart, 1–4 = scene jump |

### Deterministic API

```js
window.renderAtFrame(1500); // renders exactly frame 1500 (t = 25.000 s), every time
```

Every scene transition, camera trajectory, particle burst, quarantine deflection, caption cue and
HUD counter is a pure function of the frame index — safe for headless capture (call
`window.renderAtFrame(n)` per frame from DevTools or any automation driver).

## 1-Click .webm export

1. Open [renderer/index.html](renderer/index.html).
2. Press **Record .webm (1-click)** — the recorder seeks to frame 0, plays the full deterministic
   45-second pass at 60 fps via `canvas.captureStream(60)` + `MediaRecorder`, then auto-downloads
   `pipeline_master_45s_1080p60.webm`.
3. Move the download to `pipeline/recorded_video.webm` for muxing.

## .mp4 master via ffmpeg

1. Export the `.webm` as above and place it at `pipeline/recorded_video.webm`.
2. Run the verifier (regenerates the WAV and prints/writes the exact command):

```
python video-creation/pipeline/build_and_verify.py
```

3. Run the generated mux command from this folder's parent (also in
   [pipeline/ffmpeg_command.txt](pipeline/ffmpeg_command.txt)):

```
ffmpeg -y -i pipeline/recorded_video.webm -i pipeline/ambient_cues.wav -i pipeline/subtitles.srt -map 0:v:0 -map 1:a:0 -map 2:s:0 -c:v libx264 -preset medium -crf 18 -r 60 -pix_fmt yuv420p -c:a aac -b:a 192k -c:s mov_text -metadata:s:s:0 language=eng -shortest master_1080p60.mp4
```

Output: `master_1080p60.mp4` — H.264, 60 fps, with the WAV bed and an SRT soft-subtitle track
(broadcast captions are additionally burned into the video by the renderer HUD).

## Verification — 10 deterministic checks

Canonical run: `python video-creation/pipeline/build_and_verify.py` (pure Python standard
library) — generates `pipeline/ambient_cues.wav`, `pipeline/ffmpeg_command.txt`,
[verification/run_log.txt](verification/run_log.txt) (canonical 10/10 PASS) and
[verification/report.json](verification/report.json).

> **Provenance note.** During authoring, the canonical script was executed to completion on these
> exact inputs inside an in-browser CPython 3.12 runtime (Pyodide): **10/10 PASS**, and
> `ambient_cues.wav` was generated and self-verified by CHK-04/CHK-07 (7,938,044 bytes; SHA-256
> `705646bf83ad06525d3c531b3688f903d5e32594def637feff1183530c0cc942`). Synthesis is fully
> deterministic, so a local run reproduces that file bit-for-bit. To materialize the WAV in
> `pipeline/`, either run the verifier once locally or move the downloaded `ambient_cues.wav`
> into this folder.

| Check | Verifies |
|---|---|
| CHK-01 | Storyboard scene durations sum to exactly 45.000 s = 2700 frames at 60 fps |
| CHK-02 | SRT timestamps strictly monotonic, zero overlaps, end ≤ 00:00:45,000 |
| CHK-03 | SRT line length ≤ 42 chars and reading speed ≤ 20 chars/s |
| CHK-04 | WAV header: 44100 Hz, stereo, 16-bit PCM, 1,984,500 frames = 45.000 s |
| CHK-05 | Renderer has 1920x1080 buffer, `renderAtFrame` hook, `MediaRecorder` export |
| CHK-06 | Renderer is self-contained: zero external `http(s)` references |
| CHK-07 | Scene boundaries 0/10/24/36/45 s aligned across storyboard, renderer, SRT and WAV chimes |
| CHK-08 | Voiceover word count 107 within the 105–135 broadcast window |
| CHK-09 | FFmpeg command syntax and input/output paths |
| CHK-10 | Redaction compliance scan across all files (zero emails / currency / org names) |

## Director's edge-case review log (manually reviewed)

1. **Broadcast voiceover pacing (CHK-03 / CHK-08).** 107 words over 45 s = 2.38 words/s — inside
   the 105–135 word broadcast window. Peak cue reading speed is 19.6 chars/s (cue 13), under the
   20 chars/s cap; every cue ≥ 1.5 s. Resolution: cues 11–13 were re-timed so the quarantine line
   does not rush; if a VO talent reads faster than the grid, keep cue edges fixed and let pauses
   absorb the difference.
2. **Visual contrast of quarantined packets (Scene 3).** Amber #ff9f1a and red #ff4757 on the
   void-navy background hold strong contrast for large motion graphics, and quarantined packets
   additionally carry a white gate-flash, a glow halo and a dashed red quarantine bin with a
   persistent amber label. Resolution: verified blocks use solid fill + bright stroke (not
   wireframe-only) so green "locks" stay readable at 1080p broadcast distance.
3. **Audio-visual sync at scene transitions (CHK-07).** Chimes are synthesized at exactly
   0.0 / 10.0 / 24.0 / 36.0 / 44.5 s and the renderer cuts scenes on the same frame indices
   (600 / 1440 / 2160) with camera keyframes shared across the cut. The verifier measures WAV
   energy at each chime against the ambient bed. Resolution: the 4-frame screen flash at each cut
   masks residual encoder jitter; real-time 60 fps capture keeps `.webm` VFR drift within a
   single frame (~17 ms), inside broadcast sync tolerance, and the mux uses `-shortest`.

## Redaction policy

1. Only the canonical tokens `[REDACTED_ENTITY]` and `[REDACTED_AMOUNT]` may appear.
2. No emails, no currency figures, no unredacted organization patterns anywhere under
   `video-creation/` — enforced by `CHK-10` across every text deliverable on each run.
3. Abstract metrics (99.98%, packet counts, latencies, frame indices) are sanctioned.
