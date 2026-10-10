# Gameplay buff observations versus audible playback

**Status:** Runtime verified on **TFM2 0.6.3 / stable ABI 9**, from Berserker Keeps Yelling Probes 001–006 (2026-10-09). **Unresolved:** sample-accurate playback tick, mid-clip voice stop, and native death event ordering.

## Simulation state is not the playback clock

Berserker's observed `berserker_skill1` buff repeatedly lasted exactly **179 simulation ticks** for naturally completed intervals. Probe 006 recorded **91 additions**, **88 normal removals**, and three disappearances while the buff was active. The disappearances reported nonzero previous-tick HP and `alive=true`: they are *death/despawn candidates*, not verified death events. The 179-tick buff remains a **strong Rage candidate**, not a visually cross-validated Rage identification.

Probe 002 found that watched simulation reached **36,471** (~10:08 at 60 tps) while the visible HUD was only at **00:47**. Simulation callbacks therefore cannot trigger audible clips at the observed tick without a separate presentation-time mechanism.

## Sound-event APIs are not interchangeable

**Runtime verified:** Probe 003 played a quiet mod-owned synthetic WAV via `StableClient::play_sound(path, volume)` on F8; the owner heard it. Probe 004 then played the same file through a HUD-clock-triggered `play_sound` at visible **00:10**, and the owner heard both the manual and automatic beeps. This demonstrates **coarse client presentation-time one-shot audio**, not precise replay scheduling.

**Runtime negative evidence:** Probe 003 called `StableSim::play_sfx(name, caster_id, target)` from the scheduled match hook at tick 600, but the owner could not hear the expected 00:10 sound. The official [stable API](https://github.com/teamsamoyed/TeamfightManager2Mod/blob/main/docs/stable-api-reference.md) describes `play_sfx` as a *view-effect name* that must already have a corresponding client binding. The experiment instead used a custom **file path**. That binding mismatch is a **plausible explanation, not proved exclusive cause**. It does not disprove the properly bound frame-event pipeline.

**API documentation evidence:** `play_sound` has no documented individual sound voice handle or per-voice stop operation. Do **not** assume arbitrary 3+ second sounds can be interrupted using this method. Do not hijack global `play_bgm` / `stop_bgm` for independent champion voices.

## Playback-clock UI negative experiment

- Probe 005 depth-first UI scan was **inconclusive**: it exhausted 1,202 nodes / 36 matches, mostly on unrelated athlete/champion *speed* labels. Twenty-nine samples returned no slider ratios.
- Probe 006 replaced it with a bounded **breadth-first** SDK UI scan (max depth 13, 12k-node limit, 150 nodes/client update). It **drained its queue after 3,189 visited nodes** (`truncated=false`) and collected **30** subsequent samples.
- No retained candidate was a slider runner; all 30 samples had `ratios=[]`. Only the whole-second `ingame.header.game_time.value` was identified as a useful time label.
- **Scope:** no high-resolution playback cursor was found **in the UI tree exposed to this scan**. This does not prove the native replay has no fine-grained cursor or that deeper/inaccessible UI state does not exist.

## Implications and remaining tests

1. Separate presimulation tick, rendered replay cursor, monotonic wall time, scene epoch, and champion identity. The HUD's integer seconds are insufficient for a 179-tick effect's exact entry/exit.
2. Use native presentation-state investigation (exact build fingerprint and fail-closed reads) instead of repeating an unchanged UI traversal.
3. Before long voice clips, prove independent **owned** audio start/stop/pause/cleanup using a generated sample. Windows XAudio2 source voices are a **documented OS-level candidate**, not a TFM2-tested integration; own-game volume settings and mix coexistence need verification.
4. Prove true death callback/order and multiple-Berserker handling. Despawn is not the same as an observed death.

**Source reports:** [Berserker Probe 003 findings](https://github.com/patrickehopkins/TFM2-Berserker-Keeps-Yelling/blob/main/docs/PROBE-003-FINDINGS.md), [Probe 004 findings](https://github.com/patrickehopkins/TFM2-Berserker-Keeps-Yelling/blob/main/docs/PROBE-004-FINDINGS.md), [Probe 005 findings](https://github.com/patrickehopkins/TFM2-Berserker-Keeps-Yelling/blob/main/docs/PROBE-005-FINDINGS.md), [Probe 006 findings](https://github.com/patrickehopkins/TFM2-Berserker-Keeps-Yelling/blob/main/docs/PROBE-006-FINDINGS.md). Raw logs remain in the original project workflow and are not copied here.
