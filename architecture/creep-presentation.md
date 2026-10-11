# Native creeps with champion presentation — 0.6.3

**Status: RUNTIME VERIFIED** for original melee Knight presentation in Probe 008 and **both melee Knight / ranged Archer role-separated presentation in Probe 011** (Creep Chaos source; private repository), on the [fingerprinted 0.6.3 build](../game-versions/compatibility.md).

Native `melee_minion` entities were displayed with Knight champion artwork/animations **without converting their underlying simulation identity into champions**. Runtime observer still reported `champion=false`, `minion=true`. Lane movement and combat were observed in screenshots; native wave lifecycle and creep identity stayed intact.

## Why an initial attempt turned invisible

Probe 006 physically changed the world base resource to Knight, but the renderer expected minion-specific composite animation keys. The native minion resolver used names such as `melee_blue_idle`, `melee_red_attack`; the Knight resource expected base actions such as `idle`, `attack`, `run`, `dead`. Without remapping, the art became invisible.

Probe 008 paired two hooks: world-resource resolver RVA `0x0230AB20` and animation-key resolver RVA `0x02313A30` for the exact 0.6.3 fingerprint. The bridge rewrote composite names to base actions. The paired hook installation and actual substitutions were observed in runtime logs; screenshots showed animated Knight-bodied creeps.

> **Later research, separate status:** original kind-3 minion attacks and original kind-15 champion Knight W have statically mapped access to the same native ready-effect dispatcher; see [native action/effect research](native-action-effects.md) for the exact 0.6.3 evidence and corrected W state-5 progress path. **No champion ability cast by a native minion has been verified.**

## 2026-10-11 update — runtime verified melee/ranged role-specific champion presentation (Probe 011)

**RUNTIME VERIFIED:** Teamfight Manager 2 **0.6.3 Win64**, original EXE SHA-256 `f21cf691799a83d9afa0ccae3e2b95862f5780446a501ee97860b91b752dbe2f`, PE timestamp `0x6AC5C567`, SizeOfImage `0x052D6000`; original stable SDK **ABI 9**, Creep Chaos diagnostic mod **v0.0.19**. User physically ran one watched 5v5 match and supplied a main-menu screenshot, three match screenshots and a diagnostic log. **This supersedes the former ranged-minion-unverified qualification** for role-specific *presentation only*.

The **same two guarded native client-only detours**—world-resource resolver RVA **`0x0230AB20`** and animation-key resolver RVA **`0x02313A30`**—now render **original native `melee_minion` as Knight** and **native `range_minion` as Archer**, without converting either class to a champion in simulation. The native action namespace bridge adapts `melee_blue/red_<action>` **and** `range_blue/red_<action>` to champion-style `<action>`; the runtime sample included `attack`, `dead`, `idle`, `run` for both colors/classes. Native log counters recorded **189,789 Knight and 120,180 Archer resource rewrites**, and **124,158 melee and 75,059 ranged animation-key rewrites**, in the first observation. These are **cumulative resolver invocations, not distinct spawned entity counts**; no invalid-action or string-capacity failure was logged in sampled animation telemetry.

A watched match confirmed normal native **2 melee + 1 ranged per team per lane** slot timing (melee ticks **40/70**, ranged **100**), with `champion=false`, `minion=true` for both and ordinary first-wave melee **400 HP / 10 attack** versus ranged **250 HP / 15 attack**, followed by native growth. Thus **presentation per original creep role** is verified. **Individual wave-slot identity, deterministic curated per-slot champion pool selection, 3+3 waves, native champion skill casts, remote/replay/gameplay authority and jungle conversion remain unverified.**

### Main-menu background is useful for quick visual smoke tests, but cannot substitute for match authority

**RUNTIME observation:** In the main-menu background screenshot, champion-bodied minions were already visible before a watched match was manually started. At the first explicit watched `MATCH ... first_tick=1` report, previously installed native hooks had accumulated **502,880** world-resource and **368,676** animation-key calls, plus **86,603** native action-start routine calls (including **534** Knight W classifications). These values were collected **before or outside the first watched-match callback**; they show substantial activity but are **not independently tagged as menu simulation or specific authoritative jobs**. Some may belong to accelerated precomputation, loading or other contexts, and do **not** establish Knight W usage by a minion.

**Practical workflow:** For purely client visual changes, first view the main-menu background and compare scene rendering and sampled resource/animation rewrite counters. For entity-to-view identity, deterministic match-seed and mirrored slot selection, AI, skills, rewards, authoritative copies or replay consistency, **still inspect an appropriate controlled match**. If a new experiment needs positive menu-simulation attribution, add an explicit scene-tagged counter snapshot across menu updates instead of inferring identity from global native hook counts. No need to replay every earlier EH lifetime probe.

## Important boundary

This demonstrates **visual resource compatibility and a deterministic per-minion proof-state cooldown**. It does *not* prove native creeps can execute Knight's full built-in champion skill pipeline, target champions under all ability rules, or support generalized **per-slot** hero selection, 3+3 wave expansion, siege/jungle variants, or native skill use. The tested counter `post_cc_visible` remained zero, so custom CC persistence was **not** established by this probe.

## Additional validated observation

Creep Chaos Probe 002 (Creep Chaos source; private repository) observed default 5v5 per-lane wave composition of two melee and one ranged unit. In that run, first-slot wave starts were 780 ticks apart despite `tick_per_wave=660`. Do not equate a configured wave-body interval with full spawn-to-spawn cadence without measurement.
