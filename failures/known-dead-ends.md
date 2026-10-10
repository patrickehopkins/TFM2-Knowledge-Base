# Negative evidence and known failure modes

Failures are retained here because they prevent repeated unsafe work.

| Investigation | Result | Scope |
| --- | --- | --- |
| Harbinger native common-loop 16-byte detour | **Unsafe**: an existing branch entered the patched span mid-way; three repeatable launch crashes | historical 0.5.8 native RVA; see [postmortem](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/native-hook-crash-postmortem.md) |
| Harbinger `match_view+0x250/+0x258` as visible clock | **Disproven** by physical clock validation; `+0x250` remained 1 while display time advanced | original Harbinger historical probe; [simulation study](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/simulation-research.md) |
| `StablePlayerAi` callback gated to visible clock to direct a champion | **Did not establish control**; callbacks may finish ahead of visible playback | Harbinger historical research |
| Creep Chaos base resource swap alone | Native minion became **invisible**; required downstream animation-key adaptation | 0.6.3 Probe 006, later corrected by successful Probe 008 |
| Creep Chaos Probe 007 animation resolver RVA | **Fail-closed preflight**, wrong by 0x1000; no mutation ran, so no conclusion about animation-key theory | 0.6.3; Probe 007 (Creep Chaos source; private repository) |
| Assuming `berserker_skill1` expiry corresponds to visible sound timing | **Unsupported**; Candidate-A presimulation finished long before visible playback | 0.6.3 Berserker Probe 002 |
| Interpreting a Berserker disappearance as a confirmed death | **Unsupported** across Probes 001–006: despawn was observed with stale nonzero HP / alive=true; three Rage-interruption candidates in Probe 006, still no native death event | 0.6.3 Berserker Probes 001–006 |

| Sending a custom file asset path as a `play_sfx` view-effect name | **Inaudible** in Probe 003 despite confirmed dispatch; requires a recognized client binding, which was not verified. Does not disprove frame-recorded SFX generally | 0.6.3 Berserker Probe 003; contrast audible `play_sound` in Probes 003/004 |
| Assuming stable UI provides a precise replay slider | Probe 005 DFS inconclusive/truncated; Probe 006 full bounded BFS (3,189 nodes, depth cap 13) found no slider runner/ratio and only whole-second clock | 0.6.3 Berserker Probes 005/006; absence not general to native internals |

Do not copy conclusions between game versions without recreating relevant evidence. When a failed approach is later fixed, retain the original failure and link the passing follow-up.
