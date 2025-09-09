---
source: "Claude Code Documentation"
retrieved: 2025-09-09
owner: "development-team"
tags: [claude-code, agent-blueprints, reference, vendor, claude]
blueprint: claude-agents
policy: vendor-specific
---

# **Introduction: A Framework for Responsible Agentic Development**

**Purpose.** This manual is a complete, self-contained guide for designing, operating, and governing agentic systems with **Claude Code**\-style workflows. It is written to be both a practitioner's handbook and a durable architectural reference. While the examples use Claude-centric conventions, all patterns are deliberately **transferable** to other agent frameworks.

**Scope.** Part A contains end-to-end, production-ready **Blueprints** you can drop into a secure, reproducible **Devcontainer**environment. Part B is an exhaustive **Reference Manual**, structured for rapid retrieval (RAG-friendly) with dense tables and checklists.

---

## **Risk & Control Overview (High-Level)**

This manual applies a **Unified Security Model** with four pillars—**Governance, Environment, Data, and Operations**—and twelve controls. These controls recur across all blueprints.

| Pillar | Control | Intent | Minimum Standard (Gold) | Diagnostic Question |
| ----- | ----- | ----- | ----- | ----- |
| Governance | Purpose & Scope | Prevent capability creep and unclear authority. | Written scope with allowed tasks, prohibited tasks, and escalation rules; reviewed quarterly. | "What can this agent never do?" |
| Governance | Human-in-the-Loop (HITL) | Ensure accountable oversight for material actions. | Mandatory approvals for data exfiltration, code commits, spend \> threshold. | "Who approves high-impact actions?" |
| Governance | Ethical Guardrails | Reduce harm, bias, and misuse. | Bias testing before release; explicit content boundaries; DPIA for personal data. | "What harms have we pre-empted?" |
| Environment | **Devcontainer Baseline** | Reproducibility, immutability, least privilege. | Devcontainer with pinned base images, non-root user, read-only secrets mount, network egress policies. | "Can I rebuild this bit-for-bit?" |
| Environment | Secret Hygiene | Prevent credential leakage. | Secrets via env vars and injected mounts; no secrets in repo; secret scanners in CI. | "Could a 'strings' dump leak keys?" |
| Environment | Dependency Integrity | Pin and verify dependencies. | SBOM generation; checksum verification; supply-chain policy. | "Can we prove what we ran?" |
| Data | Data Minimisation | Limit and mask data exposure. | Field-level allow-lists; PII masking; dataset versioning; retention rules. | "Why does the agent need this field?" |
| Data | Privacy & Consent | Respect lawful and ethical use. | Consent catalogue; DPIA; deletion and access rights flows. | "Can we honour a deletion request?" |
| Data | Red-Team Prompts | Detect prompt-injection & data exfil. | Inbound content filtering; model-side system prompts enforcing deny-lists. | "How would an attacker trick the agent?" |
| Operations | Observability | Traceability for audit and debugging. | Correlatable request IDs; structured logs; metric baselines and SLOs. | "Can we reconstruct any decision path?" |
| Operations | Reliability | Maintain useful service under faults. | Retries, timeouts, circuit breakers; idempotent actions; dead-letter queues. | "How do we fail safely?" |
| Operations | Cost Control | Prevent runaway costs. | Quotas per agent; budget alarms; token/latency dashboards; caching. | "What stops a spend spiral?" |

**Mandate:** The **Devcontainer** is the **single canonical environment**. Every blueprint provides a Devcontainer-first implementation with pinned dependencies, non-root users, and explicit secret handling.

---

## **Agent Query Index (for RAG-Style Lookups)**

| Common Question | See Section | Why |
| ----- | ----- | ----- |
| "How do I start a secure dev environment for agents?" | Part A · Ch.1 | Devcontainer baseline, troubleshooting, central config. |
| "What does a complete blueprint look like?" | Part A · Ch.2–8 | Each chapter is a full spec: diagrams, commands, scripts, risk matrix. |
| "How do I orchestrate multiple agents safely?" | Part A · Ch.8 | Delegation, hand-offs, JSON contracts, fault tolerance. |
| "Where are CLI flags, exit codes, and file formats?" | Part B · Ch.10–13 | Core CLI, tools, extensions, configuration schemas. |
| "How do I add human oversight and approvals?" | Part A · Ch.9; Appx A | Patterns summary, HITL decision trees, autonomy gates. |
| "How do I reduce cost/latency without losing quality?" | Patterns in each blueprint; Appx A | Caching, routing, summarisation ladders, adaptive context. |
| "How do I integrate with LangChain or AutoGPT?" | Appx B | Interop patterns, adapters, contracts. |
| "How do I simulate agents locally before release?" | Appx C | Simulation harness, mocks, deterministic seeds. |
| "What are ethical considerations per use-case?" | Each blueprint's Ethics; Intro | Bias, privacy, explainability, user expectations. |

---

# **Part A: Agent Blueprints & Patterns — Practical Recipes**

## **Chapter 1: The Standard Development Environment**

### **1.1 The Recommended Architecture: Why We Use Devcontainers**

**Goals.** Guarantee **reproducibility**, **least-privilege**, and **auditability**. Avoid "works on my machine". Standardise shell tools, Python/Node tooling, CUDA where applicable, and policy guards.

**Baseline Characteristics.**

* **Non-root user** with minimal capabilities.  
* **Pinned image** (digest, not just tag).  
* **Read-only** mounts for code; **tmpfs** for transient artefacts.  
* **Secrets** injected via **devcontainer features** or environment file in a secrets mount (`/run/secrets`), never committed.  
* **Network policies**: deny-all outbound by default; explicit allow-list per blueprint; optional HTTP proxy for inspection.  
* **Observability baked-in**: cli wrappers emit JSON logs with request\_id, model, token\_use, latency, exit\_code.  
* **SBOM** built at container creation; dependency lockfiles enforced.

**Devcontainer Skeleton.**

`// .devcontainer/devcontainer.json`  
`{`  
  `"name": "claude-agents-gold",`  
  `"image": "mcr.microsoft.com/devcontainers/base:ubuntu-24.04@sha256:<<pinned_digest>>",`  
  `"remoteUser": "vscode",`  
  `"features": {`  
    `"ghcr.io/devcontainers/features/python:1": { "version": "3.11" },`  
    `"ghcr.io/devcontainers/features/node:1": { "version": "20" }`  
  `},`  
  `"containerEnv": {`  
    `"AGENT_HOME": "/workspaces/agents",`  
    `"AGENT_LOG_DIR": "/workspaces/agents/.logs"`  
  `},`  
  `"runArgs": [`  
    `"--cap-drop=ALL",`  
    `"--pids-limit=512",`  
    `"--read-only",`  
    `"--tmpfs", "/tmp:rw,exec,nosuid,size=256m",`  
    `"--mount", "type=bind,source=${localWorkspaceFolder},target=/workspaces/agents,consistency=cached"`  
  `],`  
  `"mounts": [`  
    `"source=agent-secrets,target=/run/secrets,type=volume,readonly",`  
    `"source=agent-cache,target=/workspaces/agents/.cache,type=volume"`  
  `],`  
  `"onCreateCommand": "bash .devcontainer/provision.sh",`  
  `"postStartCommand": "bash .devcontainer/post_start.sh",`  
  `"customizations": { "vscode": { "extensions": ["ms-python.python","github.vscode-github-actions"] } }`  
`}`

`# .devcontainer/provision.sh`  
`set -euo pipefail`  
`umask 027`  
`mkdir -p "$AGENT_LOG_DIR" .cache .sbom`  
`pip install --no-cache-dir --require-hashes -r requirements.lock`  
`npm ci --ignore-scripts`  
`python - <<'PY'`  
`print("Provisioned devcontainer with pinned deps.")`  
`PY`

**Note.** Use `requirements.lock` and `package-lock.json` with **hashes**. Generate an SBOM (e.g., `cyclonedx`for npm and pip) into `.sbom/`.

---

### **1.2 Setting Up Your First Devcontainer for Claude Code**

**Steps.**

1. **Clone** the repository with blueprints.  
2. **Open in Devcontainer** (VS Code / CLI).  
3. **Inject secrets** into the named volume `agent-secrets` (e.g., `ANTHROPIC_API_KEY`, model IDs), never into files under version control.  
4. **Verify health** using `make doctor`.

`# Makefile (excerpt)`  
`SHELL := bash`  
`.DEFAULT_GOAL := help`

`help: ## List commands`  
	`@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-28s\033[0m %s\n", $$1, $$2}'`

`doctor: ## Validate environment`  
	`@bash scripts/doctor.sh`

`run-%: ## Run blueprint by name (e.g., make run-docs)`  
	`@bash scripts/run_blueprint.sh $*`

`# scripts/doctor.sh`  
`set -euo pipefail`  
`echo "Checking secrets…"`  
`test -r /run/secrets/ANTHROPIC_API_KEY || { echo "Missing ANTHROPIC_API_KEY secret"; exit 2; }`  
`echo "Checking connectivity policy…"`  
`# Example: verify only allow-listed domains`  
`echo "OK"`

---

### **1.3 Creating a Centralised, Version-Controlled Agent Configuration (`~/.claude_agents`)**

**Goal.** A single **source of truth** for agent defaults and per-blueprint overrides, mounted read-only into containers.

**Schema.** `config.yaml`:

`version: 1`  
`defaults:`  
  `model: "claude-ops"        # alias; resolved by adapter`  
  `temperature: 0.2`  
  `max_tokens: 2048`  
  `timeouts:`  
    `request_s: 60`  
    `connect_s: 10`  
  `redaction:`  
    `pii: ["email", "phone", "address"]`  
    `strategy: "mask"         # mask|drop`  
  `allowlist_domains:`  
    `- "api.vendor.local"`  
    `- "internal.registry.local"`  
`logging:`  
  `level: "info"`  
  `format: "json"`  
  `destination: "stdout"      # stdout|file`  
`blueprints:`  
  `documenter:`  
    `system_prompt_ref: "prompts/documenter.system.md"`  
    `tools: ["fs.read","git.diff","markdown.format"]`  
  `guardian_watcher:`  
    `event_bus: "fsnotify"`  
    `debounce_ms: 500`

**Pattern.** Keep `~/.claude_agents` in a private repository, mounted to `/opt/claude/config` **read-only**.

---

### **1.4 Troubleshooting Common Devcontainer Issues**

| Symptom | Likely Cause | Fix | Prevent |
| ----- | ----- | ----- | ----- |
| Cannot write under `/workspaces/agents` | Read-only rootfs | Use `/tmp` or `.cache` tmpfs; ensure proper bind mount for workspace. | Keep read-only and write to tmpfs; commit artefacts via scripts. |
| "Module not found" despite lockfiles | Lock mismatch or cache poisoning | `pip install --require-hashes`; clear `.cache`; re-build container. | Enforce CI job to rebuild and verify SBOM. |
| Keys read but SDK fails | Wrong env var name or scope | Map secret names in adapter; verify with `doctor`. | Provide a secrets contract in Reference → Configuration. |
| External calls blocked | Egress policy | Add domain to `allowlist_domains`; re-build with policy. | Explicitly document endpoints per blueprint. |
| High latency / timeouts | Large prompts or poor retries | Apply summarisation ladders; set backoff with jitter; cache embeddings. | Include cost/latency SLOs in blueprint success criteria. |

---

## **Chapters 2–6: Core Agent Blueprints**

**Format Mandate (per blueprint):** Objective & Success Criteria · Real-World Case Study · Agent Workflow Diagram (Mermaid) · Custom Slash Command (`.md`) · Invocation Script (`.sh`) with audit logging · Prompt Adaptation Template · Risk & Control Matrix · Ethical Considerations · Failure Modes & Recovery (with code).

---

### **Chapter 2: The Automated Documenter**

**Objective & Success Criteria.**  
Automate generation of high-quality architecture notes, ADRs (Architecture Decision Records), and README files from source code and commit history.

* **Success Metrics:**  
  * 95% of PRs include an auto-generated draft ADR within 60 seconds of push.  
  * Documentation freshness score ≥ 0.9 (repo-level metric comparing code churn vs. doc update cadence).  
  * Human edit time per ADR ≤ 5 minutes median.

**Real-World Case Study (Condensed).**  
A platform team integrated the Documenter into their CI. On each feature branch push, the agent reads `git diff`, relevant files, and open issues, producing: a summarised design delta, risk notes, follow-ups, and a changelog snippet. Reviewers accept or adjust the ADR within minutes.

**Agent Workflow Diagram.**

`flowchart TD`  
  `A[Git Push] --> B[CI Hook: run-documenter.sh]`  
  `B --> C[Collect: git diff, touched files, issue refs]`  
  `C --> D[Context Compression & Chunking]`  
  `D --> E[LLM: Draft ADR + README updates]`  
  `E --> F[Validation: templates, lint, PII scan]`  
  `F --> G{HITL? Policy requires?}`  
  `G -- Yes --> H[Open PR comment with Draft + Require Approval]`  
  `G -- No --> I[Commit to docs/ & push branch]`  
  `H --> I`  
  `I --> J[Emit audit log + metrics]`

**Custom Slash Command (`prompts/documenter.command.md`).**

`---`  
`name: "/documenter"`  
`version: "1.0"`  
`intent: "Generate ADR and README updates from code changes"`  
`inputs:`  
  `- id: git_diff`  
    `type: text`  
    `required: true`  
  `- id: touched_files`  
    `type: json`  
    `required: true`  
  `- id: repo_context`  
    `type: text`  
    `required: false`  
`system:`  
  `- "You are a rigorous software architect. Write concise, testable ADRs."`  
  `- "Follow the ADR template with: Context, Decision, Status, Consequences, Alternatives."`  
  `- "Flag risks and unknowns explicitly."`  
`policies:`  
  `- "Never include secrets or raw tokens. Mask and warn."`  
  `- "Respect file allow-lists; do not invent APIs."`  
`style:`  
  `- "Australian English, active voice, crisp headings."`  
`outputs:`  
  `- id: adr_markdown`  
    `type: markdown`  
  `- id: readme_patches`  
    `type: unified_diff`  
`---`

`# Inputs`

`{{git_diff}}`

`# Touched Files`

`{{touched_files}}`

`# Task`

`1. Produce **ADR** in Markdown (adr/ADR-{{date}}-{{short-branch}}.md).`  
`2. Produce **README** patch hunks for sections impacted.`  
`3. Add a **Risk & Follow-Up** checklist with owners.`

**Invocation Script (`scripts/run-documenter.sh`).**

`#!/usr/bin/env bash`  
`set -euo pipefail`  
`export PATH="/usr/local/bin:$PATH"`

`CMD_NAME="documenter"`  
`RUN_ID="$(date +%Y%m%dT%H%M%S)-$CMD_NAME-$$"`  
`LOG_DIR="${AGENT_LOG_DIR:-.logs}"`  
`mkdir -p "$LOG_DIR"`

`git_diff="$(git diff --patch --stat HEAD~1..HEAD || true)"`  
`touched_files="$(git diff --name-only HEAD~1..HEAD | jq -R . | jq -s .)"`

`payload="$(jq -n \`  
  `--arg cmd "/documenter" \`  
  `--arg git_diff "$git_diff" \`  
  `--argjson touched_files "$touched_files" \`  
  `'{command:$cmd, inputs:{git_diff:$git_diff, touched_files:$touched_files}}')"`

`# Adapter pattern: route to provider via AGENT_ADAPTER (http|cli).`  
`adapter="${AGENT_ADAPTER:-http}"`  
`case "$adapter" in`  
  `http)`  
    `# Generic HTTP adapter (endpoint, model from env, secrets mounted).`  
    `response="$(curl -sS -X POST "${AGENT_API_BASE:-http://adapter.local}/run" \`  
      `-H "Authorization: Bearer $(cat /run/secrets/ANTHROPIC_API_KEY)" \`  
      `-H "Content-Type: application/json" \`  
      `--data "$payload")"`  
    `;;`  
  `cli)`  
    `response="$(agentctl run --command "/documenter" --json-input "$payload")"`  
    `;;`  
  `*)`  
    `echo "Unknown adapter: $adapter" >&2; exit 64`  
    `;;`  
`esac`

`echo "$response" | tee "$LOG_DIR/$RUN_ID.response.json" >/dev/null`

`# Extract outputs (defensive)`  
`echo "$response" | jq -r '.outputs.adr_markdown' > "adr/ADR-${RUN_ID}.md"`  
`echo "$response" | jq -r '.outputs.readme_patches' | git apply -p0 --index || true`

`# Structured audit`  
`jq -n --arg run_id "$RUN_ID" \`  
      `--arg blueprint "$CMD_NAME" \`  
      `--arg tokens "$(echo "$response" | jq -r '.usage.total_tokens // "n/a"')" \`  
      `--arg latency_ms "$(echo "$response" | jq -r '.metrics.latency_ms // "n/a"')" \`  
      `--arg exit_code "0" \`  
      `'{ts:now|toiso8601, run_id:$run_id, blueprint:$blueprint, usage:{tokens:$tokens}, metrics:{latency_ms:$latency_ms}, exit_code:$exit_code}' \`  
      `>> "$LOG_DIR/audit.jsonl"`

`echo "Documenter run complete: $RUN_ID"`

**Prompt Adaptation Template.**

`[Objective] Summarise the intent in one sentence.`

`[Scope Boundaries] Explicitly list: in-scope, out-of-scope.`

`[Evidence Pack] Enumerate artefacts (diffs, issues, design notes) with short rationales.`

`[Structure Preference] ADR headings, bullet density, code vs prose ratio.`

`[Risk Appetite] Conservative | Balanced | Bold (choose one and justify).`

`[Review Persona] Architect | Lead Engineer | Compliance | Ops SRE (select).`

**Risk & Control Matrix.**

| Risk | Vector | Control | Implementation |
| ----- | ----- | ----- | ----- |
| Secret leakage in diffs | Hard-coded keys in code | Secret scanner; redaction | Pre-LLM content filter; deny commit if match. |
| Hallucinated APIs | Model invents function names | Strict tool contracts; schema validate | Reject outputs lacking references to touched files. |
| Bias in documentation | Style misrepresents decision trade-offs | Multi-persona review | HITL reviewers rotate roles. |
| Cost blowout | Large diffs prompt large tokens | Chunking \+ map-reduce | Cap per-run tokens; summarise before synthesis. |

**Ethical Considerations.**  
Ensure ADRs reflect actual dissent and alternatives; do not "launder" contentious decisions as neutral facts. Preserve authorship and attributions.

**Failure Modes & Recovery.**

* **Timeouts / 429:** Exponential backoff with jitter.  
* **Invalid Diff Patch:** Dry-run `git apply --check`, fallback to manual patch file.  
* **Validation Fail:** Emit machine-readable errors; file to `adr/errors/`.

`# Snippet: resilient HTTP call`  
`for i in {1..5}; do`  
  `curl -sS ... && break || sleep $((RANDOM % 4 + i))`  
`done`

---

### **Chapter 3: The Guardian File-Watcher**

**Objective & Success Criteria.**  
Continuously watch a repository or directory, perform **policy checks** (PII, licence headers, binary blobs), and trigger safe actions (quarantine, notify, auto-fix).

* **Success Metrics:**  
  * 100% policy violations detected before merge to `main`.  
  * False positive rate \< 2%.  
  * Mean time to remediation \< 10 minutes.

**Case Study.**  
A data platform team uses Guardian to block accidental CSV uploads containing email addresses; the agent rewrites files to remove PII and opens a PR with masked data and remediation notes.

**Workflow Diagram.**

`flowchart TD`  
  `FS[fsnotify events] --> F{Filter}`  
  `F -- allow --> C[Policy Check Pipeline]`  
  `F -- ignore --> X[Drop]`  
  `C --> V[Violation?]`  
  `V -- No --> OK[Log + continue]`  
  `V -- Yes --> A[Agent Auto-Remediate]`  
  `A --> R[Create PR / Quarantine]`  
  `R --> N[Notify Owners + Audit]`

**Custom Slash Command (`prompts/guardian.command.md`).**

`---`  
`name: "/guardian"`  
`version: "1.0"`  
`intent: "Detect and remediate file policy violations"`  
`inputs:`  
  `- id: file_path`  
    `type: text`  
  `- id: file_excerpt`  
    `type: text`  
  `- id: policies`  
    `type: json`  
`system:`  
  `- "You enforce repository data handling policy. You are strict and explain your reasoning."`  
`policies:`  
  `- "Mask PII; never reveal full values."`  
  `- "Prefer minimally invasive remediations."`  
`outputs:`  
  `- id: remediation_patch`  
    `type: unified_diff`  
  `- id: incident_note`  
    `type: markdown`  
`---`  
`Check the content against the policies. If violation, propose minimal diff and draft an incident note.`

**Invocation Script (`scripts/run-guardian.sh`).**

`#!/usr/bin/env bash`  
`set -euo pipefail`  
`event_file="$1"`  
`policies_json="$(cat policies/policies.json)"`  
`excerpt="$(head -c 5000 "$event_file" || true)"`  
`payload="$(jq -n --arg cmd "/guardian" --arg file_path "$event_file" --arg file_excerpt "$excerpt" --argjson policies "$policies_json" '{command:$cmd,inputs:{file_path:$file_path,file_excerpt:$file_excerpt,policies:$policies}}')"`  
`response="$(agentctl run --command "/guardian" --json-input "$payload")"`  
`echo "$response" | jq -r '.outputs.remediation_patch' | git apply -p0 --index || true`  
`echo "$response" | jq -r '.outputs.incident_note' > "incidents/$(date +%s)-$(basename "$event_file").md"`

**Prompt Adaptation Template.**

`[Policy Strictness] Low | Medium | High`  
`[Preferred Remediation] Mask | Remove | Replace | Quarantine`  
`[Incident Comms Tone] Formal | Neutral | Coaching`  
`[Auto-PR Threshold] files ≤ N, diff ≤ K lines`

**Risk & Control Matrix.**

| Risk | Control |
| ----- | ----- |
| Over-zealous deletion harms dev velocity | Require HITL for destructive actions; dry-run mode default. |
| PII missed in obscure formats | Expand detectors with file-type plugins; periodic red-team tests. |
| Infinite loops on file writes | Debounce events; ignore paths under `.guardian/`. |

**Ethics.** Minimise developer friction; default to **coaching** notes that explain policy rationale.

**Failure & Recovery.**  
If the patch fails, open an issue with remediation guidance. Use a **dead-letter** directory for files that repeatedly fail checks.

---

### **Chapter 4: The Janitor File-Management Agent**

**Objective & Success Criteria.**  
Maintain repository hygiene—archive stale artefacts, normalise directory structure, unify licences and headers, deduplicate assets.

* **Success Metrics:**  
  * Stale file count reduced by ≥ 80% in 30 days.  
  * Duplicate asset ratio \< 1%.  
  * Licence/header conformity \= 100% on `main`.

**Diagram.**

`flowchart LR`  
  `S[Scheduler] --> C[Catalogue Files]`  
  `C --> D[Deduplicate]`  
  `D --> H[Header/Licence Normaliser]`  
  `H --> A[Archive Stale]`  
  `A --> P[Propose PR]`

**Slash Command (`prompts/janitor.command.md`).**

`---`  
`name: "/janitor"`  
`version: "1.0"`  
`intent: "Hygiene: deduplicate, normalise headers, archive stale"`  
`inputs:`  
  `- id: file_catalogue`  
    `type: json`  
  `- id: policy`  
    `type: json`  
`outputs:`  
  `- id: actions`  
    `type: json`  
  `- id: patch`  
    `type: unified_diff`  
`---`  
`Given the catalogue and policy, produce a minimal set of actions and a patch.`

**Invocation Script.**

`#!/usr/bin/env bash`  
`set -euo pipefail`  
`catalogue="$(python scripts/catalogue.py)" # produces JSON listing`  
`policy="$(cat policies/janitor.json)"`  
`jq -n --arg cmd "/janitor" --argjson file_catalogue "$catalogue" --argjson policy "$policy" \`  
  `'{command:$cmd,inputs:{file_catalogue:$file_catalogue,policy:$policy}}' \`  
`| agentctl run --command "/janitor" --stdin \`  
`| tee ".logs/janitor-$(date +%s).json" \`  
`| jq -r '.outputs.patch' | git apply -p0 --index || true`

**Prompt Adaptation Template.**

`[Archive Cut-Off Days] e.g., 120`  
`[Header Template] SPDX or custom block`  
`[Structure Canon] example: src/, docs/, tooling/, scripts/`  
`[PR Grouping] One mega PR | Multiple topical PRs`

**Risk Matrix (Excerpt).**

| Risk | Control |
| ----- | ----- |
| Accidental deletion of live assets | Dry-run; require HITL for delete; tagging before archive. |
| Licence misclassification | Licence detector ensemble; manual override allow-list. |

**Failure Modes.**  
If dedup guesses wrong, **relink** rather than delete; keep a **quarantine** folder under `janitor/backup/` with retention.

---

### **Chapter 5: The Automated Tester**

**Objective & Success Criteria.**  
Generate missing tests, propose refactors for testability, run test suites, interpret failures, and open targeted PRs.

* **Success Metrics:**  
  * Test coverage delta ≥ \+10% quarter-on-quarter.  
  * Flaky test detection rate ≥ 90% with actionable suggestions.  
  * Mean time to triage failure \< 5 minutes.

**Diagram.**

`flowchart TD`  
  `CI[CI Trigger] --> R[Run Tests]`  
  `R --> F{Failures?}`  
  `F -- No --> G[Report coverage + badges]`  
  `F -- Yes --> E[Explain Failures]`  
  `E --> S[Suggest Fix or Test]`  
  `S --> P[Open PR with patch + rationale]`

**Slash Command.**

`---`  
`name: "/testsmith"`  
`version: "1.0"`  
`intent: "Analyse failures, propose minimal fixes and missing tests"`  
`inputs:`  
  `- id: test_logs`  
    `type: text`  
  `- id: coverage_report`  
    `type: text`  
  `- id: code_context`  
    `type: text`  
`outputs:`  
  `- id: patch`  
    `type: unified_diff`  
  `- id: analysis`  
    `type: markdown`  
`---`  
`Explain the root cause and propose minimal diffs with new tests where useful.`

**Invocation Script.**

`#!/usr/bin/env bash`  
`set -euo pipefail`  
`logs="$(cat artifacts/test.log)"`  
`coverage="$(cat artifacts/coverage.txt)"`  
`ctx="$(python scripts/context.py --failures artifacts/test.log)"`  
`jq -n --arg cmd "/testsmith" --arg test_logs "$logs" --arg coverage_report "$coverage" --arg code_context "$ctx" \`  
  `'{command:$cmd,inputs:{test_logs:$test_logs,coverage_report:$coverage_report,code_context:$code_context}}' \`  
`| agentctl run --command "/testsmith" --stdin \`  
`| tee ".logs/testsmith-$(date +%s).json" \`  
`| jq -r '.outputs.patch' | git apply -p0 --index || true`

**Prompt Adaptation Template.**

`[Testing Framework] pytest | jest | junit | go test | other`  
`[Refactor Budget] lines ≤ N`  
`[Stability Goal] Reduce flakiness; deterministic seeds always`  
`[HITL Threshold] Any patch touching prod code`

**Risk Matrix.**

| Risk | Control |
| ----- | ----- |
| Non-deterministic suggestions | Freeze seeds; require deterministic tests. |
| Over-broad patches | Patch size cap; enforce "smallest fix" rule. |

**Failure Modes.**  
If tests cannot be reproduced, agent files a **Repro Steps** issue template, attaching the environment fingerprint (versions, hashes).

---

### **Chapter 6: The CI/CD Security Analyst**

**Objective & Success Criteria.**  
Review pipelines for secret leakage, insecure steps, unpinned actions, missing SBOM, and policy violations; propose PRs.

* **Success Metrics:**  
  * 100% actions pinned by digest.  
  * SBOM present for all build artefacts.  
  * Zero plaintext secrets in logs.

**Diagram.**

`flowchart LR`  
  `Y[CI/CD YAML] --> A[Static Analysis]`  
  `A --> R[Risk Scoring]`  
  `R --> S{Score ≥ Threshold?}`  
  `S -- Yes --> P[Patch Proposal + PR]`  
  `S -- No --> N[Note + Dashboard]`

**Slash Command.**

`---`  
`name: "/cicd-analyst"`  
`version: "1.0"`  
`intent: "Harden CI/CD pipelines"`  
`inputs:`  
  `- id: pipeline_yaml`  
    `type: text`  
  `- id: findings`  
    `type: json`  
`outputs:`  
  `- id: risk_report`  
    `type: markdown`  
  `- id: patch`  
    `type: unified_diff`  
`---`  
`Check for: unpinned actions, missing SBOM, plaintext secrets, overbroad permissions.`

**Invocation Script.**

`#!/usr/bin/env bash`  
`set -euo pipefail`  
`yaml="$(cat .github/workflows/*.yml | sed 's/::/__/g')" # neutralise edge tokens`  
`findings="$(python scripts/scan_ci.py)"`  
`jq -n --arg cmd "/cicd-analyst" --arg pipeline_yaml "$yaml" --argjson findings "$findings" \`  
  `'{command:$cmd,inputs:{pipeline_yaml:$pipeline_yaml,findings:$findings}}' \`  
`| agentctl run --command "/cicd-analyst" --stdin \`  
`| tee ".logs/cicd-$(date +%s).json" \`  
`| jq -r '.outputs.patch' | git apply -p0 --index || true`

**Prompt Adaptation Template.**

`[Pinning Policy] digest-only | version-tag-ok`  
`[Secret Exposure Policy] fail on detection | warn`  
`[Permissions Policy] least privilege required`

**Risk Matrix (Excerpt).**

| Risk | Control |
| ----- | ----- |
| False sense of security | Require independent periodic audits; red-team tests. |
| Breakage from pinning | Test matrix with canary branch; staged rollout. |

**Failure Modes.**  
If pipeline breaks post-hardening, auto-rollback to prior commit and open an incident note with diff and rationale.

---

## **Chapter 7: Advanced Blueprint — The Adaptive Learning Agent**

**Objective & Success Criteria.**  
Continuously **self-improve** using feedback loops: evaluate outcomes, learn from mistakes, update prompts/tools/policies under strict governance.

* **Success Metrics:**  
  * Measurable KPI uplift (e.g., accuracy, latency, cost) month-over-month.  
  * Safe change rate: zero policy regressions after updates.

**Case Study.**  
A support triage agent collects **structured feedback** from analysts (thumbs up/down \+ rationale), runs nightly evaluations on a curated benchmark, and proposes small prompt/tool changes. Changes require HITL approval and roll out behind feature flags.

**Workflow Diagram.**

`flowchart TD`  
  `U[User/Analyst Feedback] --> L[Log & Label]`  
  `L --> E[Nightly Evaluation Runs]`  
  `E --> A[Analysis & Hypotheses]`  
  `A --> P[Proposed Prompt/Tool Changes]`  
  `P --> H{HITL Approval?}`  
  `H -- No --> R[Reject + Learn]`  
  `H -- Yes --> D[Deploy to Canary]`  
  `D --> M[Monitor Metrics]`  
  `M --> C{Success?}`  
  `C -- Yes --> W[Widen Rollout]`  
  `C -- No --> R`

**Slash Command.**

`---`  
`name: "/adapt"`  
`version: "1.0"`  
`intent: "Analyse feedback and propose minimal safe changes"`  
`inputs:`  
  `- id: feedback_events`  
    `type: json`  
  `- id: current_prompt`  
    `type: markdown`  
  `- id: tool_usage_stats`  
    `type: json`  
  `- id: eval_results`  
    `type: json`  
`outputs:`  
  `- id: change_proposal`  
    `type: markdown`  
  `- id: diff`  
    `type: unified_diff`  
`policies:`  
  `- "Propose the smallest change likely to help."`  
  `- "Never widen scope; adhere to policy constraints."`  
`---`  
`Produce a change proposal referencing evidence and provide a diff to the prompt or tool config.`

**Invocation Script.**

`#!/usr/bin/env bash`  
`set -euo pipefail`  
`jq -n \`  
  `--arg cmd "/adapt" \`  
  `--slurpfile fb ".data/feedback/*.json" \`  
  `--rawfile cp "prompts/triage.system.md" \`  
  `--slurpfile tu ".data/tool_stats/*.json" \`  
  `--slurpfile ev ".data/evals/*.json" \`  
  `'{command:$cmd,inputs:{feedback_events:$fb, current_prompt:$cp, tool_usage_stats:$tu, eval_results:$ev}}' \`  
`| agentctl run --command "/adapt" --stdin \`  
`| tee ".logs/adapt-$(date +%s).json" \`  
`| jq -r '.outputs.diff' | git apply -p0 --index || true`

**Prompt Adaptation Template.**

`[Primary KPI] accuracy | resolution_rate | latency | cost`  
`[Change Budget] tokens ≤ N, tools ≤ K modified`  
`[Risk Threshold] require approval if KPI delta < x%`  
`[Experiment Design] A/B | canary | shadow`

**Risk & Control Matrix.**

| Risk | Control |
| ----- | ----- |
| Reward hacking (optimising the metric, not the outcome) | Multiple KPIs with guardrails; qualitative sampling. |
| Prompt drift to unsafe behaviours | Unit tests for guardrails; evals covering safety; gated approvals. |
| Overfitting to recent feedback | Rolling, stratified eval sets; seasonality checks. |

**Ethical Considerations.**  
Do not make changes that reduce user agency or transparency. Explain changes in release notes with human-readable rationales.

**Failure & Recovery.**  
If canary metrics regress, **auto-revert** and annotate the proposal with counter-evidence. Maintain a **learning log** of rejected changes and reasons.

---

## **Chapter 8: Advanced Blueprint — The Collaborative Multi-Agent Orchestrator**

**Objective & Success Criteria.**  
Coordinate **specialised sub-agents** (e.g., Researcher, Planner, Coder, Reviewer) via robust protocols, ensuring correctness, safety, and bounded cost.

* **Success Metrics:**  
  * Tasks complete within cost/latency budget ≥ 95% of time.  
  * Handoff errors \< 1% (violations of schema or missing fields).  
  * HITL acceptance rate ≥ 90% for complex tasks.

**Handoff Protocol.**  
All inter-agent messages use a **standard JSON envelope**:

`{`  
  `"trace_id": "uuid",`  
  `"role": "researcher|planner|coder|reviewer",`  
  `"intent": "summarise|plan|implement|evaluate",`  
  `"inputs": { "schema_version": "1.0", "payload": { } },`  
  `"constraints": { "time_budget_s": 60, "token_budget": 2000 },`  
  `"expected_outputs": { "schema": "ref://schemas/plan.json" }`  
`}`

**Workflow Diagram.**

`sequenceDiagram`  
  `participant U as User`  
  `participant O as Orchestrator`  
  `participant R as Researcher`  
  `participant P as Planner`  
  `participant C as Coder`  
  `participant V as Reviewer`

  `U->>O: Task Request`  
  `O->>R: Research Envelope`  
  `R-->>O: Findings (JSON)`  
  `O->>P: Plan Envelope (with findings)`  
  `P-->>O: Plan (JSON with steps)`  
  `O->>C: Implement Envelope (with plan)`  
  `C-->>O: PR Patch + Notes`  
  `O->>V: Review Envelope (with patch)`  
  `V-->>O: Approval/Block + Feedback`  
  `O-->>U: Result + Audit Trail`

**Fault-Tolerant Orchestration Patterns.**

* **Saga / Compensation:** For multi-step tasks with side-effects, define compensating actions (e.g., revert a PR, delete temp resources).  
* **Circuit Breakers:** Pause a sub-agent on consecutive failures; escalate to HITL.  
* **Backpressure:** Queue and throttle requests per agent to respect budgets.

**Slash Command (`prompts/orchestrator.command.md`).**

`---`  
`name: "/orchestrate"`  
`version: "1.0"`  
`intent: "Delegate tasks to specialist agents"`  
`inputs:`  
  `- id: user_goal`  
    `type: text`  
  `- id: constraints`  
    `type: json`  
  `- id: policy`  
    `type: json`  
`outputs:`  
  `- id: result`  
    `type: markdown`  
  `- id: audit_trail`  
    `type: json`  
`---`  
`Decompose the goal, create a plan, and delegate to role agents using the JSON envelope. Enforce constraints strictly.`

**Invocation Script.**

`#!/usr/bin/env bash`  
`set -euo pipefail`  
`goal="$(cat -)"`  
`constraints="$(cat config/constraints.json)"`  
`policy="$(cat policies/orchestrator.json)"`  
`jq -n --arg cmd "/orchestrate" --arg user_goal "$goal" --argjson constraints "$constraints" --argjson policy "$policy" \`  
  `'{command:$cmd,inputs:{user_goal:$user_goal,constraints:$constraints,policy:$policy}}' \`  
`| agentctl run --command "/orchestrate" --stdin \`  
`| tee ".logs/orchestrate-$(date +%s).json" \`  
`| jq -r '.outputs.result'`

**Prompt Adaptation Template.**

`[Roles Enabled] researcher, planner, coder, reviewer, security-analyst`  
`[Budget] tokens ≤ N, walltime ≤ S`  
`[Risk Profile] conservative | balanced | experimental`  
`[Escalation Rules] auto-HITL conditions`

**Risk & Control Matrix.**

| Risk | Control |
| ----- | ----- |
| Message schema drift | Validate envelopes; versioned schemas; contract tests. |
| Cost explosion from chatter | Token budgets per agent; summarisation between steps; caching. |
| Conflicting actions | Orchestrator maintains a **global plan** and a lock for side-effectful steps. |

**Ethics.** Maintain user awareness that multiple agents are acting; provide a cohesive explanation and a single point of accountability.

**Failure & Recovery.**  
If a sub-agent stalls, the orchestrator re-routes to a backup role or requests clarifications from the user, persisting state for resumability.

---

## **Chapter 9: Patterns Summary — Cross-Blueprint Principles**

**Human-in-the-Loop Best Practices.**

* Define **autonomy levels**: 0 (advice only) → 3 (execute with rollback).  
* Use **gates**: high-impact actions require explicit approval.  
* Bind approvals to **scope-limited** commits or actions, not blanket permissions.

**Secure Tooling Patterns.**

* **Tool Allow-lists** with schemas; deny free-form shell access.  
* **Egress rules** configured per agent; shared "safe" DNS list.  
* **Content Filters** both inbound (prompt-injection) and outbound (secrets, PII).

**Compute Optimisation Patterns.**

* **Routing:** choose lighter models for classification or extraction; reserve frontier models for synthesis.  
* **Summarisation Ladders:** compress context at each step; attach citations.  
* **Caching & Embeddings:** memoise common queries; pin semantic search indices.  
* **Streaming & Early Cut-offs:** stop when sufficient confidence reached.

**Decision Trees (Examples).**

* *Single vs Multi-Agent?*  
  * **Single** if scope is narrow, latency-critical, or toolset small.  
  * **Multi** if tasks need specialised roles, parallelism, or explicit checks/balances.  
* *When to Canary Changes?*  
  * Canary if **policy**, **model**, or **tool** changes; otherwise direct rollout for low-risk prompt edits.

---

# **Part B: The Reference Manual — Technical Specifications**

**Format Mandate:** Dense, factual, self-contained, RAG-friendly. Prefer tables and lists. No external links.

---

## **Chapter 10: Core CLI Reference (Abstracted Adapter)**

**Philosophy.** Use a **provider-agnostic** adapter (`agentctl`) that accepts: a command name, inputs JSON, and returns structured outputs. Replace `agentctl` with your preferred runner; keep the contracts.

### **Commands**

| Command | Purpose | Inputs | Outputs | Exit Codes |
| ----- | ----- | ----- | ----- | ----- |
| `agentctl run --command <n>` | Execute a slash command with inputs (stdin or file). | `{"command": "/name", "inputs": {...}}` | `{"outputs": {...}, "usage": {...}, "metrics": {...}}` | `0` success, `64` bad args, `65`schema error, `69` provider unavailable, `75` retryable |
| `agentctl validate` | Validate command and schema. | `--file <prompt.md>` | Logs validation result | `0`/`1` |
| `agentctl budget` | Simulate token/cost usage. | `--file <prompt.md>` | Cost estimate | `0`/`1` |
| `agentctl trace` | Show last run trace. | `--id <run_id>` | JSON trace | `0`/`1` |

### **Environment Variables**

| Variable | Meaning | Example |
| ----- | ----- | ----- |
| `ANTHROPIC_API_KEY` | Provider credential injected via secrets volume. | `/run/secrets/ANTHROPIC_API_KEY` |
| `AGENT_API_BASE` | Adapter endpoint base URL. | `http://adapter.local` |
| `AGENT_LOG_DIR` | Directory for JSONL audit. | `.logs` |
| `AGENT_MODEL` | Default model alias. | `claude-ops` |
| `AGENT_BUDGET_TOKENS` | Per-run token cap. | `4000` |

### **File Conventions**

| Path | Purpose |
| ----- | ----- |
| `prompts/*.command.md` | Slash command specs, versioned. |
| `policies/*.json` | Policy packs (allow-lists, thresholds). |
| `scripts/*.sh` | Invocation wrappers with audit logs. |
| `.logs/*.jsonl` | Append-only audit trail (per run). |

---

## **Chapter 11: Tooling Reference**

**Tool Contracts.** Each tool declares **name**, **schema**, **idempotency**, **side-effects**, and **permissions**.

| Tool | Input Schema | Output Schema | Idempotent | Side-Effects | Min Permission |
| ----- | ----- | ----- | ----- | ----- | ----- |
| `fs.read` | `{ "path": "string", "bytes_max": 1048576 }` | `{ "path": "string", "content_b64": "string" }` | Yes | No | Read |
| `fs.write` | `{ "path": "string", "content_b64": "string", "mode":"0644" }` | `{ "path": "string", "bytes": "number" }` | No | Writes file | Write (HITL if outside workspace) |
| `git.diff` | `{ "rev": "string" }` | `{ "patch": "string" }` | Yes | No | Read |
| `http.get` | `{ "url":"string", "headers": {...} }` | `{ "status": 200, "body": "string" }` | Yes | Depends | Net (allow-listed) |
| `ci.validate` | `{ "pipeline": "yaml" }` | `{ "findings": [ ... ] }` | Yes | No | Read |
| `redact.pii` | `{ "text": "string", "policy": {...} }` | `{ "text": "string", "redactions": [...] }` | Yes | No | Read |

**Observability Fields (standard).**

| Field | Type | Description |
| ----- | ----- | ----- |
| `trace_id` | string | End-to-end correlation id. |
| `run_id` | string | Unique per invocation. |
| `usage.tokens_prompt` | number | Prompt tokens. |
| `usage.tokens_completion` | number | Completion tokens. |
| `metrics.latency_ms` | number | Walltime. |
| `policy_flags` | object | Any policy triggers (e.g., redaction applied). |

---

## **Chapter 12: Extensibility Reference**

**Adding a New Slash Command.**

1. Create `prompts/<n>.command.md` with `name`, `version`, `inputs`, `outputs`, `policies`.  
2. Run `agentctl validate` (schema checks).  
3. Write `scripts/run-<n>.sh` with audit logging.  
4. Add tests in `tests/commands/<n>_spec.json`.  
5. Document in `README` and `CHANGELOG`.

**Schema for `.command.md` (YAML frontmatter).**

| Field | Required | Description |
| ----- | ----- | ----- |
| `name` | Yes | Slash command (e.g., `/documenter`). |
| `version` | Yes | Semantic version. |
| `intent` | Yes | One-sentence purpose. |
| `inputs` | Yes | Array of `{id,type,required}`. |
| `outputs` | Yes | Array of outputs. |
| `system` | No | System prompts. |
| `policies` | No | Guardrail statements. |
| `style` | No | Writing style hints. |

**Event Bus Integration (Optional).**

* For watchers or schedulers, integrate with OS events (`fsnotify`) or cron-like schedulers.  
* Use **idempotency keys** to avoid duplicate processing.

---

## **Chapter 13: Configuration Reference**

**Global Config (`config.yaml`).** See Chapter 1.3.  
**Per-Blueprint Overrides.** Merge via shallow override, no implicit inheritance of **secret names**.

**Secrets Contract.**

| Secret | Used By | Scope | Storage |
| ----- | ----- | ----- | ----- |
| `ANTHROPIC_API_KEY` | All agents via adapter | Read | `/run/secrets` volume |
| `GIT_TOKEN` | Documenter/Janitor | Write PRs | `/run/secrets` |
| `CI_TOKEN` | CI Analyst | Modify pipeline | `/run/secrets` |

**Policy Packs.** Structured JSON:

`{`  
  `"version": 1,`  
  `"pii": { "mask": ["email", "phone"], "drop": ["credit_card"] },`  
  `"egress": { "allow": ["api.vendor.local"] },`  
  `"cost": { "tokens_per_run_max": 4000 }`  
`}`

**Budgeting & Quotas.**

| Setting | Default | Effect |
| ----- | ----- | ----- |
| `tokens_per_run_max` | 4000 | Soft cap per invocation; adapter enforces hard cut. |
| `monthly_token_budget` | 50,000 | Alert at 80%, deny at 100% without override. |
| `latency_slo_ms` | 2000 | Emit warnings on breaches. |

---

# **Appendices**

## **Appendix A: Core Agent Design Principles**

**A.1 Scalability Heuristics: Multi-Agent vs Single-Agent**

* Prefer **single-agent** for tight control loops, latency-sensitive tasks, or small toolboxes.  
* Prefer **multi-agent** when roles are naturally separable, require checks and balances, or benefit from parallel work.  
* Use **coarse-grained boundaries** between agents; avoid chatty micro-interactions to reduce cost.

**A.2 Observability Patterns**

* **Structured logs** (JSON) with `trace_id`, `run_id`, `policy_flags`.  
* **Metrics**: latency histograms, token counts, cache hit rate, cost per result.  
* **Traces**: span per tool call; error tags; policy decisions as events.  
* **Repro Packs**: save inputs and outputs sufficient to reproduce a run (with PII redaction).

**A.3 Evaluating Autonomy & Alignment**

* **Autonomy Levels:**  
  * L0: Advisory only.  
  * L1: Execute reversible actions (patches, PRs).  
  * L2: Execute with compensations (sagas).  
  * L3: Execute material actions under caps (spend/time), HITL for exceptions.  
* **Alignment Checks:** Unit tests for guardrails; red-team suites for prompt-injection and data exfil; **ethical review** for sensitive domains.

---

## **Appendix B: Interoperability with Other Frameworks**

**B.1 Patterns for Integrating with LangChain**

* Wrap slash commands as **LC Tools** with strict input/output Pydantic schemas.  
* Use LC's **runnables** to sequence: retrieval → summarise → generate → validate.  
* Maintain the **same policy packs**; do not fork guardrails between stacks.

**B.2 Calling Claude Code Agents from AutoGPT**

* Expose commands as **HTTP endpoints** in the adapter; AutoGPT calls them as tools.  
* Enforce quotas and schemas at the boundary; map AutoGPT roles to your **handoff envelope**.

---

## **Appendix C: Agent Simulation Toolkit**

**Purpose.** Validate designs **offline** without contacting providers.

**Pseudocode Harness.**

`class FakeLLM:`  
    `def __init__(self, seed=7):`  
        `self.seed = seed`  
    `def run(self, command, inputs):`  
        `# Deterministic canned behaviours for tests`  
        `return {"outputs": {"result": f"stub for {command} with {list(inputs.keys())}"}, "usage": {"tokens": 123}}`

`def simulate_pipeline():`  
    `llm = FakeLLM()`  
    `trace = []`  
    `for step in ["research", "plan", "implement", "review"]:`  
        `out = llm.run(step, {"payload": {}})`  
        `trace.append({"step": step, "out": out})`  
    `return trace`

`if __name__ == "__main__":`  
    `print(simulate_pipeline())`

**Testing Guidance.**

* Provide **golden files** for expected outputs.  
* Use **property-based tests** (no secret leakage, schema compliance).  
* Seed all randomness; simulate timeouts and retries deterministically.

---

## **Appendix D: Further Reading & Official Resources (Inline Summaries)**

* **Claude System Prompting.** Emphasise clear roles, constraints, and policies in the **system** section; encode hard boundaries ("never do X").  
* **Tool Use & Schemas.** Tools act as **capabilities**; prefer explicit JSON schemas and idempotent operations.  
* **Prompt Hygiene.** Avoid ambiguous instructions; use **few-shot** exemplars sparingly; control brevity vs completeness by specifying output shapes and token budgets.  
* **Evaluation.** Treat evals as **tests**: representative data, coverage for edge cases, safety checks, and regression suites aligned to KPIs.

---

## **Appendix E: Contributions Guide**

**Principles.**

* **Single Source of Truth.** Each blueprint owns a `.command.md`, a `run-*.sh`, and a policy file.  
* **Versioning.** Use semantic versions; update **CHANGELOG** with "Added/Changed/Fixed/Deprecated".  
* **Safety First.** New contributions must include: Risk & Control Matrix, Ethics, Failure & Recovery.

**How to Contribute.**

1. Fork and create a feature branch.  
2. Add your blueprint under `prompts/`, `scripts/`, and `policies/`.  
3. Provide **Mermaid** diagrams and a **Prompt Adaptation Template**.  
4. Run `make doctor && make test`.  
5. Open a PR with a short video or screenshot of a dry-run (no secrets).

**Acceptance Criteria.**

* Reproducible in the **Devcontainer**.  
* Passes schema validation and safety tests.  
* Includes observability and budgeting.

---

## **Closing Notes**

* **Unified Security Model:** All blueprints are Devcontainer-first, least-privilege by default, with explicit egress policies and secrets via read-only mounts.  
* **Timeless Patterns:** Modularity, orchestration, observability, and governance outlast any specific provider or SDK.  
* **Resource Efficiency:** Route intelligently, cache aggressively, and compress context. Cost is a **design parameter**, not an afterthought.

This manual is intentionally **self-contained** and **RAG-optimised**: dense headings, stable schemas, consistent terminology, and rich internal keywords ensure high-quality retrieval for both human readers and assistant agents.
