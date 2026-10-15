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

**Follow-up v0.6.3 result (physical Flame 0.3.3, 2026-10-13):** a native chat template instantiated in a uniquely owned sibling **under `ingame`, outside `ingame.chat_list`** remained readable and visible through 60 seconds of updates, with an independent screenshot proving synthetic chat text rendered on screen. A plain label sibling also survived 60 seconds but has no conclusive screenshot proof of painted text. This is SDK presentation ownership evidence, **not** native chat event/dispatch or replay-clock ownership. See [chat presentation](../architecture/chat-presentation.md).

**Physical 0.6.3 text/portrait update result (Flame 0.3.4, 2026-10-13):** `ui_set_text` successfully replaced a synthetic message twice on the **same separately owned native chat-template UI subtree**, with readback verifying both writes. The second markup string `<#ffa64dff>Flame Probe:<> alternate-color test` was visually confirmed in a screenshot to paint an orange speaker name. The template already contained `chat.icon_slot.icon`; `ui_set_champion_icon` rendered a small portrait for SDK champion `fighter`. These writes did not create native chat-history records, and the synthetic row remained positioned above the ordinary chat feed. See [version-specific evidence and limitations](../architecture/chat-presentation.md).

## 0.6.4 official stable API expansion (contract-supported; no gameplay verification)

The uploaded 0.6.4 SDK announces **ABI 10** and appends entity kind classification, champion-only cooldown/charge reads and cooldown reductions, per-caster/target AI action gates, dynamic range, unit-kill passives, draft position override/lineup IDs, server AutoPatch settings, and extra match-replay athlete statistics. Host-side passive match-view frames and zero-charge normalization also affect already-compiled stable mods, per developer documentation. **None of these creates minion-owned extra native skills, a precise presentation clock, direct native chat dispatch, or externally authoritative multiplayer input.** The 0.6.3 runtime outcomes on this page remain build-specific. See [the versioned ABI audit, exact executable fingerprint and per-mod tests](../game-versions/0.6.4-sdk-impact.md).

**Updated native relocation status (2026-10-14):** the new 0.6.4 [shared native profile](../game-versions/0.6.4-native-relocation.md) includes independently matched Candidate A/B/C simulation job entries, Creep Chaos resource and animation resolvers, and a read-only exact-file verifier. These are **static** checks of the original 0.6.4 game image, *not physical gameplay passes*. Projects should migrate against these profiles rather than request the same uploaded executable again for these already-mapped entry points.

## Installed SDK crate metadata versus research archive contract — 0.6.4 (2026-10-14)

**Evidence: owner-run installer failure + source inspection; corrected installer runtime PENDING.** Berserker Probe 019 / v0.0.15 successfully matched the **exact 0.6.4** game SHA-256, PE timestamp and image size. Its next guard checked the existence of both `mod-sdk-stable/base_version.txt` and `mod-sdk-stable/contract/abi_v1.txt` and stopped with a combined "missing" error **before refreshing the SDK, compiling or installing**. Because the error combined two paths, this single log **does not identify which path was absent**. The uploaded research archive contained the ABI contract; that alone is not evidence the Steam-installed SDK contains the contract at the same path.

**Source-supported correction (not yet physically rerun):** Build tools in the independently maintained Flame and Creep Chaos mods access the installed Rust crate at `mod-sdk-stable/mod-api-stable`; Flame's builder uses `mod-sdk-stable/base_version.txt` and parses `pub const ABI_LEVEL: u32 = ...;` in `mod-api-stable/src/lib.rs`. Berserker's corrected read-only installer gate now checks the version file, crate `Cargo.toml` and `src/lib.rs`, and requires exactly game **0.6.4 / SDK ABI 10**. It no longer treats `contract/abi_v1.txt` as a required installed-game file. Source identity/ABI checks still fail closed on missing or mismatched metadata.

**General lesson:** Differentiate an original SDK research ZIP's contract tree from a distributed game's Rust crate tree. Do not report "bad SDK" merely because an archive-only path is absent; validate installed version and ABI from the actual source crate without weakening the expected values. This correction is **not** a successful SDK ABI read, Windows build, or runtime hook test until rerun.

Origin: Berserker `docs/PROBE-019-064-MIGRATION-RUNBOOK.md` and `scripts/install-probe.ps1`; Flame `scripts/build-from-source.ps1`; Creep Chaos `scripts/bootstrap-sdk.ps1` (project source references, no raw logs or local user paths republished).


## Champion data, animation tags and client UI for sound-pack tooling — SDK documentation (2026-10-15)

**Classification: official SDK/documentation evidence, NOT a 0.6.4 runtime test.** The developer's [data-champion guide](https://github.com/teamsamoyed/TeamfightManager2Mod/blob/main/docs/data-champion.md) and [stable API reference](https://github.com/teamsamoyed/TeamfightManager2Mod/blob/main/docs/stable-api-reference.md) describe complementary champion metadata and client presentation capabilities that could be useful to independent champion sound packs.

- **Data-champion IDs/actions:** `.data_champion` files declare an exact, save-referenced champion `id`; reworks can preserve the base ID. Action definitions use slots `attack`, `skill`, `skill2`, `ult`, with `action_name` denoting a renderer animation tag. Displayed names and ability descriptions are not reliable filesystem or canonical identity keys. The schema includes `sprite`, `anim_prefix`, `skill_icon` and `skill_icons`; animated tags can be different from slot names.
- **Native champions:** `StableChampion::skill_icon(index)` and `StableAction::action_name()` are documented registration-time surfaces. Their existence does **not** establish a stable client function to enumerate the full installed champion registry or query every effective definition after all mods are loaded.
- **Client UI:** stable client documentation includes `ui_spawn_source`, `ui_spawn_template`, `ui_set_champion_icon`, click/path-event handlers and basic runners including `animation`, `dropdown`, `tree_view`, `image`, and `button`. **The presence of an animation runner does not prove that a mod can instantiate a live champion renderer in an arbitrary preview UI, nor trigger an idle/cast animation on demand.** Separate UI and renderer experiments are necessary.
- **Runtime simulation enumeration limit:** `StableSim::champion_count` and `champion_id_at` return **champion entity IDs in a simulation**, not the installed catalogue's champion definition IDs. Enumerating these is not a complete roster-discovery method.
- **Sound handle limit:** `StableClient::play_sound(path, volume)` is documented without a returned cancellable per-playback handle; separately owned cancellable WinMM voices from the Berserker probes should not be treated as native SDK sound handles. File-dialog and user-folder-open functions are **not established** by the cited client API.

**Generalizable design implication (hypothesis, not implementation):** a universal sound pack can use exact champion IDs plus stable *slot* keys, while testing installed-catalog discovery, present-time skill-cast events and renderer previews independently. Preserve current mod files while experimenting; treat user-imported audio outside managed mod folders as an explicit, user-owned storage choice with clear deletion guidance. This is not a claim that arbitrary custom champion packs have been tested.

**Version and limits:** reviewed against the developer's stable API documentation and this knowledge base's **TFM2 0.6.4 / ABI10** active baseline on **2026-10-15**; no new executable scans, host integration tests, external-mod compatibility tests or GUI demonstrations occurred in this review. This entry is an independent reading of public SDK documentation, not a reproduction or publication of a collaborator's private implementation. The originating project's detailed design proposal remains in its own private repository.
