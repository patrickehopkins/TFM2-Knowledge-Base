# Native detour safety and fail-closed checks

**Status: a verified crash postmortem, plus successful version-gated hooks.** See [Harbinger incident](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/native-hook-crash-postmortem.md), Creep Chaos Probe 007 (Creep Chaos source; private repository) and Probe 008 (Creep Chaos source; private repository).

## A relocated prologue is not automatically detour-safe

Harbinger's historical v0.5.8 loop probe patched a 16-byte region at RVA `0x018147F4`. An existing conditional branch entered the **middle** of that region at `0x1418147FC`. Once patched, that incoming branch jumped into detour data rather than the original comparison. Physical testing produced three repeatable launch crashes. The patch was rolled back.

**Lesson:** before choosing a multi-instruction patch span, enumerate potential branch, call and exceptional control-flow entry targets into *every instruction* it would overwrite. Relocatable overwritten instructions alone do not establish safety. Historical RVA above is not a reusable hook recommendation.

## Paired-hook preflight

In Creep Chaos Probe 007 (0.6.3), the animation resolver RVA was mistyped `0x02312A30` instead of `0x02313A30` (a 0x1000 discrepancy). The signature check rejected it; both dependent presentation mutations remained off, and vanilla sprites remained visible. **This is a successful fail-closed guard, not proof of the intended animation-key hypothesis.** Probe 008 then corrected the address and physically validated the paired path.

## Synthetic x86-64 disassembly negative-control lesson (2026-10-13)

**CI-verified synthetic fixture, not an original game hook:** In Berserker's offline Probe 011A–P, changing just the leading REX prefix `0x48` of a synthetic 64-bit `LEA` did **not** remove all decodable RIP-relative references to its string target. The remaining instruction bytes can form another valid instruction starting at the next byte (32-bit destination register). The first synthetic negative therefore failed, and the test was corrected to mutate the actual `LEA` opcode. The corrected synthetic positive and negative tests passed in GitHub CI.

**Reusable safety implication:** a single-byte modification or an assembler disassembly at one chosen start address does not prove that an x86-64 instruction is absent, nor that entering the changed span through another boundary is harmless. Validate exact instruction boundaries, overlapping decodings and inbound branch targets before any native detour or patch. The synthetic negative proves an *analysis pitfall*, **not** safe or unsafe game hooking.

## Minimal safety checklist

1. Verify full executable build identity and expected target instruction bytes.
2. Check instruction boundaries **and inbound control flow into the overwrite span**.
3. Use complete build-specific profiles: never mix one version's RVA with another's object offsets.
4. Treat multiple native hooks as a transactional unit if partial installation would corrupt presentation or data.
5. Disable unsupported builds and revert to the last known-good hooks after a crash.
6. Consider concurrency: two independently installed mods detouring the same entrypoint may conflict even when each works alone.
7. Test in-game after static verification; keep sanitized logs and negative tests.

Published addresses are historical research anchors, **not** general patch instructions or a safe-compatibility guarantee.
