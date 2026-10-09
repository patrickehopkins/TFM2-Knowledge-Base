# Native creeps with champion presentation — 0.6.3

**Status: physically verified** in Creep Chaos Probe 008 (Creep Chaos source; private repository) on the [fingerprinted 0.6.3 build](../game-versions/compatibility.md).

Native `melee_minion` entities were displayed with Knight champion artwork/animations **without converting their underlying simulation identity into champions**. Runtime observer still reported `champion=false`, `minion=true`. Lane movement and combat were observed in screenshots; native wave lifecycle and creep identity stayed intact.

## Why an initial attempt turned invisible

Probe 006 physically changed the world base resource to Knight, but the renderer expected minion-specific composite animation keys. The native minion resolver used names such as `melee_blue_idle`, `melee_red_attack`; the Knight resource expected base actions such as `idle`, `attack`, `run`, `dead`. Without remapping, the art became invisible.

Probe 008 paired two hooks: world-resource resolver RVA `0x0230AB20` and animation-key resolver RVA `0x02313A30` for the exact 0.6.3 fingerprint. The bridge rewrote composite names to base actions. The paired hook installation and actual substitutions were observed in runtime logs; screenshots showed animated Knight-bodied creeps.

## Important boundary

This demonstrates **visual resource compatibility and a deterministic per-minion proof-state cooldown**. It does *not* prove native creeps can execute Knight's full built-in champion skill pipeline, target champions under all ability rules, or support generalized hero selection, scaling, ranged/siege/jungle variants. The tested counter `post_cc_visible` remained zero, so custom CC persistence was **not** established by this probe.

## Additional validated observation

Creep Chaos Probe 002 (Creep Chaos source; private repository) observed default 5v5 per-lane wave composition of two melee and one ranged unit. In that run, first-slot wave starts were 780 ticks apart despite `tick_per_wave=660`. Do not equate a configured wave-body interval with full spawn-to-spawn cadence without measurement.
