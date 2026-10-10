# Source-project index and provenance

Initial selection compiled **2026-10-09** from technical documents in five separate TFM2 mod projects. Four of the source repositories are not publicly accessible; their original Markdown reports are **not** republished or linked here. This knowledge base summarizes reusable findings with their own evidence status and game-version limits.

| Project | Source documents consulted | Reusable subject | Access |
| --- | --- | --- | --- |
| [Harbinger Direct Control](https://github.com/patrickehopkins/TFM2-DirectControl) | [Simulation research](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/simulation-research.md), [Native crash postmortem](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/native-hook-crash-postmortem.md), [Camera](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/camera-research.md) | Simulation workers, replay ownership, camera, native patch safety | Public |
| Flame Simulator | `docs/REWIND-EVIDENCE.md`, `docs/TRAIT-MAPPING-2026-09-27.md`, `docs/STATUS.md` | Replay, UI observations, athlete/profile data, SDK ABI | Private source; standalone summaries here |
| Creep Chaos | `docs/PROBE-002-FINDINGS.md`, `docs/PROBE-008-FINDINGS.md`, `docs/PROBE-010G-MINION-EFFECT-HANDOFF.md`, `docs/PROBE-010J-RESULTS.md`, `docs/PROBE-010K4-W-PHASE-CORRECTION.md` | Watched simulation, creep presentation, original action timing, effect execution and corrected Knight W control flow | Private source; summarized here |
| Berserker Keeps Yelling | `docs/PROBE-001-FINDINGS.md` through `docs/PROBE-006-FINDINGS.md`, `docs/AUDIO-VOICE-PROBE-A-FINDINGS.md` (game 0.6.3 / SDK ABI 9; audio probe standalone Windows) | 179-tick buff duration, ahead-of-time simulation, audible client WAV, failed custom SFX binding, complete bounded UI-clock search, **standalone** dual-handle audible stop | Private source; standalone summaries here |
| Dynasties | `docs/technical-probes.md` | Proposed athlete identity, persistence, roster lifecycle experiments — **not verified** | Private source; plans only |

**Provenance limitation:** the private originals may not be independently inspectable by public readers. Please treat each public summary's reproducibility guidance and specific evidence limitations as essential, and add sanitized public reproductions when available. Original projects remain authoritative for their implementation-specific source, logs, and runbooks. No private logs, unpublished code, audio, or game assets are packaged here.
