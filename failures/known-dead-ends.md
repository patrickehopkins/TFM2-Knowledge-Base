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
| Interpreting a Berserker disappearance as a confirmed death | **Unsupported** by first two probes: no direct death transition | 0.6.3 Berserker Probes 001/002 |

Do not copy conclusions between game versions without recreating relevant evidence. When a failed approach is later fixed, retain the original failure and link the passing follow-up.
