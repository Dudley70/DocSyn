## 0.4 Agent Query Index (Router) {{#CH0-ROUTER}}

**Legend**
- **Positive Patterns**: Any of these tokens in the user query is considered a *match signal*.
- **Negative Patterns**: Presence of any of these tokens *excludes* the row even if positives match.
- **Tie‑break**: If multiple rows match, prefer the one with the *most* positive matches; on ties, choose the row with a more specific Blueprint (BP-*).
- **Fallback**: If nothing matches, route to §I (Foundations) and ask a clarifying question.
- **Risk hinting**: The Gem should surface the listed **Key Risks** rows from §0.2 when answering.


> Deterministic routing matrix for the Gem. Match user intent against **Positive Patterns**; avoid **Negative Patterns** when present. Each row maps to a chapter/blueprint and a suggested quick action.

| Intent | Positive Patterns (any) | Negative Patterns | Chapter → Section | Blueprint | Quick Action | Key Risks |
|---|---|---|---|---|---|---|
| Generate documentation from a repo | `docs`, `readme`, `summarise`, `documentation` | `test`, `pipeline` | §IV → BP-DOC | BP-DOC | `/orchestrate --bp doc` | Data, Ops |
| Watch a folder and lint/guard | `watch`, `file watcher`, `lint`, `guard`, `monitor` | `deploy`, `scan container` | §IV → BP-GUA | BP-GUA | `/orchestrate --bp guard` | Env, Ops |
| Cleanup repo hygiene | `cleanup`, `janitor`, `dead code`, `format` | `security scan`, `ci/cd` | §IV → BP-JAN | BP-JAN | `/orchestrate --bp janitor` | Ops |
| Automated testing | `test`, `unit`, `integration`, `coverage` | `docs`, `generate documentation` | §IV → BP-TST | BP-TST | `/orchestrate --bp test` | Ops |
| CI/CD security analysis | `pipeline`, `ci/cd`, `sast`, `dast`, `secrets scan` | `doc`, `readme` | §IV → BP-CICD | BP-CICD | `/orchestrate --bp cicd` | Gov, Data, Ops |
| Adaptive learning/self-tuning | `feedback`, `self-improve`, `adapt`, `retrospective` | `deploy`, `prod push` | §IV → BP-ADAPT | BP-ADAPT | `/adapt --target ssot` | Gov, Ops |
| Multi-agent orchestration | `plan`, `handoff`, `multi agent`, `workflow`, `orchestrate` | `single step`, `quick fix` | §IV → BP-ORCH | BP-ORCH | `/orchestrate --bp orchestrator` | Gov, Env, Ops |
