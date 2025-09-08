# 1. Unified Risk & Control Model
{{#CH1-RISKS}}

| Pillar | Risk | Severity (1-5) | Standard Mitigation |
|---|---|---:|---|
| Governance | Unapproved data processing | 5 | HITL approvals; audit trail |
| Environment | Over-privileged agents | 4 | Least-privilege devcontainer; scoped tokens |
| Data | Sensitive info leakage | 5 | Redaction; denylist; test data only |
| Operations | Runaway loops / cost spikes | 4 | Step caps; budget alerts; circuit breakers |

> Always document mitigations in each blueprint's **Local Risks** and wire KPIs to dashboards.

