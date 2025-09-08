# 0. Router — Query-Pattern Matrix
{{#CH0-ROUTER}}

> Legend: **Positive** (must match), **Negative** (must not match). **Route** points to the blueprint section.

| Intent | Positive Patterns | Negative Patterns | Route | Key Risks |
|---|---|---|---|---|
| Generate docs for a repo | docs, document, readme, scan | secrets, payments | CH4-BP-DOC | Data: leakage; Ops: cost |
| Guard with file watcher | guard, watch, lint | deploy, payments | CH4-BP-GRD | Env: perms; Ops: noise |
| Clean/format code | janitor, cleanup, dead code | deploy, cdn | CH4-BP-JAN | Ops: destructive ops |
| Run tests with coverage | test, unit, integration, coverage | perf test | CH4-BP-TST | Ops: flakiness |
| CI/CD security analysis | pipeline, secrets, SAST, DAST | perf, load | CH4-BP-CICD | Governance: approvals |
| Multi-agent orchestration | orchestrate, multi-agent, plan | single prompt | CH4-BP-ORCH | Ops: runaway loops |
| Learn from feedback | adapt, improve, retrospective | delete data | CH4-BP-ADAPT | Governance: consent |

---

## Router Legend
- **Positive Patterns**: comma-separated keywords/regex the router uses to route queries.
- **Negative Patterns**: keywords/regex that disqualify a route.
- **Route**: stable section ID of the target blueprint.
