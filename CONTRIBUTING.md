# Contributing research

Contributions are welcome when they distinguish **observation from inference** and provide enough context to reproduce or falsify a finding.

## Required finding record

1. **Question and status:** runtime verified, static evidence, hypothesis, or rejected/unsafe.
2. **Environment:** exact game version; SDK/host ABI and loader if applicable; executable SHA-256, PE timestamp and image size for native signatures.
3. **Method:** setup, instrumented callback/hook, steps, controls, and relevant commands.
4. **Evidence:** minimally necessary sanitized log excerpts, observed counts/screenshots, original source commit or document when public.
5. **Conclusion and limitations:** what was demonstrated, what was not, and possible confounders.
6. **Compatibility:** what must be revalidated after an update.

Passing compilation, static disassembly, and physical in-game verification are **different evidence classes**. Do not silently promote one into another. UI polling is not a precise event timestamp. Client simulation ticks are not necessarily playback time. A plausible cause of disappearance is not a verified death callback.

## Cross-repository workflow

1. Perform the experiment and preserve detailed results in the owning mod's repository.
2. Decide whether any finding is generalizable to other TFM2 mods.
3. Update or submit a focused knowledge-base page with version, status, and original evidence. Prefer a hyperlink rather than copying an entire implementation report.
4. If a newer test corrects an earlier claim, amend the existing page and preserve the old conclusion as a dated historical finding when instructive.
5. When native patches are involved, document fail-closed fingerprints, overwritten instruction control flow, and rollback.
6. When a finding is shared between projects, explicitly distinguish **research reuse** from **reusing hook implementations concurrently**; two mods detouring the same target may conflict.

## Publication hygiene

Do not upload third-party copyrighted recordings, proprietary game assets, personal file paths, user account details, machine identifiers, credentials, or raw unreviewed logs. Private repositories may be cited as provenance, but do not expose private material wholesale. Favor small descriptions and synthetic reproductions. For public commits, remember that author/committer metadata can expose an email even when the files themselves are clean.

## AI-assisted contributions

AI agents should follow [AGENTS.md](AGENTS.md) for detailed research, cross-repository updates, and verification requirements. Agents working in individual mod repositories should also follow that project's own instructions.

**No automatic mirroring:** a project-specific design decision or runbook does not inherently belong in the shared knowledge base.
