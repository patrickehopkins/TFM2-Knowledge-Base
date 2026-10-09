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
