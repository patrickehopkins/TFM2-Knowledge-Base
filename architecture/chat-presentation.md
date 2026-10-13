# Native chat UI ownership and refresh behavior

## 0.6.3: one-shot custom chat child disappears

**Status: runtime verified (appearance in the SDK UI tree and disappearance); cause is a hypothesis.**

- **Game:** Teamfight Manager 2 **v0.6.3**, original EXE SHA-256 `f21cf691799a83d9afa0ccae3e2b95862f5780446a501ee97860b91b752dbe2f` (PE timestamp `0x6AC5C567`, image size `0x052D6000`, from independently recorded original-build fingerprint).
- **Environment:** stable host/SDK **ABI 9**, Flame Simulator observation probe **0.3.2**, physically run on Windows **2026-10-13**.
- **Method:** the client presentation probe created a uniquely named child under the live UI selector `ingame.chat_list` using stable `ui_spawn_source`, then `ui_spawn_template` with `asset/base/ui/layout/ingame_component/chat`, then `ui_set_text` on its own `chat.text` child. It never edited native sibling rows or the game's backing chat data. Passive SDK UI polling was approximately every 250 ms.
- **Observed:** source creation, template load and text write succeeded. The first subsequent ordinary UI sample read the owned subtree and synthetic text. The following ordinary UI sample found its parent with **zero children** and the owned subtree absent. The elapsed interval from creation to first observed absence was at most **257.8 ms**. A separate half-second lifecycle poll logged disappearance **505.7 ms** after creation: that is the delayed detection event, **not** the row's lifetime.
- **Other negative:** the probe's explicit client-side read of `RecordKindV1::MatchReplay` found **zero IDs in that test context**. Do not generalize that negative result to other saves/scenes or claim saved replays contain no chat/timing data.
- **Capture quality:** complete F9 footer, 2,056 sequential captured events and zero reported queue/event drops. A visible-clock rewind was also observed, but it occurred **after** the temporary node had already vanished and does **not** test its survival across rewind.

**Consequence (supported for this exact build and setup):** successful generic SDK template spawning inside the native chat list does **not** establish a persistent chat insertion route. Testing appearance in the SDK UI tree is not equivalent to proving the widget was actually painted onscreen; no screenshot or rendered-frame ownership trace was captured. The node's initial measured rect was zero before layout.

### Why might the child disappear?

**Hypothesis / static cross-version support, not a 0.6.3 causal proof:** an earlier disassembly of a distinct **0.6.2 executable** found a path that clears/repopulates the native `chat_list` children. The quick loss in the later 0.6.3 game is consistent with native chat-list rebuilding. No 0.6.3 hook identified the actual remover, and no execution frequency of the earlier native routine has been established. Do **not** claim an every-frame refresh or transplant 0.6.2 native offsets to 0.6.3.

### Practical research implication

Prefer discovering the **native chat event/dispatch ownership** or using an **independently owned, replay-aware presentation UI**, rather than assuming a one-shot custom node below `chat_list` will survive. The latter alternative still requires lifecycle, timing and visual validation. Repeated automatic re-spawning might mask a real ownership problem and has not been validated.

**Probe-design lesson:** these results were captured by ordinary, bounded passive UI polling. Hand-timed markers were **not required** to establish create/visible/disappeared order; optional phase markers should not be imposed as a user-workflow gate without a specific timing question.

**Source:** Flame Simulator probe 0.3.2, project report `docs/CHAT-0.3.2-FINDINGS.md` and verification `verification/0.3.2.json` (originating repository private). No raw files or local identifiers reproduced here. The stable SDK methods are described in the [official stable API reference](https://github.com/teamsamoyed/TeamfightManager2Mod/blob/main/docs/stable-api-reference.md).

**Still open:** persistent native event injection, whether the native list refresh actually caused deletion, reliable replay-time association, visible rendering of an owned chat row, and any corresponding multiplayer behavior.
