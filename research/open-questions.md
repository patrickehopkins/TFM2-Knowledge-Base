# High-value open investigations

These are **questions or test plans**, not completed discoveries.

1. **Exact playback event timing:** Berserker Probes 005 and 006 found no high-resolution replay cursor in the tested SDK-visible UI (Probe 005 search truncated; Probe 006 BFS drained after 3,189 nodes at depth ≤13). Investigate native presentation state on exact TFM2 0.6.3 fingerprint, or properly bound frame-recorded SFX, including pause/seek/speed behavior. Private Berserker source, Probe 006 findings.
2. **Champion ability plumbing on native creeps:** Probe 008 proved Knight-bodied rendering and proof-state persistence, not built-in Knight skill invocation or targeting. Probe 008 (Creep Chaos source; private repository).
3. **Multiplayer authority and deterministic peer state:** verify vanilla watched-simulation equivalence and first divergence before transporting human inputs. [Harbinger research plan](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/multiplayer-research.md). No networking compatibility claim.
4. **Athlete lifecycle / identity stability:** census across season transitions, saves and reloads, transfers/retirement, stable IDs, roster minimum, forfeits and auto-recruitment. Dynasties probe plan (Dynasties source; private repository).
5. **General native-hook coexistence:** determine whether independent mods can safely hook the same version-gated entrypoint concurrently; isolated passes are not enough.
6. **Audio voice ownership:** F8 `StableClient::play_sound` and visible-HUD-triggered 00:10 synthetic WAV were audibly confirmed in Berserker Probes 003/004; the stable SDK does not document a per-voice stop handle. Test a standalone independently stoppable Windows audio backend (WinMM feasibility and XAudio2 candidate) and then game co-existence, death interruption and seek teardown. This is an open experiment, not a verified TFM2 integration.
7. **Version migrations:** re-identify native addresses and field layouts for each new executable fingerprint, with runtime smoke tests.

For each resolved question: preserve the original implementation-specific report in its mod repository, publish the generalized result here, and explicitly mark what remains unproven.
