# 1. Unified Risk & Control Model
{{#CH1-RISKS}}

| Risk Category | Description | Primary Controls | Residual Risk Notes |
|---|---|---|---|
| Data leakage | Unintended disclosure of sensitive data via prompts, logs, or tools. | Devcontainer isolation; redaction middleware; allow‑list I/O; content classifiers; encryption at rest/in transit; structured prompts with placeholders. | Residual risk is minimised but not eliminated; audit prompts and outputs. |
| Hallucination & over‑reach | Agent invents facts or acts beyond mandate. | Tool gating; schema‑validated outputs; retrieval grounding; confidence thresholds; human review gates; conservative defaults. | Track provenance and show evidence; fall back to safe templates. |
| Prompt injection | Adversarial content diverts intent. | Context sanitisation; policy preambles; deny‑list; source trust scoring; per‑tool guardrails; chain‑of‑custody tags. | Treat all external text as untrusted; validate before execution. |
| Abuse & bias | Harmful or biased outputs. | Policy filters; bias checks; counter‑prompting; controlled vocabularies; red‑team tests; explainability notes. | Escalate to human for sensitive cohorts or decisions. |
| Tool misuse | File system or network misuse. | Read‑only mounts; scoped tokens; ephemeral credentials; just‑in‑time secrets; rate limits; dry‑run mode. | Enable kill‑switch and emergency stop. |
| Reliability | Non‑deterministic outcomes, timeouts. | Retries with jitter; circuit breakers; checkpoints; idempotent handlers; dead‑letter queues. | Expose SLOs and error budgets. |
| Cost & compute | Runaway token or GPU use. | Budgets per command; batch and cache; small‑to‑large model cascade; streaming; aggressive early‑exit rules. | Continuous cost dashboards. |
| Compliance & audit | Missing traceability. | Signed audit logs; immutable storage; change control; approvals recorded in PRs. | Regular evidence capture against control mapping. |

---
