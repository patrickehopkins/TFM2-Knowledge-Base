# Simulation and visible replay are separate

**Status: runtime verified** across independently instrumented Harbinger, Flame Simulator and Berserker projects; exact mechanisms vary by build. Sources: [Harbinger simulation](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/simulation-research.md), Flame rewind (Flame Simulator source; private repository), Berserker Probe 002 (Berserker Keeps Yelling source; private repository).

A watched match's client simulation can finish far ahead of the on-screen playback clock. An AI callback tick **must not** be used as a direct presentation timestamp or wall-clock audio trigger.

## Concrete evidence

- Harbinger observed simulation/AI callbacks stop while the visible clock continued. A visual-clock-matched `StablePlayerAi` return did not produce authoritative interactive control. The old `match_view +0x250/+0x258` display-clock hypothesis was physically rejected.
- Flame 0.6.1 Probe 0.2.0 observed two deliberate rewinds from 00:06 and 00:05 to 00:00 while the sampled simulation stream continued forward; visible chat text remained immediately after seeks. First readable opening text occurred at displayed 00:02 on multiple passes but differed in wording. The *first readable poll* is not an exact native spawn instant.
- Berserker 0.6.3 Probe 002 observed Candidate-A tick `36,471` (~10:07.85 at 60 tps) by visible HUD **00:47**; the rendered match continued to **10:07** while the watched simulation's tick had stopped increasing.

## Watcher versus authority

Creep Chaos Probe 002 physically revalidated watched ClientMatchView Candidate A on its exact 0.6.3 build, but explicitly does **not** treat it as the authoritative simulation mutation surface. The stable `StableMatchHook` handles deterministic game-rule mutations; a watched-client/native hook is for observation or presentation. The engine can maintain more than one simulation context.

## Practical consequences

- Keep simulation tick, presentation clock, wall clock, scene epoch, and instance identity as **separate fields**.
- Replay rewind must not replay irreversible persistent career mutations, simply because the visible clock moved backward.
- For audio, investigate frame-recorded sound events; do not trigger client sound directly from a presimulation callback.
- For multiplayer, first prove vanilla peer state equivalence before injecting externally synchronized inputs.

## Not yet proved

These observations do **not** disclose a sample-accurate presentation clock, unique cross-match ID, general determinism of repeated fresh matches, or the exact native chat event queue. Do not infer those capabilities from a few matched timestamps.
