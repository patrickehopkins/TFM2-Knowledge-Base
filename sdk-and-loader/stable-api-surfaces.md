# Stable mod SDK: observed integration boundaries

This is a research inventory, not an exhaustive or official API definition. For authoritative API signatures see the [TFM2 stable API reference](https://github.com/teamsamoyed/TeamfightManager2Mod/blob/main/docs/stable-api-reference.md). Source: Creep Chaos Probe 002 (Creep Chaos source; private repository), Flame 0.6.3 probe (Flame Simulator source; private repository), Berserker frame-event plan (Berserker Keeps Yelling source; private repository).

| Surface | Evidence-based role |
| --- | --- |
| `StableMatchHook` | Deterministic simulation mutation surface; do not substitute a watched-client-only detour for authoritative rules |
| `StableServerExtension` + supported GameSetting writes | Configuration applied to later matches, including exposed wave/balance settings |
| `StableSim::seed()` | Synchronized match seed observed in Creep Chaos v0.6.3 |
| `StablePlayerAi::think()` | Can be called during ahead-of-display simulations; not a presentation-frame callback |
| Stable UI state tree and paths | Exposes observed match clock/chat/viewport selectors with bounded polling, but not a sample-accurate event clock |
| `StableSim::play_sfx(...)` | Documented frame-event candidate; actual playback behavior requires physical test |

Flame Probe 0.3.1 was physically run on 0.6.3 with host ABI 9 / installed SDK ABI 9 and recognized UI selector candidates. It recorded positive `tick_per_second=60` and `visible_distance=130000`. This is a **specific test outcome**, not a promise that all SDK behaviors are stable across releases.

For native instrumentation: verify each executable's hash/PE identity and prologue; never assume that stable SDK ABI implies stable native layout.

**Important v0.6.3 native chat limitation (physical Flame 0.3.2 probe, 2026-10-13):** stable SDK `ui_spawn_source` / `ui_spawn_template` / `ui_set_text` created a readable probe-owned child under `ingame.chat_list`, but it was absent by the next ordinary UI poll, under 258 ms after creation. Generic UI spawning is not a persistent native chat-dispatch API. The cause of removal and onscreen painting remain unverified. See [chat presentation finding](../architecture/chat-presentation.md).
