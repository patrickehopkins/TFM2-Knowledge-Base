# Multiplayer research: simulation authority is not network transport

**Evidence status:** mixed. The TFM2 simulation/replay separation below has **runtime evidence** from prior mod probes; the multiplayer architecture, external-input synchronization, and provider comparisons are **research inferences / proposals, not runtime-verified TFM2 multiplayer behavior**.

**Research update:** 2026-10-10. **Game scope:** documented TFM2 0.6.1–0.6.3-era stable SDK and mod observations where specified; no claim that a complete multiplayer input path has been verified for any build. Recheck the exact game/SDK build before acting on these suggestions.

This page distills cross-project lessons relevant to mods that want human input, deterministic simulation changes, or compatible presentation while TFM2 is networked. It is **not** a library selection, networking implementation, or promise that TFM2 supports ten human players.

## Observed TFM2 facts (runtime verified, bounded)

- A watched match's simulation may run **ahead of visible replay/playback**. `StablePlayerAi::think()` operates on a simulation callback, not necessarily the currently displayed frame. Harbinger's attempt to gate the callback to the visible clock **did not establish authoritative direct control**. See [simulation and replay](simulation-and-replay.md) and the [Harbinger simulation report](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/simulation-research.md).
- The stable API has separate surfaces for deterministic match mutation (`StableMatchHook`), AI/input callbacks (`StablePlayerAi`) and watched-client/presentation observations. Seeing a command in one context is **not** proof that another peer or the match authority consumes it. See [SDK boundaries](../sdk-and-loader/stable-api-surfaces.md).
- Creep Chaos observed a synchronized match seed for its deterministic selection logic on a tested 0.6.3 build. **A shared seed alone does not prove identical full match state, authority, external input scheduling, or multiplayer correctness.**

**Not yet runtime verified:** whether two vanilla TFM2 match clients advance equivalent simulations at matching ticks; which process owns authoritative game outcomes; whether injecting an `InputV1` command on one peer replicates, diverges, or is rejected; whether an asynchronously received command can be applied deterministically at a scheduled tick; native ten-player control, snapshotting or rollback compatibility.

## Two independent feasibility gates

1. **Simulation / external input authority (the difficult TFM2-specific gate).** Find where the *actual advancing match simulation*, not merely replay presentation, accepts a player command. Prove that such input can be introduced at a defined simulation tick with known entity ownership and that peer behavior is consistent. An SDK callback allowing a local AI decision is **not** proof that it may safely read a network socket.
2. **Transport / connectivity (a separate engineering gate).** Once the input boundary exists, transmit an authenticated session's commands with correct tick association, ordering, sequence/deduplication, disconnect handling and observability. Many free transports exist. **None can supply a missing game simulation/input integration point.**

Failure through the stable SDK is not automatically proof that a lower-level implementation is impossible. A documented upstream API change, a supported host-side tick-queue, or carefully version-gated native experiments are *possible investigative branches*, **not** verified fixes. Ordinary OS keystroke injection does not by itself provide independent ownership of multiple champions.

## Study the native model before choosing a netcode design

Possible architectures are **hypotheses until TFM2 multiplayer experiments identify its authority model**:

| Model | What it would require | Caution |
| --- | --- | --- |
| Deterministic command/lockstep | Each simulation consumes the same ordered inputs at the same tick, with identical initial state and deterministic transitions | Different input arrival, mod configurations, callback timing or seed consumption can desync peers |
| Host-authoritative game state | One authoritative live simulation receives validated remote commands and replicates state to participants | Remote presentation and input response require deliberate latency/correction handling; compatibility with TFM2's existing match flow is unproved |
| Prediction and rollback | Snapshots or exact restoration, reproducible state stepping, historical input log and resimulation | TFM2's ahead-of-display watched-match simulation is **not** evidence of rollback support; do not start by importing GGPO |
| Commands from a separate controller/relay | A bridge queues tick-indexed commands for a real simulation input boundary | A successful socket/WebSocket connection demonstrates only connectivity, not control |

A plausible abstract separation is:

```text
transport -> session authentication/ownership -> tick-indexed command queue
          -> native simulation boundary -> state/replay diagnostics
```

Never call sockets, wall-clock clocks, system RNG or other asynchronous sources directly from a deterministic match callback if they can change simulation output. The goal is an input timeline the simulation can replay or consistently consume, **not** a network thread steering rendering.

## Minimal empirical test plan (proposal; not yet run)

1. Observe **two unmodified clients in one native multiplayer match**. Record match/session identity, tick, stable entity IDs, representative health/position/cooldown state and canonical state hashes at agreed checkpoints. Keep simulation tick, wall time, and visible replay cursor separate.
2. Identify first divergence (if any) before injecting anything. Record startup/seed, game build, mod configuration, authority/reconciliation events, and whether clients advance beyond visible playback.
3. At an agreed tick, inject one harmless, obvious `InputV1` movement command on **only one peer**. Determine if it propagates, remains local, is reconciled/rejected, or causes a mismatch. Preserve both traces. No strong multiplayer claim follows without this test.
4. If an authoritative input path is confirmed, try a **local two-process / two-machine transport** with a sequence number, session ID, stable champion ID, simulation tick, and command payload. Prove determinism and disconnect behavior before internet NAT/relay testing.
5. Only then stress delay, loss, jitter, reordering, duplicates, NAT/firewall restrictions, reconnect and divergence. Begin with two humans; **up to ten independent champion controllers** is a later research target, not an established capability.

Reproduce on each game version; retain exact build fingerprints for native hooks. If a mod only needs deterministic world changes or cosmetic chat, it may need **peer/replay consistency tests**, not its own network transport.

## Connectivity tools and service boundaries (candidate research, not adoption)

The following are **alternatives for the transport gate only**. Eligibility, limits, privacy requirements and current terms must be checked at implementation time.

| Candidate | Potential role | Important boundary |
| --- | --- | --- |
| Direct UDP / WebRTC / ICE | Player-hosted peer traffic and NAT traversal | Signaling, security and relay fallback are additional problems; a direct path is not guaranteed for every NAT pair |
| [Epic Online Services](https://onlineservices.epicgames.com/multiplayer) | P2P, lobbies and relays for eligible applications | Third-party **TFM2 mod** entitlement and credentials have **not** been established. Do not reuse a game's product identity without authorization |
| [Steam networking](https://partner.steamgames.com/doc/features/multiplayer/networking) | P2P/relay for eligible Steamworks applications | Owning or modding a Steam title does not grant its Steamworks credentials or an automatic right to Steam Datagram Relay |
| [GameNetworkingSockets](https://github.com/ValveSoftware/GameNetworkingSockets) | Open-source network transport implementation | Not itself a free entitlement to Valve's hosted relay backbone |
| [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) | HTTP/WebSocket prototype relay, auxiliary control or signaling | **Not** a generic free UDP game relay. Paid Spectrum is a distinct service; named production tunnels can involve a paid/renewed domain, and temporary Quick Tunnels are not production infrastructure |
| Tailscale / ZeroTier | Closed-peer tests without conventional port forwarding | Account requirements and free-plan device/user limits; not a guaranteed public ten-player solution |
| Localhost/LAN | First proof of control and deterministic command synchronization | Cannot validate external NAT or internet conditions |

No free provider should be documented as **permanently free or guaranteed to relay all traffic**. NAT and carrier-grade NAT (CGNAT) are interoperability cases on many networks; do not presume a particular developer's ISP or topology.

### Budget scope, not a TFM2 engine fact

The originating personal multiplayer mod projects require **$0.00/month in mandatory recurring infrastructure costs**. A reasonably priced **one-time** software license may be reviewed. This is a **project policy**, not proof that any provider or application is free forever, and not a general requirement imposed on unrelated TFM2 mods. Prefer player-hosted sessions, no developer-operated always-on paid host, and an interchangeable transport so terms can change without rewriting game simulation. This constraint does **not** solve the simulation authority gate.

## Source hierarchy and what each reference actually contributes

**Established networking concepts** (not proof of TFM2 compatibility):

- [Gaffer on Games: networked physics](https://gafferongames.com/categories/networked-physics/) — lockstep, state synchronization, prediction and state transport.
- [Valve Source multiplayer networking](https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking) — server authority, client prediction, interpolation and lag compensation.
- [GGPO developer guide](https://github.com/pond3r/ggpo/blob/master/doc/DeveloperGuide.md) — deterministic save/restore/rollback contracts, best studied when assessing rollback *feasibility*, not automatically adopted as TFM2 netcode.
- [TFM2 stable mod API](https://github.com/teamsamoyed/TeamfightManager2Mod/blob/main/docs/stable-api-reference.md) — check the real SDK contract for the target build. Our own paired-runtime probes are more probative than generic networking tutorials.

**Secondary implementation and testing examples**:

- [GGRS](https://github.com/gschup/ggrs) — an implementation with sync-test and multi-peer examples; not proof of TFM2 integration.
- [Drift Engine](https://driftengine.dev/) — inspect its compact deterministic step/rewind design and latency/loss visualization as educational material. Its approach combines established ideas; **no evidence here that it is novel, production-proven, appropriate for TFM2, or adopted by our projects**.
- Existing network impairment tools and replay/state-hash harnesses should be preferred to building a custom visual test lab without a demonstrated gap.

## Provenance and status

- **Runtime TFM2 evidence:** [Harbinger simulation research](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/simulation-research.md); [existing knowledge-base replay analysis](simulation-and-replay.md); [SDK boundaries](../sdk-and-loader/stable-api-surfaces.md). Tests span particular historical game builds; no two-client authority probe is claimed here.
- **Unexecuted cross-project test plan:** [Harbinger multiplayer reconnaissance](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/multiplayer-research.md), revised October 2026.
- **Related compatibility problem:** Creep Chaos `docs/DETERMINISM.md` tracks reproducible wave/ability outcomes without adopting networking infrastructure; Flame Simulator `docs/ROADMAP.md` treats shared chat/replay behavior as deferred compatibility work. Those project-specific roadmaps are not mirrored in this public knowledge base.

**Bottom line:** there are plausible zero-recurring-cost ways to move commands between machines. Whether a TFM2 mod can make those commands affect a synchronized **live authoritative simulation** remains **unverified** and is the critical next research gate.
