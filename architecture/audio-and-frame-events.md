# Gameplay buff observations versus audible playback

**Status:** TFM2 **0.6.3 / stable ABI 9**, runtime evidence through Berserker Probe **008** (2026-10-11). **Verified:** custom WAV playback during visible HUD time, standalone and in-process independent WinMM voices, manual one-voice-at-a-time interruption with ordinary game audio continuing. **Unresolved:** precise native replay cursor, real Rage/death event timing, pause/seek semantics, game mute/gain mapping, DLL unload/forced process shutdown and other game versions. **Eight-second watchdog and active-voice return-to-title cleanup are now verified** in Probe 008's lifecycle follow-up.

## Simulation state is not the playback clock

Berserker's observed `berserker_skill1` buff repeatedly lasted exactly **179 simulation ticks** for naturally completed intervals. Probe 006 recorded **91 additions**, **88 normal removals**, and three disappearances while the buff was active. The disappearances reported nonzero previous-tick HP and `alive=true`: they are *death/despawn candidates*, not verified death events. The 179-tick buff remains a **strong Rage candidate**, not a visually cross-validated Rage identification.

Probe 002 found that watched simulation reached **36,471** (~10:08 at 60 tps) while the visible HUD was only at **00:47**. Simulation callbacks therefore cannot trigger audible clips at the observed tick without a separate presentation-time mechanism.

## Sound-event APIs are not interchangeable

**Runtime verified:** Probe 003 played a quiet mod-owned synthetic WAV via `StableClient::play_sound(path, volume)` on F8; the owner heard it. Probe 004 then played the same file through a HUD-clock-triggered `play_sound` at visible **00:10**, and the owner heard both the manual and automatic beeps. This demonstrates **coarse client presentation-time one-shot audio**, not precise replay scheduling.

**Runtime negative evidence:** Probe 003 called `StableSim::play_sfx(name, caster_id, target)` from the scheduled match hook at tick 600, but the owner could not hear the expected 00:10 sound. The official [stable API](https://github.com/teamsamoyed/TeamfightManager2Mod/blob/main/docs/stable-api-reference.md) describes `play_sfx` as a *view-effect name* that must already have a corresponding client binding. The experiment instead used a custom **file path**. That binding mismatch is a **plausible explanation, not proved exclusive cause**. It does not disprove the properly bound frame-event pipeline.

**API documentation evidence:** `play_sound` has no documented individual sound voice handle or per-voice stop operation. Do **not** assume arbitrary 3+ second sounds can be interrupted using this method. Do not hijack global `play_bgm` / `stop_bgm` for independent champion voices.

## Independent audio voices: evidence ladder

**Standalone runtime verified, 2026-10-09 (Audio Voice Probe A):** WinMM `waveOut` used two distinct handles for self-generated 440 Hz and ~659 Hz PCM tones. The tester heard two tones, then one, then silence after individual handle resets. A second standalone run with TFM2 open confirmed the same note sequence, but game-sound continuity was not explicitly reported at that stage. This was **not** an SDK-owned stop API or XAudio2.

**In-process runtime verified, 2026-10-09 (Berserker Probe 007, v0.0.7):** In TFM2 0.6.3, the mod client's explicit F10 test started two synthetic WinMM voices; callback stop requests occurred at **903 ms** and **2105 ms**, and the tester heard the two-to-one-to-silence sequence. This proved in-process independent sound stopping, but not that the game's original audio continued unaltered.

**Manual interruption + native sound coexistence verified, 2026-10-11 (Berserker Probe 008, v0.0.8):** The user heard **two successful F10 start-both → stop-low-only → stop-high sequences**, and explicitly reported that TFM2's normal audio continued. Separate stop-request callbacks were logged at **2166/3891 ms** in the first sequence and **1756/3386 ms** in the second. No audio-error marker was reported. This is a **real in-process, game-audio-coexisting demonstration** with generated tones—not a claim of calibrated speaker latency, per-champion voice ownership, or full Rage integration.

**Further lifecycle runtime verified (2026-10-11; Berserker Probe 008, v0.0.8):** The owner confirmed two additional sound behaviors while watching TFM2 0.6.3, with matching diagnostic evidence.

- **Watchdog:** an F10 start left both WinMM voices active; without another F10, the client logged `VOICE_INPROCESS_CLEANUP reason=watchdog_8_seconds low_active=true high_active=true`. The owner heard both notes stop. The log has no calibrated speaker-out latency and no exact watchdog elapsed-ms value.
- **Title-screen exit:** in a separate run, both voices were still active when the stable-client callback logged `VOICE_INPROCESS_CLEANUP reason=left_ingame_scene low_active=true high_active=true`; immediately afterward the UI logger recorded an `InGame → Title` transition. The owner confirmed the sounds stopped while **TFM2 stayed running**.
- **Useful negative control:** an earlier exit attempt quit TFM2 to Windows while sound was active. The process stopping sound is **not evidence** of clean mod/DLL unload. That trial did not contain the positive client cleanup marker and remains inconclusive.
- **Concurrency boundary:** diagnostics from the watched simulation still continued after the title transition. A running simulation worker does **not** imply an active client match presentation. Audio teardown must be tied to the relevant client scene or playback epoch.

**Still open:** game volume/mute linkage (independent WinMM need not follow TFM2's settings), forced DLL unload/crash safety, seek/pause/speed, multiple champion voices, native Rage/death events, clip streaming and rights, measured speaker-stop latency, and XAudio2. The prior Probe 008 manual-stop run transitioned to results only **after** the sounds ended; the *later* separate return-to-title test is what establishes active-voice cleanup.

**Source provenance:** Originating private Berserker Keeps Yelling reports `docs/AUDIO-VOICE-PROBE-A-FINDINGS.md`, `docs/PROBE-007-FINDINGS.md`, and `docs/PROBE-008-FINDINGS.md`. No raw logs or private source links are republished.

## Playback-clock UI negative experiment

- Probe 005 depth-first UI scan was **inconclusive**: it exhausted 1,202 nodes / 36 matches, mostly on unrelated athlete/champion *speed* labels. Twenty-nine samples returned no slider ratios.
- Probe 006 replaced it with a bounded **breadth-first** SDK UI scan (max depth 13, 12k-node limit, 150 nodes/client update). It **drained its queue after 3,189 visited nodes** (`truncated=false`) and collected **30** subsequent samples.
- No retained candidate was a slider runner; all 30 samples had `ratios=[]`. Only the whole-second `ingame.header.game_time.value` was identified as a useful time label.
- **Scope:** no high-resolution playback cursor was found **in the UI tree exposed to this scan**. This does not prove the native replay has no fine-grained cursor or that deeper/inaccessible UI state does not exist.

## Implications and remaining tests

1. Separate presimulation tick, rendered replay cursor, monotonic wall time, scene epoch, and champion identity. The HUD's integer seconds are insufficient for a 179-tick effect's exact entry/exit.
2. Use native presentation-state investigation (exact build fingerprint and fail-closed reads) instead of repeating an unchanged UI traversal.
3. Probe 008 confirmed **two early/manual in-process WinMM stop sequences while normal game audio continued**; subsequent owner-run follow-ups confirmed **both-voice watchdog timeout and return-to-title cleanup**. Focus next on exact playback Rage/death triggers, pause/seek, and forced-unload robustness—not repeating basic two-tone feasibility. XAudio2 remains a documented, untested alternative.
4. Prove true death callback/order and multiple-Berserker handling. Despawn is not the same as an observed death.

**Source reports (private project, titles only):** `TFM2-Berserker-Keeps-Yelling/docs/PROBE-003-FINDINGS.md`, `PROBE-004-FINDINGS.md`, `PROBE-005-FINDINGS.md`, and `PROBE-006-FINDINGS.md`, plus `AUDIO-VOICE-PROBE-A-FINDINGS.md`, `PROBE-007-FINDINGS.md`, and `PROBE-008-FINDINGS.md`. The originating repository is currently private; no private deep links, raw logs, or proprietary assets are republished here.
