# Version and compatibility matrix

These are **research-specific fingerprints**, not an official list of releases. A PE fingerprint is not an API guarantee and must be verified against the running executable before using native offsets.

| Version | Evidence | Fingerprint or compatibility |
| --- | --- | --- |
| 0.5.8 | Harbinger native analysis and physical tests | SHA-256 `4ed3aed08971efd06b7415817c9da9a444b6c7f63dc2ec09540b572568a4e045`; timestamp `0x6A978218`, image size `0x04A1D000` |
| 0.6.0 | Harbinger relocation and 2026-09-20 physical controls test | Candidate A/B/C RVA `0x00AC2AE0` / `0x00AC36F0` / `0x00AC4300`; validate exact version-specific profile |
| 0.6.1 | Harbinger historical native study; Flame replay and trait captures | Harbinger referenced SHA-256 `91084e9a29c70993595a1d7d0c22064bae0ee82b0fc773c696077d15c2268f98`; timestamp `0x6AB1D950`; size `0x05264000`. Flame recorded stable ABI 9 |
| 0.6.2 | Harbinger documented shipping profile | timestamp `0x6ABC597E`, image size `0x052B8000`; Candidate A/B/C RVA `0x00BE42B0` / `0x00BE4D40` / `0x00BE57D0` |
| 0.6.3 | Creep Chaos runtime Probe 002/008; Flame 0.3.1 physical probe; Berserker 001/002 | Creep Chaos target SHA-256 `f21cf691799a83d9afa0ccae3e2b95862f5780446a501ee97860b91b752dbe2f`; timestamp `0x6AC5C567`, image size `0x052D6000`; Candidate A/B/C RVA `0x00BFC320` / `0x00BFCDB0` / `0x00BFD840`. Flame confirmed game/SDK 0.6.3 and ABI 9 |
| 0.7.0_beta1 (beta only) | Static PE inspection 2026-10-11 + advertised notes; no runtime test | SHA-256 `6c9cd659e727b4130766241e9d43b222454a8455609b40f9bf73c01d5136a94f`; timestamp `0x6AC5FAB4`, image size `0x056D8000`; [impact assessment](0.7.0-beta1-impact.md); **NOT cleared for any mod** |

**Never copy an RVA between builds.** Even within one version, do not rely on a version string alone: validate executable fingerprint and the expected instruction bytes. For SDK integration also capture the installed SDK tree/manifest and host ABI.

See [native hook safety](../native-hooks/safety.md), [simulation/replay](../architecture/simulation-and-replay.md), and [source provenance](../research/source-index.md).
