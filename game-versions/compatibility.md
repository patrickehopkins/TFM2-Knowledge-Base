# Version and compatibility matrix

These are **research-specific fingerprints**, not an official list of releases. A PE fingerprint is not an API guarantee and must be verified against the running executable before using native offsets.

| Version | Evidence | Fingerprint or compatibility |
| --- | --- | --- |
| 0.5.8 | Harbinger native analysis and physical tests | SHA-256 `4ed3aed08971efd06b7415817c9da9a444b6c7f63dc2ec09540b572568a4e045`; timestamp `0x6A978218`, image size `0x04A1D000` |
| 0.6.0 | Harbinger relocation and 2026-09-20 physical controls test | Candidate A/B/C RVA `0x00AC2AE0` / `0x00AC36F0` / `0x00AC4300`; validate exact version-specific profile |
| 0.6.1 | Harbinger historical native study; Flame replay and trait captures | Harbinger referenced SHA-256 `91084e9a29c70993595a1d7d0c22064bae0ee82b0fc773c696077d15c2268f98`; timestamp `0x6AB1D950`; size `0x05264000`. Flame recorded stable ABI 9 |
| 0.6.2 | Harbinger documented shipping profile | timestamp `0x6ABC597E`, image size `0x052B8000`; Candidate A/B/C RVA `0x00BE42B0` / `0x00BE4D40` / `0x00BE57D0` |
| 0.6.3 | Creep Chaos runtime Probe 002/008; Flame 0.3.1 physical probe; Berserker 001/002 | Creep Chaos target SHA-256 `f21cf691799a83d9afa0ccae3e2b95862f5780446a501ee97860b91b752dbe2f`; timestamp `0x6AC5C567`, image size `0x052D6000`; Candidate A/B/C RVA `0x00BFC320` / `0x00BFCDB0` / `0x00BFD840`. Flame confirmed game/SDK 0.6.3 and ABI 9 |
| 0.6.4 | Uploaded original Windows EXE and stable SDK archive, static inspection 2026-10-14; no runtime mod verification | SHA-256 `a1d05045405a12e2bed182daeafcad8c8a40cf29ab68ba6ea5bfd30257439582`; PE timestamp `0x6ACF3112`; image size `0x0533F000`; bundled stable SDK ABI **10** (0.6.3 used ABI 9). [ABI additions and cross-project impact](0.6.4-sdk-impact.md). [Five shared native entry points statically relocated with exact binary checks](0.6.4-native-relocation.md); **0.6.4 in-game detour execution still untested**. |

**Berserker project migration status (2026-10-14; source guard, not 0.6.4 runtime):** The 0.6.3 Candidate-A/WinMM mod retains its original `0.6.3` Rust game gate and version-specific detour signature checks. A new pre-install read-only SHA-256/PE fingerprint audit rejects the exact known 0.6.4 executable and any unknown build **before SDK refresh or DLL replacement**. This is a project-specific example of fail-closed version selection, **not a 0.6.4 runtime detour/gameplay verification; the separately documented Candidate-A RVA has now been statically relocated**. See the Berserker project's `docs/TFM2-0.6.4-ABI10-MIGRATION-ASSESSMENT.md`; the verifier itself still requires an executed Windows test.

**Never copy an RVA between builds.** Even within one version, do not rely on a version string alone: validate executable fingerprint and the expected instruction bytes. For SDK integration also capture the installed SDK tree/manifest and host ABI.

See [native hook safety](../native-hooks/safety.md), [simulation/replay](../architecture/simulation-and-replay.md), and [source provenance](../research/source-index.md).
