# Native chat UI ownership and refresh behavior

## 0.6.3: writing colored chat text and champion portraits

**Status: runtime verified for text updates, orange speaker markup and portrait painting; 2026-10-13.** Source: Flame Simulator **Probe 0.3.4**, physically run against the original TFM2 **v0.6.3** executable SHA-256 `f21cf691799a83d9afa0ccae3e2b95862f5780446a501ee97860b91b752dbe2f`, stable SDK/host **ABI 9**, Windows build. Owning project documentation: `docs/CHAT-0.3.4-FINDINGS.md` and `verification/0.3.4.json`.

**Method:** an independently owned `ingame` sibling (not a native `chat_list` child) used the game's `asset/base/ui/layout/ingame_component/chat` template. On its `chat.text` label, `ui_set_text` changed the diagnostic text twice without rebuilding the node, after approximately **5.04** and **10.08 seconds of diagnostic wall-clock time**. The first write used the native-readback speaker-markup structure with one synthetic color; the second wrote `<#ffa64dff>Flame Probe:<> alternate-color test`. Its existing `chat.icon_slot.icon` node accepted `ui_set_champion_icon` for SDK champion `fighter` at 24 × 24, scale 2.0. No extra image child was required.

**Results:** both writes returned successful and the text was read back intact. A user screenshot independently confirms the **second markup rendered an orange speaker name** and **a champion portrait painted beside it**. The first markup had successful write/readback, but **no screenshot proves its exact painted color**. The plain-label comparison node remained readable/visible through the API, but no screenshot unambiguously demonstrated its painted pixels.

The two owned sibling nodes persisted for roughly **30.25 seconds** through native `chat_list` population changes (0–3 child rows), then were intentionally removed. Automatic capture closed with **2,077 unique sequenced IDs, 0..2076**, zero missing/duplicate IDs and zero reported queue drops; concurrent events did not always appear in numerical file order.

**Important limitation / negative result:** the custom styled message was visibly positioned **above the normal chat feed**, not within the native chat history or scrolling arrangement. Its text-update timing was wall-clock, **not synchronized playback time**. Neither this result nor the portrait appearance establishes native chat dispatch, real speaker attribution, replay seeking, exact frame/time binding, hiding with UI, multi-resolution placement or lifetime inside the game's history. Do not promote a successful sibling UI overlay into proof of native chat event insertion.

**Reusable finding:** when working with independently owned noninteractive game UI, a native template's existing text and portrait child nodes may be updated through stable client SDK methods without directly modifying native chat entries, but visual proof and layout integration must be tested separately. Treat image and markup effects as version-specific to this tested build.

---

## 0.6.3: independently owned chat-template sibling persists

**Status: runtime verified, including onscreen rendering in one screenshot.** Flame Simulator Probe **0.3.3**, Windows physical game, **2026-10-13**, TFM2 **0.6.3**, host/SDK **ABI 9**. Original executable SHA-256 `f21cf691799a83d9afa0ccae3e2b95862f5780446a501ee97860b91b752dbe2f` (PE timestamp `0x6AC5C567`, image size `0x052D6000`). Originating evidence: `docs/CHAT-0.3.3-FINDINGS.md`, `verification/0.3.3.json` in Flame Simulator.

**Method:** using the stable client UI API, the observer created two uniquely owned **siblings of** `ingame.chat_list` beneath the visible `ingame` parent. One used an `empty` container + `ui_spawn_template("asset/base/ui/layout/ingame_component/chat")` + `ui_set_text` on its child `chat.text`; the other was a basic `label` with distinct synthetic text. No native chat-list child was inserted, and no chat storage, player inputs or simulation/AI were modified. Start, sampling and cleanup were automatic; no hand-timed markers.

**Positive observations:** both elements successfully spawned, held their original text and reported visible with positive **500 × 30** UI rectangles after layout. They survived all **120** half-second polling cycles across approximately **60.13 seconds** (25 sparse/transition observations in the log, each with both children present). In that window the native `chat_list` varied among **0–3** children; the independent siblings persisted. Both were intentionally removed successfully when the bounded probe ended. A separate user screenshot visibly shows the *native-template sibling's synthetic text alongside normal game chat*, proving it was painted in at least one frame. The plain label was readable and `ui_visible=true`, but its onscreen painting is **not** independently established from that screenshot.

**Native row structure observed (same 0.6.3 physical capture):** `ingame.chat_list.chat` is an `empty` row with a `chat.text` **label** and `chat.icon_slot` **color** container housing an `icon` **image** node. Five unique sampled native `ui_text` values shared the inline color markup shape `<#5873ffff>speaker:<> message` (synthetic example; original user chat names/content not republished). **Verified:** that is the native label readback format for these sampled rows. **Unverified:** whether writing the same markup from a mod produces equivalent paint/color, whether other channels/colors differ, and whether adding a champion portrait via stable SDK can match native icon layout.

**Negative/control and limits:** Contrast with Probe 0.3.2 below, whose diagnostic child inserted directly **inside** `chat_list` vanished within 258 ms. The difference supports a UI-ownership boundary, **not** the identity of an underlying native refresh method. A sibling surface remains **outside native chat history, ordering, timestamps, speaker attribution and automatic replay handling**. Whether custom elements hide with chat, scale across resolutions, and correctly pause/seek at replay time remains untested. Stable UI polling is not a sample-accurate presentation clock. Results apply to this exact game build/SDK and must be revalidated on future versions.

**Reusable technique:** for noninteractive custom presentation alongside game-owned dynamic lists, consider adding a uniquely owned child to a more stable common parent **outside** the list rather than attaching it to a list rebuilt by native logic. Guard collisions, track ownership, bound polling, clean up on lifetime/scene exit, and separately verify painted output; readable UI nodes alone are insufficient.

**Evidence quality:** auto-completed 2,229 unique sequenced captured events with zero reported queue/event drops. Original screenshot, raw ZIP/JSONL and local identifiers remain private; no game assets are redistributed. This independently verified presentation method can be investigated by other UI mods, but is **not proof of native chat event injection**.

---

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
