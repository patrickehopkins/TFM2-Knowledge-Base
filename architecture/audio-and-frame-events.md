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


## Third-party custom champion audio asset pipeline (static evidence, 2026-10-12)

**Status:** **static evidence only** from an uploaded copy of Workshop package `3774304166`, identified by its bundled metadata as *Silver's League of Legend Reborn* (`test_mod`, package metadata version `0.1.0`). **Game version not established:** the package includes an older minimum `base >=0.4.11` dependency and workshop-note filenames, neither of which proves an exact runtime-tested build. This package was inspected but **not installed, executed, or tested against TFM2 0.6.3**.

A custom champion's declarative effect can specify `{"type":"Sfx","name":"example_cast"}` (or `TargetSfx`). A `sound/sfx/example_cast.sound_info` file provides a `plays` array; each entry has a `clip` asset name, `delay` and `volume`. The package registers sound definitions and individual clips through `mod.override_info` mappings from `asset/base/sound/sfx/...` to `asset/<mod_id>/sound/sfx/...`. External `.wav` and `.mp3` assets exist alongside these declarations. In this snapshot there are 111 `.sound_info` entries, 98 WAV clips, 13 MP3 clips, and 206 sound-path override entries. Counts describe the archive, **not** which entries successfully play.

The `plays` array can declare multiple clips/delays for one event (example patterns include 0 and 0.15 second entries, or repeated clips). This is evidence of an authored scheduling *format*, **not** verification of playback fidelity, looping, cancellation, audio handle ownership, pause behavior, or replay synchronization.

**Relationship to Berserker probes:** earlier Probe 003's inaudible `StableSim::play_sfx` used a file path instead of a bound sound-event name; this third-party asset layout strengthens the **binding-mismatch hypothesis** but does not prove it was the exclusive cause. WinMM Probe 007/008's individually stoppable audio remains separately runtime verified. A native sound definition and an interruptible per-voice audio backend should **not** be assumed equivalent.

**Further original-EXE static evidence (Berserker 010A–010H, owner-run 2026-10-13, exact 0.6.3):** Non-executable PE sections contained **3 `sound_info` token occurrences, 29 `sound/sfx` and 75 `sfx`** ASCII occurrences. The scanner decoded **33** candidate sound-associated RIP-relative LEA reference sites, among 383 total mixed-category references. These values are **string/xref censuses only**; some occurrences may be unrelated, and 010's analysis of native ownership was capped at 90 of 190 unwind groups. They do **not** demonstrate a registered Sfx playing or per-voice native interruption. The next offline investigation aims to distinguish actual sound-definition names from generic Sfx strings and inspect additional RIP-relative memory opcodes. The user did not provide the optional local sound package inventory input to that scan.

**Later original-EXE static evidence (Berserker 011A–011P, owner-run 2026-10-13, exact 0.6.3):** the expanded native RIP-memory decoder found **11 `sound_info`/`sound/sfx` reference sites**, all `lea` in this search, across eight unwind-owner ranges. A sound-path-named function (RVA begin `0x00930640`) contained two decoded direct calls to a `game_time`-label-bearing function (begin `0x00B9C970`). This is **not** evidence of audio playback-clock coupling: both strings might be used by general resource/configuration handling. The sweep stopped at a **12-million-instruction limit**, so a later scan must validate coverage. Neither named Sfx registration, audible named playback, individual sound cancellation nor a native mixer interface was proven. The standard import census did locate `winmm.dll`, but an imported DLL alone does not establish the specific native voice engine or stop semantics.

**Next tests:** construct mod-owned synthetic test tone with `.sound_info`, asset mappings, and a valid named Sfx invocation; verify audible playback on the exact target build (0.6.3), then test whether native playback exposes per-instance stopping and whether events emitted from presimulation are heard during visible replay. Avoid distributing third-party sound files or copying proprietary assets.

**Provenance/limitations:** user-supplied third-party Workshop archive `3774304166.zip`, reviewed 2026-10-12; no third-party recordings, binary, personal local paths, or raw logs included here. This is independent package inspection, not a claim about the original author's test results.
