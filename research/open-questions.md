# High-value open investigations

These are **questions or test plans**, not completed discoveries.

1. **Exact playback event timing:** locate trustworthy render/replay timeline events or verify frame-recorded SFX at visible time, including pauses, rewinds and seeks. Berserker plan (Berserker Keeps Yelling source; private repository).
2. **Champion ability plumbing on native creeps:** Probe 008 proved Knight-bodied rendering and proof-state persistence, not built-in Knight skill invocation or targeting. Probe 008 (Creep Chaos source; private repository).
3. **Multiplayer authority and deterministic peer state:** verify vanilla watched-simulation equivalence and first divergence before transporting human inputs. [Harbinger research plan](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/multiplayer-research.md). No networking compatibility claim.
4. **Athlete lifecycle / identity stability:** census across season transitions, saves and reloads, transfers/retirement, stable IDs, roster minimum, forfeits and auto-recruitment. Dynasties probe plan (Dynasties source; private repository).
5. **General native-hook coexistence:** determine whether independent mods can safely hook the same version-gated entrypoint concurrently; isolated passes are not enough.
6. **Native audio voice ownership:** test individual sound stop/cancel behavior, death interruption and seek teardown, rather than assuming `play_sound` returns a stop handle.
7. **Version migrations:** re-identify native addresses and field layouts for each new executable fingerprint, with runtime smoke tests.

For each resolved question: preserve the original implementation-specific report in its mod repository, publish the generalized result here, and explicitly mark what remains unproven.
