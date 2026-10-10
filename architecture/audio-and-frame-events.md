# Gameplay buff observations versus audible playback

**Status:** Runtime verified on **TFM2 0.6.3 / stable ABI 9**, from Berserker Keeps Yelling Probes 001–006 (2026-10-09). **Unresolved in TFM2:** sample-accurate playback tick, per-voice stop in the game process, and native death event ordering. **Standalone Windows voice-stop feasibility now runtime verified** (Audio Voice Probe A, 2026-10-09).

## Simulation state is not the playback clock

Berserker's observed `berserker_skill1` buff repeatedly lasted exactly **179 simulation ticks** for naturally completed intervals. Probe 006 recorded **91 additions**, **88 normal removals**, and three disappearances while the buff was active. The disappearances reported nonzero previous-tick HP and `alive=true`: they are *death/despawn candidates*, not verified death events. The 179-tick buff remains a **strong Rage candidate**, not a visually cross-validated Rage identification.

Probe 002 found that watched simulation reached **36,471** (~10:08 at 60 tps) while the visible HUD was only at **00:47**. Simulation callbacks therefore cannot trigger audible clips at the observed tick without a separate presentation-time mechanism.

## Sound-event APIs are not interchangeable

**Runtime verified:** Probe 003 played a quiet mod-owned synthetic WAV via `StableClient::play_sound(path, volume)` on F8; the owner heard it. Probe 004 then played the same file through a HUD-clock-triggered `play_sound` at visible **00:10**, and the owner heard both the manual and automatic beeps. This demonstrates **coarse client presentation-time one-shot audio**, not precise replay scheduling.

**Runtime negative evidence:** Probe 003 called `StableSim::play_sfx(name, caster_id, target)` from the scheduled match hook at tick 600, but the owner could not hear the expected 00:10 sound. The official [stable API](https://github.com/teamsamoyed/TeamfightManager2Mod/blob/main/docs/stable-api-reference.md) describes `play_sfx` as a *view-effect name* that must already have a corresponding client binding. The experiment instead used a custom **file path**. That binding mismatch is a **plausible explanation, not proved exclusive cause**. It does not disprove the properly bound frame-event pipeline.

**API documentation evidence:** `play_sound` has no documented individual sound voice handle or per-voice stop operation. Do **not** assume arbitrary 3+ second sounds can be interrupted using this method. Do not hijack global `play_bgm` / `stop_bgm` for independent champion voices.

## Independently stoppable Windows audio voices — standalone proof, not TFM2 integration

**Runtime verified (user auditory report, 2026-10-09):** Berserker *Audio Voice Probe A* ran as a separate Windows process (Rust `src/bin/voice_probe.rs`; OS **WinMM** `waveOut`, not XAudio2). It generated two low-level, 16-bit PCM notes (440 and ~659 Hz), started them on separate output handles, reset the first handle after about 0.9 s and the second after about 2.1 s. The tester reported hearing **both tones, then one tone, then silence**. That is evidence that one sound stopped while the other continued audibly in this standalone setup.

**Not verified:** running concurrently with TFM2's own audio, running inside a mod DLL, game master/SFX volume integration, measured stop latency, replay pause/seek handling, lifecycle cleanup under stress, or XAudio2 behavior. This test demonstrates a **general Windows per-handle audio capability**, not a game SDK stop handle and not a final WinMM backend decision.

**Next control:** repeat the *same unmodified standalone executable* while TFM2 plays ordinary match audio and check that game sound remains audible/unaffected. Then, if useful, evaluate a modern owned XAudio2 voice inside the mod under strict version/mixer/lifecycle tests. For exact Rage interruption timing, native *presentation* playback tracking still remains separate.

### Standalone follow-up with TFM2 running

**Runtime verified (audible tones, 2026-10-09):** the owner repeated the standalone WinMM dual-handle test with TFM2 running, using an optional startup delay, and again heard two tones, followed by one, then silence. This reinforces that independent stopping is reproducible while TFM2 is open. **No explicit report confirmed whether TFM2's own sound remained continuously audible, unducked or unaffected.** The test still ran in a separate process, not inside the mod DLL. Probe 007 is an **unverified source-only** experiment designed to test F10-triggered WinMM audio handles inside the existing stable-client extension. Its compilation, mixer behavior and cleanup are pending.

## Playback-clock UI negative experiment

- Probe 005 depth-first UI scan was **inconclusive**: it exhausted 1,202 nodes / 36 matches, mostly on unrelated athlete/champion *speed* labels. Twenty-nine samples returned no slider ratios.
- Probe 006 replaced it with a bounded **breadth-first** SDK UI scan (max depth 13, 12k-node limit, 150 nodes/client update). It **drained its queue after 3,189 visited nodes** (`truncated=false`) and collected **30** subsequent samples.
- No retained candidate was a slider runner; all 30 samples had `ratios=[]`. Only the whole-second `ingame.header.game_time.value` was identified as a useful time label.
- **Scope:** no high-resolution playback cursor was found **in the UI tree exposed to this scan**. This does not prove the native replay has no fine-grained cursor or that deeper/inaccessible UI state does not exist.

## Implications and remaining tests

1. Separate presimulation tick, rendered replay cursor, monotonic wall time, scene epoch, and champion identity. The HUD's integer seconds are insufficient for a 179-tick effect's exact entry/exit.
2. Use native presentation-state investigation (exact build fingerprint and fail-closed reads) instead of repeating an unchanged UI traversal.
3. Two standalone WinMM listening tests, one with TFM2 open, have **audibly proven independent per-handle stopping**; next prove uninterrupted game-audio coexistence and controlled in-process lifetime. Windows XAudio2 source voices remain a **documented but untested alternative**, with game volume integration unknown.
4. Prove true death callback/order and multiple-Berserker handling. Despawn is not the same as an observed death.

**Source reports (private project, titles only):** `TFM2-Berserker-Keeps-Yelling/docs/PROBE-003-FINDINGS.md`, `PROBE-004-FINDINGS.md`, `PROBE-005-FINDINGS.md`, and `PROBE-006-FINDINGS.md`, plus `AUDIO-VOICE-PROBE-A-FINDINGS.md`. The originating repository is currently private; no private deep links, raw logs, or proprietary assets are republished here.
