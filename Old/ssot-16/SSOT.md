# Single Source of Truth (SSOT)

> Build: 2025-09-08T18:15:53.225757Z

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

# 1. Unified Risk & Control Model
{{#CH1-RISKS}}

| Pillar | Risk | Severity (1-5) | Standard Mitigation |
|---|---|---:|---|
| Governance | Unapproved data processing | 5 | HITL approvals; audit trail |
| Environment | Over-privileged agents | 4 | Least-privilege devcontainer; scoped tokens |
| Data | Sensitive info leakage | 5 | Redaction; denylist; test data only |
| Operations | Runaway loops / cost spikes | 4 | Step caps; budget alerts; circuit breakers |

> Always document mitigations in each blueprint’s **Local Risks** and wire KPIs to dashboards.

# 2. Standard Development Environment
{{#CH2-DEVCONTAINER}}

Use the reference **devcontainer.json** and **Dockerfile** from `/reference/` to ensure reproducible, least-privilege dev.

- Non-root user
- Minimal toolchain
- Explicit allowlisted CLIs

See also: `/reference/devcontainer.json`, `/reference/Dockerfile`.
---

# Adaptive Learning

---

# Cicd Analyst

---

# Documenter

## Objective
Provide automated documentation generation.

## Snippets
Short, actionable snippets belong here.

## Commands

```bash
/document --scan . --out docs/
```

```bash
/document --scan . --out docs/
```

---

# Guardian

---

# Janitor

---

# Orchestrator

---

# Tester
