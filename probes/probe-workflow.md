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
