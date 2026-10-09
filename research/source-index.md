# Source-project index and provenance

Initial selection compiled **2026-10-09** from technical documents in five separate TFM2 mod projects. Four of the source repositories are not publicly accessible; their original Markdown reports are **not** republished or linked here. This knowledge base summarizes reusable findings with their own evidence status and game-version limits.

| Project | Source documents consulted | Reusable subject | Access |
| --- | --- | --- | --- |
| [Harbinger Direct Control](https://github.com/patrickehopkins/TFM2-DirectControl) | [Simulation research](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/simulation-research.md), [Native crash postmortem](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/native-hook-crash-postmortem.md), [Camera](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/camera-research.md) | Simulation workers, replay ownership, camera, native patch safety | Public |
| Flame Simulator | `docs/REWIND-EVIDENCE.md`, `docs/TRAIT-MAPPING-2026-09-27.md`, `docs/STATUS.md` | Replay, UI observations, athlete/profile data, SDK ABI | Private source; standalone summaries here |
| Creep Chaos | `docs/PROBE-002-FINDINGS.md`, `docs/PROBE-007-FINDINGS.md`, `docs/PROBE-008-FINDINGS.md`, `docs/PRESENTATION-RE.md` | Watched simulation identification, creep identity, render resources and animation keys | Private source; standalone summaries here |
| Berserker Keeps Yelling | `docs/PROBE-001-FINDINGS.md`, `docs/PROBE-002-FINDINGS.md`, `docs/PROBE-003-RUNBOOK.md` | Buff observation, simulation/presentation lag, audio-event hypothesis | Private source; standalone summaries here |
| Dynasties | `docs/technical-probes.md` | Proposed athlete identity, persistence, roster lifecycle experiments — **not verified** | Private source; plans only |

**Provenance limitation:** the private originals may not be independently inspectable by public readers. Please treat each public summary's reproducibility guidance and specific evidence limitations as essential, and add sanitized public reproductions when available. Original projects remain authoritative for their implementation-specific source, logs, and runbooks. No private logs, unpublished code, audio, or game assets are packaged here.
