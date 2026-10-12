# Safe, reproducible probe workflow

A good TFM2 probe answers one question with minimal game-changing behavior, and records why alternative interpretations are ruled out.

## Procedure

1. Identify a specific claim and explicit **pass / fail / inconclusive** criteria.
2. Capture game version, exe SHA-256, timestamp/image size if native, SDK/ABI, loader, mod list, and probe revision.
3. Start with observation-only and bounded capture. Separate simulation contexts, visible scene time, and wall time.
4. Preflight native targets against exact build identity and expected signature; **fail closed**. If using paired hooks, enable mutation only after both pass.
5. Use disposable saves and reversible installations for potentially destructive tests.
6. Run focused physical test cases including negative and teardown cases. A signature match or successful cargo build is not a physical test.
7. Preserve concise sanitized raw evidence in the owning repo. Record observed log counts, drops, scene epochs, event correlation, and limitations.
8. Publish a reusable conclusion here, clearly distinguishing verification, static deductions and hypotheses.

## Good examples

- **Creep Chaos Probe 007:** wrong animation-key resolver RVA; expected failure prevented mutation. The failed preflight did not test animation semantics.
- **Creep Chaos Probe 008:** paired-hook correction produced runtime events plus screenshots of Knight-bodied creep units; clearly excludes proving native champion ability execution.
- **Flame replay capture:** records dropped-event counts, polling limits, true rewind points and the distinction between 'first readable' and exact spawn time.
- **Berserker Probe 002:** explicitly refuses to turn an entity disappearance into a claimed death callback.

## Shared hook caution

Two separate mods may each pass isolated native-hook tests yet conflict when loaded together. Treat common detour sites as compatibility hazards until joint tests show otherwise.

## Static native-code census: completeness before sampling

**Status: source-level tooling review and synthetic self-test, NOT a game-executable or runtime verification.** Creep Chaos **Probe 010L-2**, 2026-10-09, investigated an offline action-slot scanner intended for the exact **TFM2 0.6.3 Win64** original build (SHA-256 `f21cf691799a83d9afa0ccae3e2b95862f5780446a501ee97860b91b752dbe2f`, PE timestamp `0x6AC5C567`, SizeOfImage `0x052D6000`). No new original game binary census was completed in that probe.

A reviewed initial scanning design collected memory-field matches from `.pdata`-covered functions and **stopped as soon as a capped output array filled**. When common state fields are included, this can hide rarer, later-address candidate action-slot writers. This is a **tool completeness risk**, not a proven absence or presence of any native setter. The revised method:

1. Verify the entire exact executable fingerprint and PE properties **before** interpreting instructions. Reject mismatches.
2. Decode instruction boundaries rather than searching raw byte substrings. Keep ordinary reads, possible writes, and `lea` address calculations distinct when operand-access metadata permits.
3. Finish the bounded function census first; **apply output sampling limits only after** deterministic priority ranking. Report total candidates, sampled candidates, scope and truncation explicitly.
4. Prioritize candidate object/action writes and known constructor/clone/refresh edges over ubiquitous state reads. Scores rank **review work**, not evidentiary confidence.
5. For every candidate, resolve the base pointer and caller provenance, native entity kind, object lifetime and simulation-copy ownership before calling it a legitimate live setter. A field displacement such as `+0x588` on an unrelated object is only a coincidence.
6. Treat `.pdata`-covered code as **nonexhaustive**: indirect calls, inlined paths, code outside the scanned ranges and whole-record copies can evade the census.

**Limits:** The pure synthetic scanner scoring/fingerprint-gate tests were run on a locally equivalent implementation; the original 0.6.3 game executable and full Capstone scan were unavailable in this session. Therefore this section records a **verified code-design correction and untested game-scan plan**, not a found minion skill installer. The full project-specific scan plan belongs to Creep Chaos `docs/PROBE-010L-ACTION-INSTALLATION-RECON.md` (private source). Other TFM2 mods can reuse the review principle without adopting its exact offsets.

### Probe 010L-3 bounded scan: positive controls and access-metadata correction

**Evidence: user-executed offline scan report, static/report-level verification only; no in-game observation.** In Creep Chaos Probe 010L-3 (2026-10-09), a SHA-guarded read-only scanner reported **154,191** `.pdata` functions, **13,747,032** decoded instructions and **20,412** candidate references/call edges from original TFM2 0.6.3 Win64 (reported SHA-256 `f21cf691799a83d9afa0ccae3e2b95862f5780446a501ee97860b91b752dbe2f`; timestamp `0x6AC5C567`, image size `0x052D6000`). The executable itself was **not independently rescanned** in the reviewing session. The scanner recovered **previously mapped** champion constructor, entity-clone, action-cache and Knight W consumer reference sites: this was a *positive-control sensitivity check*, not discovery of a kind-3 installer.

Two negative findings apply broadly to static instrumentation:

- **Similar displacement does not imply similar object:** among reported matches, some candidate `+0x590` vtable writes actually stored tiny integer constants (e.g., 2), and hundreds used large offsets from stack-frame register `rbp`. Without base-pointer provenance and value/type consistency, a memory reference should **not** be promoted to an entity-slot writer.
- **Disassembler access flags may be wrong:** the tool labeled a memory-destination `movups [rbp+0x590], xmm0` as a read. The scanner was corrected to recognize explicit memory-destination move stores, retaining the misclassification as a documented negative result. Re-run the real scan before claiming corrected category counts.

The 5,000-record output cap also omitted **102** detected direct calls/jumps because those lower-priority entries were displaced by field references. Subsequent tooling retains direct-call matches separately even when the main report is truncated. **No live setter, minion-origin native W cast, or per-minion ability cooldown has been proven.** Original project details remain in Creep Chaos `docs/PROBE-010L3-CENSUS-FINDINGS.md`; no private logs or executable bytes are published here.

### Probe 010L-5: identical offsets can mean link pointers, not action vtables

**STATIC OFFLINE USER-EXECUTED REPORT, 2026-10-10, original TFM2 0.6.3 Win64.** Creep Chaos Probe 010L-5 followed four additional candidate `+0x588/+0x590` pointer writers at function RVAs `0x0031AE80`, `0x00C2BB40`, `0x0179F300`, and `0x01CD0000`. Each allocates/manipulates **0x5A0-byte list nodes**, explicitly sets `[node+0x588]=node` and `[node+0x590]=node`, and updates reciprocal neighbor links; another traverses nodes via `[node+0x590]`. These bytes **do not represent the native entity's action slot C**: the full action-bearing entity record has a separate `0x6B8` size, and an action vtable is not a self/neighbor link. A synthetic/JSON verifier checks 53 exact instruction anchors in the uploaded bounded read-only disassembly report; the original EXE bytes were not independently rescanned in the review session.

**Classification:** all four were **REJECTED AS SKILL-INSTALLER CANDIDATES**; their unrelated game subsystem is not assigned a speculative name. This is a generalizable negative test: before treating matching offsets as a stable ABI, identify **allocation size, base pointer origin, self-referential/sentinel writes, reciprocal pointer maintenance, payload location and actual type-specific operations**. A full address/operand match without provenance is insufficient. The result does **not** prove that no other native live action setter exists. Originating detailed finding: Creep Chaos `docs/PROBE-010L5-LINKED-NODE-FALSE-POSITIVES.md`. No disassembly dump or private game assets are included here.


### Probe 013P — bound emitted detail, not all legitimate call instructions

**USER-OBSERVED NEGATIVE; SOURCE/CI FIX AND SUBSEQUENT ORIGINAL-EXECUTABLE STATIC USER RERUN VERIFIED (2026-10-12).** Creep Chaos Probe 013P (original TFM2 **0.6.3 Win64**, expected executable SHA-256 `f21cf691799a83d9afa0ccae3e2b95862f5780446a501ee97860b91b752dbe2f`, PE timestamp `0x6AC5C567`, SizeOfImage `0x052D6000`) decoded a bounded original renderer-owner function and then **aborted** because its direct `call`-instruction count exceeded an arbitrary **250-call** budget. The subsequent report verifier found no JSON because the scanner correctly wrote nothing after the exception. This failure was **not** a game runtime malfunction, a malformed record, or proof of a mismatched executable.

**Correction (source, synthetic CI, and subsequent user-run exact-original static output):** Retain strict original binary/hash, function boundary and **30,000 decoded instruction** guards; count every recognized direct call in that already bounded function, but only retain calls near candidate record operations and cap detailed original instruction context emission to **35**, with a separate **total-nearby count and truncation flag**. An independent synthetic case with **320 calls, 40 nearby, 35 emitted** tests the former failure condition. The result schema preserves full counts without copying all proprietary instruction context, and the verifier now reports an explanatory missing-output error when the original scan has not completed.

**Reusable lesson:** Do not treat a modest *total-occurrences* cap in a successfully bounded executable function as a safety requirement. Cap expensive work, allocation, instruction decoding and reported samples; track complete bounded census counts and truncation separately. Distinguish a **fail-closed safety guard** from an **arbitrary analytical budget**. The user subsequently reran original 0.6.3 Probe 013P successfully: the original bounded function contained **306 direct CALL instructions**, with **59** relevant-near and **35** detailed contexts emitted (truncated=true); no renderer ↔ simulation entity identity or ability capability follows. Origin: private Creep Chaos `docs/PROBE-013P-BATCHED-RETURN-RECORD-ORIGIN-RUNBOOK.md`.


### Probe 013Q — an address copied into a signature gate can itself be wrong

**USER-EXECUTED STATIC-PROBE NEGATIVE, corrected source/regression test AND USER ORIGINAL-EXE RERUN PASS (2026-10-12).** Creep Chaos Probe 013Q, prepared for exact-original **TFM2 0.6.3 Win64** (SHA-256 `f21cf691799a83d9afa0ccae3e2b95862f5780446a501ee97860b91b752dbe2f`, PE timestamp `0x6AC5C567`, SizeOfImage `0x052D6000`), rejected a supposedly known `CALL` at original RVA `0x0232266F` because its earlier user-verified source report located the target function's direct call at **`0x0232226F`**. The difference was a **probe-script transcription error**, not an executable mismatch or a crash. Both the scanner's old pure synthetic self-test and its old source-string checker passed because **the same wrong literal appeared in both**; neither was an independent verification against the real instruction-source evidence. The original scan stopped with a fail-closed `ValueError` and produced **no report**, so the next verifier's missing-file error was expected.

**Corrective pattern:** Cross-check strict original-site signatures against *independently established source observations* and put the **correct known callsite + callee target** in a separate positive control, with a negative test explicitly rejecting the mistaken original RVA. Preserve SHA/PE bounds and per-call instruction checks; never relax strict native signatures merely because one check fails. The source/regression correction was committed and **the user subsequently reran the original 0.6.3 static scan successfully**, verifying the formerly blocked callsite and producing a four-study private JSON. It decoded the same **5,554** original owner instructions, found **66** compiler-local firstword syntactic writers and **55** direct copy helper calls (23 with nearby explicit 0xE8 size). Examples match short **Game/UI** literal byte lengths, favoring a string-length interpretation, not a native stable entity ID. The complete report remains private; see `architecture/creep-presentation.md` for the scoped architectural result. This provides no new minion identity or ability-authority evidence, and the result does not generalize to **0.7.0 beta**. Origin: Creep Chaos Probe 013Q; exact project runbook and original disassembly remain private.


### Presentation-to-simulation ID correlation requires an independently validated shared clock — Probe 014A

**HISTORICAL WATCHED-LOG REANALYSIS + SOURCE/SYNTHETIC TESTS, NOT NEW GAME RUNTIME VERIFICATION (2026-10-12).** Creep Chaos Probe 014A audited three previously watched **original TFM2 0.6.3 Win64 / SDK ABI9** sessions. Related exact-original native executable source scans were pinned to SHA-256 `f21cf691799a83d9afa0ccae3e2b95862f5780446a501ee97860b91b752dbe2f` (PE timestamp `0x6AC5C567`, SizeOfImage `0x052D6000`). The offline log audit **did not rehash the executable or rerun the game**. All raw native logs and file paths remain private.

Across the three **separate** previous diagnostic sessions, logs contained **270** sampled primary-renderer coordinate-field lines, **132** first-seen anonymous client-view arrival lines, **350** watched SDK simulation-entity position lines, **12** SDK snapshot summaries and **3,024** simulation-side native creep spawn lines. Nonetheless, **zero** of the supported renderer field/arrival rows included a corresponding simulation tick or validated presentation timestamp; **zero** SDK simulation-entity rows included a transient view-token key; **zero** source records provided independent shared-clock evidence. These are *selected log-line counters*, **not** a count of simultaneous objects or proof of missing real-world entity correspondence. The separate sessions cannot be merged into a common frame.

A new standalone offline synthetic matcher includes explicitly untrusted clock and endpoint/team proof flags. It **rejects before matching** when timebases are unaligned or endpoint/team translation is unknown; it rejects large synthetic drift, nearest-neighbor ties between two same-role allied melee creeps, duplicate IDs, invalid coordinates, missing snapshots, frame rewind, gaps and transient pointer-token disappearance/reappearance. After two independent **synthetically aligned** frames it reports only **repeated geometry candidates**, **never authoritative client pointer ↔ native simulation `StableEntity::id()`**. Synthetic tolerance constants are **test-fixture choices**, not empirically validated game timing/radius parameters. No new DLL/hook, native process read, active game match, sprite selection or multiplayer claim results.

This is independently consistent with the cross-project [simulation/replay timing findings](../architecture/simulation-and-replay.md), where watched simulation can finish long before visible playback and a prior guessed client display-clock offset was rejected. The 014A audit did **not** newly verify a presentation clock; the runtime studies and the audit remain distinct evidence classes.

**Reusable negative:** an SDK entity ID and position sample plus a renderer view position from the same match do **not** justify matching them by nearest coordinates or log order. Client-replay callbacks and simulation ticks can be on different clocks, and same-team same-role creeps create genuine ambiguity. Before proposing a native stable-ID bridge, require independently demonstrated clock alignment and lifecycle keys, then repeated unique matches against all competitors and pointer recycling controls. The appropriate outcome with existing evidence is **UNALIGNED / INCONCLUSIVE**, not a fabricated ID. Origin: Creep Chaos private project `docs/PROBE-014A-HISTORICAL-LOG-AND-SYNTHETIC-FINDINGS.md`; full logs and analyzer implementation stay with the mod. No beta 0.7.0 inference.


### Clock-independent trajectory matching is only a candidate test — Probe 014B (2026-10-12)

**SOURCE/SYNTHETIC + WINDOWS METADATA CI VERIFIED; NO NEW IN-GAME RUNTIME TEST YET.** Creep Chaos v**0.0.28** (prepared for original **TFM2 0.6.3 Win64**, SDK ABI **9**, native EXE SHA-256 `f21cf691799a83d9afa0ccae3e2b95862f5780446a501ee97860b91b752dbe2f`, PE timestamp `0x6AC5C567`, SizeOfImage `0x052D6000`) added a bounded observation-only collection source. Its actual DLL load/game behavior is **PENDING**; the prior physical v0.0.27 tests remain separate. No new native hooks, unverified memory offsets, gameplay authority, champion abilities or per-unit sprite changes were introduced.

The project previously demonstrated that an SDK simulation tick is not a verified visible-playback timestamp, and original primary-renderer float positions at `view+0x17C` represent original lane-world coordinates at an observed **1:1,000 scale**. A new **pure synthetic** offline correlator therefore compares *directed whole-trajectory shapes resampled by cumulative path distance*, rather than guessing a simulation↔replay wall-clock offset. Its negative controls **reject** insufficient displacement/coverage, overlapping same-team two-melee paths, close second-best candidates, nonreciprocal view/sim matches, wrong side or role, reversed order, mismatched scene epochs, duplicate anonymous view tokens / SDK IDs and out-of-bounds inputs. Thresholds are **synthetic fixture parameters, not native-game calibration**. A positive result is expressly **CANDIDATE_TRAJECTORY_CONSISTENCY**, **not** a runtime stable-ID mapping.

The prepared runtime collector is instrumented only on the **previously validated** primary renderer callback using already-copied native world-coordinate floats and the existing qualified Candidate-A SDK `StableEntity::id()/pos()` simulation observer. It caps the original watched sample at **2,048 renderer callbacks**, **96 anonymous native view tokens**, **96 SDK simulated minion IDs**, **64 position samples per track**, and **4,096 total SDK position samples**. SDK simulation tick and renderer callback ordinal remain separate source-specific indices, never synchronized by assertion. One original physical watched-match test is **planned but not yet performed**; it may legitimately produce **AMBIGUOUS / INCONCLUSIVE** if vanilla melee trajectories cannot be uniquely distinguished. Even a promising geometry candidate would need separate lifecycle and authoritative-ID verification before use in artwork or skill authority. No multiplayer, jungle, expanded waves or beta 0.7.0 claims follow.

**Reusable methodology:** When presimulation and on-screen playback clocks are fundamentally different, whole-trajectory pattern comparison can be tested as a falsifiable *candidate* identity hypothesis without assuming synchronized timestamps. However, require same-role collision/ambiguity controls, scene/replay epoch separation and independent verification of actual data quality before assigning identities. Do not allow a synthetic pass to substitute for physical observation. Detailed code/test runbooks remain in the originating Creep Chaos project; raw game logs and original binary instruction contexts are not published.


### Windows Rust native-probe prerequisite: Cargo is not enough

**USER-OBSERVED BUILD-ENVIRONMENT NEGATIVE / SOURCE FIX (2026-10-12).** On a fresh Windows development machine, a TFM2 Rust mod targeting `x86_64-pc-windows-msvc` successfully compiled its Rust crates after Rustup installation but failed at the final native link step with **`link.exe not found`**. This is a host-toolchain dependency, not a game/probe-runtime failure and not a performance result.

For MSVC-targeted TFM2 Rust mods, install **both** Rust/Cargo and Visual Studio Build Tools with the **Desktop development with C++** workload (`Microsoft.VisualStudio.Workload.VCTools`), which includes the C++ build tools and Windows SDK components. Microsoft documents the VCTools workload ID and Build Tools product separately in [Visual Studio workload and component IDs](https://learn.microsoft.com/en-us/visualstudio/install/workload-and-component-ids?view=visualstudio) and [Build Tools workload/component IDs](https://learn.microsoft.com/en-us/visualstudio/install/workload-component-id-vs-build-tools?view=vs-2022). A project installer should fail early if Cargo or the MSVC linker environment is unavailable; if Build Tools are already installed, it can load the x64 Visual Studio developer environment through `vswhere.exe` / `VsDevCmd.bat` before invoking Cargo.

**Interpretation:** warnings from Rust source compilation are not the blocker when Cargo ultimately reports a missing MSVC linker. Do not classify that host setup failure as an in-game crash, mod incompatibility, or probe-performance regression. Origin: Creep Chaos v0.0.28 development setup; no raw machine paths or private logs published.

## Fresh-workspace probe batches: regenerate ignored intermediates

**USER-REPORTED WORKFLOW FAILURE; SOURCE-LEVEL CORRECTION, NOT YET WINDOWS-RUNTIME TESTED (2026-10-12).** Berserker Keeps Yelling's offline 009C–009E runner originally required a local `probe009b-replay-clock-functions.json` generated by the preceding test. After moving to a different Windows repository checkout, `git pull` succeeded but the runner stopped with **"Probe 009B JSON not found"**. The cause was **a deliberately Git-ignored intermediate artifact**, not a missing SDK or disassembler. This is a user-observed negative result about probe reproducibility.

**Portable workflow pattern:** Treat prior local JSON as a *cache*, not as a prerequisite for a fresh clone. The runner should reconstruct safe deterministic intermediate reports from original, locally available, version-fingerprinted inputs, run each stage's synthetic self-test, and fail closed on missing prerequisites, mismatched original game SHA-256/PE version or unexpected schema. Use an isolated local environment for optional disassembly dependencies and keep intermediate/decoded outputs ignored. An explicit override may accept a saved intermediate when its fingerprint matches the same executable.

In the Berserker project, `scripts/run-probe009cde-batch.ps1` now regenerates 009A and 009B automatically before 009C–009E when no explicit `-Prior` is supplied. **Source was committed and verified in GitHub; the revised runner has not yet been physically rerun on the user's new Windows workspace.** This is general probe engineering guidance, not a new observation about TFM2's replay-clock implementation.

