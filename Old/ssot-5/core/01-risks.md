## 0.2 Unified Risk & Control Model {{#CH0-RISKS}}

> Four-pillar governance with explicit **Severity** and **Mitigation** scales. Apply globally and augment with each blueprint's local matrix.

**Severity scale:** 1 (Low) · 2 (Moderate) · 3 (High) · 4 (Critical)  
**Mitigation scale:** A (Advisory) · B (Preventive) · C (Detective) · D (Compensating)

| Pillar | Control (Minimum Standard) | Diagnostic Question | Evidence | Severity (1–4) | Mitigation (A–D) |
|---|---|---|---|---:|:---:|
| Governance | Documented decision rights & HITL approvals | Are approval thresholds defined and enforced for risky actions? | Signed runbooks, approval logs | 3 | B |
| Environment | Least-privilege, sandboxed devcontainer | Does execution occur in a constrained, reproducible environment? | `devcontainer.json`, container policy | 2 | B |
| Data | PII/Secrets handling and redaction | Are inputs/outputs scanned/filtered for sensitive data? | Secrets scan reports, data maps | 4 | B |
| Operations | Observability & provenance | Can we reconstruct actions with evidence and trace IDs? | JSONL logs, trace context | 3 | C |

> For any recommendation, the Gem should surface the relevant rows and request approvals when Severity ≥ 3 and Mitigation ∈ {B, D}.
