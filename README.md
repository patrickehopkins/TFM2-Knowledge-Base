# Teamfight Manager 2 — Modding Knowledge Base

Independent, **version-sensitive** research into Teamfight Manager 2 (TFM2) modding. This is not an official manual. Information is classified by the evidence actually collected; the same addresses and behaviors must not be assumed valid for other game builds.

## Browse

- [Contributing and evidence rules](CONTRIBUTING.md)
- [Provenance and source projects](research/source-index.md)
- [Game/build compatibility](game-versions/compatibility.md)
- [Simulation and replay separation](architecture/simulation-and-replay.md)
- [Multiplayer authority, synchronization, and networking research](architecture/multiplayer-authority-and-networking.md)
- [Camera and input](architecture/camera-and-input.md)
- [Native creep and champion presentation](architecture/creep-presentation.md)
- [Native action timing and effect processing](architecture/native-action-effects.md)
- [Athlete identity and tendencies](architecture/athletes-and-traits.md)
- [Buffs and playback audio](architecture/audio-and-frame-events.md)
- [Stable SDK boundaries](sdk-and-loader/stable-api-surfaces.md)
- [Native detour safety](native-hooks/safety.md)
- [Probe methodology](probes/probe-workflow.md)
- [Failures and negative evidence](failures/known-dead-ends.md)
- [Open investigations](research/open-questions.md)
- [Instructions for AI agents](AGENTS.md)

## Purpose and evidence language

Every claim should say whether it is **runtime verified**, **static-analysis supported**, **a hypothesis**, or **rejected/unsafe**. Capture game and SDK version, exact executable fingerprint when native addresses matter, reproduction conditions, findings, limitations, and source.

The original project owns its detailed logs, code, and runbooks. This repository curates *reusable* findings, not bulk copies of source-repository documentation. Do not publish private logs, third-party audio, game assets, or local identifiers without authorization.

Some originating repositories are private. Their source report titles are recorded without linking to inaccessible GitHub pages; the public summaries stand alone. Original private files and logs are not included.

Initial curation: **2026-10-09**. This is a starter selection, not a complete audit of every source file.
