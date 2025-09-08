### BP-CICD — CI/CD Security Analyst {#CH4-BP-CICD}

**ID:** BP-CICD  
**Name:** CI/CD Security Analyst

**Objective & Success Criteria**  
- …

**Real-World Case Study**  
- …

**Agent Workflow (Mermaid):**
```mermaid
flowchart TD
  A[Trigger] --> B[Agent Step]
  B --> C[Tool/Handoff]
  C --> D[Outputs]
```

**Inputs / Outputs / Tools**  
- …

**Slash Command:**
```yaml
command: "/cicd"
args:
  - name: target
    type: string
examples:
  - "/cicd --target repo"
```

**Invocation Script (shell):**
```bash
#!/usr/bin/env bash
set -euo pipefail
# ...
```

**JSON Contract / Handoff:**
```json
{"task_id":"...", "role":"...", "artifacts":[{"name":"...","path":"..."}], "evidence":["..."], "status":"planned"}
```

**Risk & Control Matrix (Local)**  
- …

**Failure Modes & Recovery**  
- …

**Ethical Considerations**  
- …

**Telemetry & KPIs**  
- *Secrets detected* (by type) and block rate  
- *SAST issues* by severity (open/closed)  
- *DAST findings* and *false positive %*  
- *MTTR* for High/Critical vulns and approval overrides  
**Alerting thresholds**: any Critical open > 24h, FP% > 15%.

**Verification Steps (Smoke Tests)**  
- …


---

> **Sourced excerpt from:** Chat1_ _Claude Code_ Agent Blueprints, Patterns & Reference Manual_ version_ 1.md

Ch.5 – Automated Tester**. |
| “How do I enforce security in CI/CD?” | **Ch.6 – CI/CD Security Analyst**. |
| “How can an agent improve itself with feedback?” | **Ch.7 – Adaptive Learning Agent**. |
| “How do multiple agents collaborate safely?” | **Ch.8 – Multi‑Agent Orchestrator**. |
| “What pattern should I apply?” | **Ch.9 – Patterns Summary & decision trees**. |
| “CLI, tools, extensions, or config details?” | **Ch.10–13 – Reference Manual**. |

---

# **Part A: Agent Blueprints & Patterns: Practical Recipes**

Each chapter in Part A provides a **Gold Standard Blueprint** with:

* **Objective & Success Criteria**  
* **Real‑World Case Study**  
* **Agent Workflow Diagram** (Mermaid)  
* **Custom Slash Command (`.md`)** – version‑controlled agent logic  
* **Invocation Script (`.sh`)** – copy‑paste execution with audit logging  
* **Prompt Adaptation Template**  
* **Risk & Control Matrix**  
* **Ethical Considerations**  
* **Failure Modes & Recovery**

All blueprints assume the **Unified Security Model**: run inside the official **Devcontainer** and enforce least‑privilege, reproducible environments.

---

## **Chapter 1: The Standard Development Environment**

### **1.1 The Recommended Architecture: Why We Use Devcontainers**

**Rationale:** Devcontainers deliver consistent, reproducible, isolated workspaces with explicit dependencies, non‑root execution, read‑only mounts, and policy‑controlled secrets. This eliminates “works on my machine” drift, hardens supply chains, and simplifies onboarding, testing, and audit.

**Properties:**

* Immutable base image; locked package versions; SBOM generated.  
* Non‑root user; granular Linux capabilities; read‑only project mount with writable temp workdir.  
* Secret injection via environment providers; short‑lived tokens; no secrets in git.  
* Observability baked in (stdout/stderr structured JSON logging; OpenTelemetry exporter).  
* Predictable **Claude Code** CLI toolchain preinstalled; tools gated by wrappers with allow‑lists.

### **1.2 Setting Up Your First Devcontainer for Claude Code**

**Files:** Place in repository root.

**`devcontainer.json`**

{  
"name": "claude-code-secure",  
"image": "ghcr.io/org/claude-code:stable",  
"runArgs": \["--cap-drop=ALL", "--pids-limit=512"\],  
"containerUser": "dev",  
"remoteUser": "dev",  
"mounts": \[  
"source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=cached,readonly",  
"source=cc\_tmp,target=/tmp,volume"  
\],  
"features": {},  
"postCreateCommand": "bash .devcontainer/post-create.sh",  
"customizations": {  
"vscode": {  
"extensions
