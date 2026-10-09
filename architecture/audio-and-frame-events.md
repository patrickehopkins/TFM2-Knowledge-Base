# Gameplay buff observations versus audible playback

**Status: buff/timeline observation verified on 0.6.3; sound-event delivery remains unproven in the cited Probe 003 runbook.** Sources: Berserker Probe 001 (Berserker Keeps Yelling source; private repository), 002 (Berserker Keeps Yelling source; private repository), 003 runbook (Berserker Keeps Yelling source; private repository).

Probe 001 measured 37 complete `berserker_skill1` buff intervals, each 179 sampled simulation ticks; Probe 002 measured 40 complete intervals, again all 179 ticks. This identifies a reliable **Rage-like buff candidate**, not yet an independently proven audio cue or fully verified exact Rage identity. Disappearing entities were last observed alive with nonzero HP; these probes did not directly prove an in-Rage death transition.

In Probe 002, watched simulation reached tick 36,471 while visible HUD showed 00:47, establishing why starting sound directly from the watched-simulation callback would be badly out of sync.

The stable API documentation described `StableSim::play_sfx(name, caster_id, target)` as a recorded frame event and a client-side `StableClient::play_sound(path, volume)` without a documented individual voice-stop handle. The proposed Probe 003 tests a quiet synthetic ping from each pathway, with a tick-600 frame event expected around visible 00:10. **This is a test plan, not a reported successful audible result.**

Do not build uninterruptible long playback on the assumption that the frame-event API supports stopping an individual voice, seeking, or guaranteed one-shot death handling. Those are separate proof targets.
