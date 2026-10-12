# Simulation and visible replay are separate

**Status: runtime verified** across independently instrumented Harbinger, Flame Simulator and Berserker projects; exact mechanisms vary by build. Sources: [Harbinger simulation](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/simulation-research.md), Flame rewind (Flame Simulator source; private repository), Berserker Probe 002 (Berserker Keeps Yelling source; private repository).

A watched match's client simulation can finish far ahead of the on-screen playback clock. An AI callback tick **must not** be used as a direct presentation timestamp or wall-clock audio trigger.

## Concrete evidence

- Harbinger observed simulation/AI callbacks stop while the visible clock continued. A visual-clock-matched `StablePlayerAi` return did not produce authoritative interactive control. The old `match_view +0x250/+0x258` display-clock hypothesis was physically rejected.
- Flame 0.6.1 Probe 0.2.0 observed two deliberate rewinds from 00:06 and 00:05 to 00:00 while the sampled simulation stream continued forward; visible chat text remained immediately after seeks. First readable opening text occurred at displayed 00:02 on multiple passes but differed in wording. The *first readable poll* is not an exact native spawn instant.
- Berserker 0.6.3 Probe 002 observed Candidate-A tick `36,471` (~10:07.85 at 60 tps) by visible HUD **00:47**; the rendered match continued to **10:07** while the watched simulation's tick had stopped increasing.

## Probe 009A: static replay/HUD anchor reconnaissance (not a clock)

**Static evidence, not runtime validation; exact TFM2 0.6.3 executable (2026-10-11):** An offline original-EXE scan from Berserker Keeps Yelling Probe 009A recorded SHA-256 `f21cf691799a83d9afa0ccae3e2b95862f5780446a501ee97860b91b752dbe2f`, PE timestamp `0x6AC5C567`, image size `0x052D6000`. The scanner found **4** `game_time` substring occurrences and **3** possible RIP-relative LEA-shaped source references (RVAs `0x009106D4`, `0x00B9D243`, `0x00B9D3BA`). It also found 43 `replay` and 41 `seek` occurrences, but **retained only the first 24 per token**, so those sets were truncated. Other exact tokens—including `ingame.header`, `current_frame` and `frame_index`—had zero string matches.

These are **limited string/byte-pattern matches**, not disassembled or instruction-boundary-verified references, time-update functions, playback counters, or safe hook sites. The lack of a literal UI string does not imply its UI node or semantic behavior is absent. **Probe 009B was subsequently run on that exact EXE (static evidence, 2026-10-12):** all **39/39** incoming LEA-shaped byte patterns matched again, with zero pattern rejects, and **154,191** PE `.pdata` unwind ranges were indexed. Those references grouped into **24 candidate function ranges** (none dropped at the function-group stage). The three `game_time` sites belong to **two** unwind ranges: `0x00B9C970–0x00BBDB54` (two sites) and `0x0090EB40–0x00916EC9` (one). **No instruction boundaries, native playback cursor, function semantics or hook safety have been proved.** The initial `replay`/`seek` string lists remain truncated. **Probe 009C–009E completed on the owner's exact 0.6.3 EXE (offline static evidence, 2026-10-12):** With **Capstone 5.0.6**, all **39/39** sites from the 24 unwind ranges were decoded as RIP-relative `lea` instructions whose targets matched the 009A/009B labels in a **linear sweep from their unwind starts**. No sites were unreachable to the *linear decoder*. **17** ranges had one or more **undecoded `E8`-shaped possible caller sites**; these remain hypotheses until proper caller instruction-boundary verification.

This is an improvement from raw byte matching, but **still not a validated playback-clock function or reliable runtime event source**. Several apparent `replay` and `game_time` references sit near generic text assembly/lookups; one `playback` reference is next to a potential unreachable/error handler ending in `ud2`. These are **static semantic hypotheses**, not confirmed identities. A 009F–009H batch is **source-ready, not yet physically run** to test approximate CFG entry reachability, decoded true `call` sites and bounded privacy-safe string context. A true visible playback tick would additionally require live pause/speed/rewind correlation and match-lifetime checks.

**Practical lesson for other mods:** use exact PE build fingerprints and bounded static-reference inventories to prioritize disassembly, but do not confuse symbol substrings, raw x86 byte patterns or unwind ranges with semantic gameplay/replay ownership. Avoid transplanting Harbinger's older `match_view+0x250` clock hypothesis, which failed runtime testing on a different version. Originating private Berserker reports: `docs/PROBE-009A-FINDINGS.md`, `docs/PROBE-009B-FINDINGS.md`, `docs/PROBE-009CDE-FINDINGS.md` and `docs/PROBE-009FGH-BATCH-RUNBOOK.md`. No original binaries, raw logs or private links are reproduced here.

## Watcher versus authority

Creep Chaos Probe 002 physically revalidated watched ClientMatchView Candidate A on its exact 0.6.3 build, but explicitly does **not** treat it as the authoritative simulation mutation surface. The stable `StableMatchHook` handles deterministic game-rule mutations; a watched-client/native hook is for observation or presentation. The engine can maintain more than one simulation context.

## Practical consequences

- Keep simulation tick, presentation clock, wall clock, scene epoch, and instance identity as **separate fields**.
- Replay rewind must not replay irreversible persistent career mutations, simply because the visible clock moved backward.
- For audio, investigate frame-recorded sound events; do not trigger client sound directly from a presimulation callback.
- For multiplayer, first prove vanilla peer state equivalence before injecting externally synchronized inputs.

## Not yet proved

These observations do **not** disclose a sample-accurate presentation clock, unique cross-match ID, general determinism of repeated fresh matches, or the exact native chat event queue. Do not infer those capabilities from a few matched timestamps.
