---
part: A
order: 40
slug: blueprint-patterns
tags: [core, patterns, reference]
---

## **title: "Claude Code: Agent Blueprints, Patterns & Reference Manual" version: 1.0 authors: \["Principal AI Systems Architect"\]**

### **Version History**

* **1.0 (7 September 2025):** Initial release of the canonical guide.

---

# **Introduction: A Framework for Responsible Agentic Development**

This manual is a complete, self‑contained, and implementation‑ready handbook for building, operating, and governing agentic systems using Claude Code within a unified, secure **Devcontainer** environment. It is written to function as a timeless reference for general agentic architecture: the blueprints, patterns, and controls herein are transferable to other frameworks and LLMs.

**Design Tenets (evergreen):** modularity, least‑privilege security, explicit orchestration, deterministic boundaries, observability‑first, human‑in‑the‑loop escalation, testability, idempotency, and resource efficiency.

## **High‑Level Risk & Control Overview (Whole‑of‑Framework)**

| Risk Category | Description | Primary Controls | Residual Risk Notes |
| ----- | ----- | ----- | ----- |
| Data leakage | Unintended disclosure of sensitive data via prompts, logs, or tools. | Devcontainer isolation; redaction middleware; allow‑list I/O; content classifiers; encryption at rest/in transit; structured prompts with placeholders. | Residual risk is minimised but not eliminated; audit prompts and outputs. |
| Hallucination & over‑reach | Agent invents facts or acts beyond mandate. | Tool gating; schema‑validated outputs; retrieval grounding; confidence thresholds; human review gates; conservative defaults. | Track provenance and show evidence; fall back to safe templates. |
| Prompt injection | Adversarial content diverts intent. | Context sanitisation; policy preambles; deny‑list; source trust scoring; per‑tool guardrails; chain‑of‑custody tags. | Treat all external text as untrusted; validate before execution. |
| Abuse & bias | Harmful or biased outputs. | Policy filters; bias checks; counter‑prompting; controlled vocabularies; red‑team tests; explainability notes. | Escalate to human for sensitive cohorts or decisions. |
| Tool misuse | File system or network misuse. | Read‑only mounts; scoped tokens; ephemeral credentials; just‑in‑time secrets; rate limits; dry‑run mode. | Enable kill‑switch and emergency stop. |
| Reliability | Non‑deterministic outcomes, timeouts. | Retries with jitter; circuit breakers; checkpoints; idempotent handlers; dead‑letter queues. | Expose SLOs and error budgets. |
| Cost & compute | Runaway token or GPU use. | Budgets per command; batch and cache; small‑to‑large model cascade; streaming; aggressive early‑exit rules. | Continuous cost dashboards. |
| Compliance & audit | Missing traceability. | Signed audit logs; immutable storage; change control; approvals recorded in PRs. | Regular evidence capture against control mapping. |

## **Agent Query Index (for fast RAG)**

| Question | Where to look |
| :---- | :---- |
| “How do I standardise a secure dev setup?” | **Ch.1** (Devcontainer architecture, baseline configs). |
| “What blueprint documents my repos automatically?” | **Ch.2 – Automated Documenter**. |
| “How do I watch folders safely and act on changes?” | **Ch.3 – Guardian File‑Watcher**. |
| “How do I clean, tag, and archive project assets?” | **Ch.4 – Janitor File‑Management**. |
| “How do I run tests with an AI assistant?” | **Ch.5 – Automated Tester**. |
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
"extensions": \[  
"ms-vscode.azure-repos",  
"ms-azuretools.vscode-docker"  
\]  
}  
}  
}

**`Dockerfile`**

FROM ubuntu:22.04  
ENV DEBIAN\_FRONTEND=noninteractive  
RUN apt-get update && apt-get install \-y \\  
git curl jq bash ca-certificates build-essential python3 python3-pip \\  
&& rm \-rf /var/lib/apt/lists/\*  
\# Create non-root user  
RUN useradd \-ms /bin/bash dev && mkdir \-p /opt/tools && chown \-R dev:dev /opt/tools  
USER dev  
WORKDIR /home/dev  
\# Install Claude Code CLI and wrappers (placeholder script)  
RUN mkdir \-p \~/.local/bin && echo '\#\!/usr/bin/env bash' \> \~/.local/bin/claude \\  
&& echo 'exec /opt/tools/claude "$@"' \>\> \~/.local/bin/claude \\  
&& chmod \+x \~/.local/bin/claude  
ENV PATH="/home/dev/.local/bin:${PATH}"

**`.devcontainer/post-create.sh`**

\#\!/usr/bin/env bash  
set \-euo pipefail  
pip3 install \--user opentelemetry-sdk rich typer  
\# Create dirs  
mkdir \-p \~/.claude\_agents \~/.config/claude \~/.cache/claude \~/.logs  
chmod 700 \~/.claude\_agents \~/.config/claude \~/.logs  
\# Generate SBOM and store  
if command \-v syft \>/dev/null 2\>&1; then syft dir:/ \-o spdx-json \> \~/.logs/sbom.json || true; fi

**Secrets:** Provided via container runtime (e.g., `--env-file .env.local`), never committed.

### **1.3 Centralised, Version‑Controlled Agent Configuration (`~/.claude_agents`)**

Structure:

\~/.claude\_agents/  
common.policies.md \# global guardrails, deny/allow lists  
prompts/  
canon.md \# universal preamble and style  
commands/  
doc.md \# /doc blueprint command  
watch.md \# /watch blueprint command  
janitor.md \# /janitor blueprint command  
test.md \# /test blueprint command  
secscan.md \# /secscan blueprint command  
adapt.md \# /adapt blueprint command  
orchestrate.md \# /orchestrate blueprint command

Maintain via git (private repo). Use signed commits and PR‑based change control.

### **1.4 Troubleshooting Common Devcontainer Issues**

| Symptom | Likely Cause | Fix |
| :---- | :---- | :---- |
| Cannot access host files | Read‑only bind mount | Write to `/tmp` or add a dedicated writable volume. |
| Tool cannot reach network | Network disabled by policy | Use approved egress proxy; add domain to allow‑list. |
| Secrets missing | Env not injected | Verify `.env.local` and container runtime; avoid hard‑coding. |
| Permission denied | Non‑root user constraints | Grant minimal Linux capability or write to user‑owned paths. |
| High token spend | No budgets/stop rules | Configure per‑command budgets and early‑exit heuristics. |

---

## **Chapter 2: Blueprint – The Automated Documenter**

### **Objective & Success Criteria**

* **Objective:** Generate and maintain living documentation (READMEs, API references, ADRs) from source, tests, and comments.  
* **Success:** Deterministic docs produced; provenance lines included; diffs under threshold; gated by PR; cost within budget.

### **Real‑World Case Study**

A platform team standardises repo scaffolds. The Automated Documenter scans code, extracts public interfaces, generates a README, and drafts ADR updates. Outputs are PR‑ready with traceable sources.

### **Agent Workflow Diagram (Mermaid)**

flowchart TD  
A\[Trigger /doc\] \--\> B\[Collect repo metadata\]  
B \--\> C\[Select files via allow-list\]  
C \--\> D\[Ground with code chunks\]  
D \--\> E\[Generate docs w/ templates\]  
E \--\> F\[Validate schema & links\]  
F \--\> G{Pass budgets & QA?}  
G \-- yes \--\> H\[Write to /tmp/docs\]  
G \-- no \--\> I\[Fail with reasons\]  
H \--\> J\[Open PR with audit log\]

### **Custom Slash Command (`~/.claude_agents/commands/doc.md`)**

\# /doc – Automated Documenter v1.0

\#\# intent  
Create or update repo documentation deterministically from source artefacts.

\#\# inputs  
\- path: string (default: /workspace)  
\- sections: list (e.g., \["overview", "api", "adr"\])  
\- max\_tokens: int (default: 6000\)  
\- budget\_aud: float (default: 5.00)

\#\# policies  
\- Only read files under \`path\` matching allow-list: \`\*\*/\*.py, \*\*/\*.ts, \*\*/\*.md, \*\*/\*.yaml\`.  
\- Never execute code; read-only.  
\- Redact secrets patterns: \`AKIA\[0-9A-Z\]{16}\`, \`-----BEGIN\`.

\#\# system\_preamble  
You are a documentation engineer. Use factual extraction, not invention. Include a "Provenance" table naming source files and line ranges.

\#\# steps  
1\. Enumerate files by allow-list, chunk to 2–4k tokens with overlap.  
2\. For each section, generate content using canonical templates in \`\~/.claude\_agents/prompts/canon.md\`.  
3\. Merge sections; validate against JSON schema \`doc.schema.json\`.  
4\. Emit to \`/tmp/docs\` with deterministic filenames.

\#\# outputs  
\- \`/tmp/docs/README.md\`  
\- \`/tmp/docs/ADRs/ADR-XXX.md\`  
\- \`/tmp/docs/trace.json\` (sources, costs, tokens)

\#\# budgets  
\- Hard stop at \`max\_tokens\` and \`budget\_aud\`.

\#\# review  
If confidence \< 0.8, request human review note in output footer.

### **Invocation Script (`scripts/doc.sh`)**

\#\!/usr/bin/env bash  
set \-euo pipefail  
CMD="/doc"  
STAMP=$(date \-u \+"%Y%m%dT%H%M%SZ")  
LOG=\~/.logs/doc-${STAMP}.jsonl  
PATH\_ARG=${1:-/workspace}  
SECTIONS=${2:-"overview,api,adr"}  
MAXTOK=${3:-6000}  
BUDGET=${4:-5.00}

jq \-n \--arg cmd "$CMD" \--arg path "$PATH\_ARG" \\  
\--arg sections "$SECTIONS" \--argjson maxtok "$MAXTOK" \--arg budget "$BUDGET" \\  
'{ts: now, command:$cmd, path:$path, sections:($sections|split(",")), max\_tokens:$maxtok, budget\_aud:$budget}' \\  
| tee \-a "$LOG" \>/dev/null

claude run "$CMD" \\  
\--path "$PATH\_ARG" \\  
\--sections "$SECTIONS" \\  
\--max-tokens "$MAXTOK" \\  
\--budget-aud "$BUDGET" \\  
\--out /tmp/docs | tee \-a "$LOG"

\# Optional: open PR  
if command \-v gh \>/dev/null 2\>&1; then  
(cd "$PATH\_ARG" && gh pr create \-t "docs: auto ${STAMP}" \-b "Automated doc update" || true)  
fi

### **Prompt Adaptation Template**

ROLE: Documentation Engineer  
TONE: Precise, source-grounded, concise  
INSTRUCTIONS: Extract facts from code and comments; avoid speculation. Include a PROVENANCE table (file, lines, summary). Validate all relative links.  
VARIABLES: {project\_name}, {audience}, {sections}  
OUTPUT: Deterministic markdown sections per {sections}

### **Risk & Control Matrix**

| Risk | Control | Evidence |
| :---- | :---- | :---- |
| Fabricated API signatures | Require provenance table and schema check | `trace.json`, unit test `test_schema.py` |
| Secret exposure | Regex redaction \+ deny‑list readers | Redaction report in `trace.json` |
| Excess cost | Budget and token caps | Audit log lines with spend |
| File exfiltration | Read‑only mounts; allow‑list glob | Container spec, allow‑list config |

### **Ethical Considerations**

* Avoid biased language; use inclusive examples.  
* Respect code ownership; preserve licences and attributions.  
* Provide clear disclaimers where confidence is low.

### **Failure Modes & Recovery**

| Failure | Symptom | Recovery |
| :---- | :---- | :---- |
| Schema validation fails | Output rejected | Re‑generate section with stricter prompts; emit diff context |
| Budget exceeded | Hard stop | Re‑run with reduced scope (`sections`) or chunk size |
| Missing files | Empty sections | Fallback to templates with TODO markers |

**Backoff Snippet**

for i in 1 2 3; do  
if claude run /doc \--path "$PATH"; then break; fi  
sleep $(( (RANDOM%4 \+ 2\) \* i ))  
done  
---

## **Chapter 3: Blueprint – The Guardian File‑Watcher**

### **Objective & Success Criteria**

* **Objective:** Observe file events, classify intent, and trigger safe handlers (lint, scan, notify).  
* **Success:** Zero unsafe executions; actions within SLO; alerts deduplicated.

### **Real‑World Case Study**

A research folder receives frequent drops of PDFs. The watcher classifies and extracts metadata, then files artefacts to a controlled `ingest/` area with a receipt.

### **Agent Workflow Diagram**

flowchart TD  
A\[Inotify event\] \--\> B\[Classify file type\]  
B \--\> C{Allowed?}  
C \-- No \--\> D\[Quarantine \+ alert\]  
C \-- Yes \--\> E\[Select handler\]  
E \--\> F\[Run safe action\]  
F \--\> G\[Record receipt \+ metrics\]

### **Custom Slash Command (`~/.claude_agents/commands/watch.md`)**

\# /watch – Guardian File‑Watcher v1.0

\#\# intent  
Safely respond to file system events with allow‑listed handlers.

\#\# inputs  
\- watch\_path: string  
\- handlers: map {"pdf":"extract", "md":"index"}  
\- debounce\_ms: int (default 500\)

\#\# policies  
\- No network by default; handlers run in offline mode.  
\- Quarantine unknown types to \`\~/.quarantine\`.

\#\# steps  
1\. Listen for create/modify events.  
2\. Classify file using extension and magic bytes.  
3\. If allowed, call handler with read‑only access.  
4\. Write receipt JSON to \`\~/.receipts\`.

### **Invocation Script (`scripts/watch.sh`)**

\#\!/usr/bin/env bash  
set \-euo pipefail  
LOG=\~/.logs/watch-$(date \-u \+%Y%m%dT%H%M%SZ).jsonl  
claude run /watch \--watch-path "${1:-/workspace/inbox}" \--handlers "pdf=extract,md=index" | tee \-a "$LOG"

### **Prompt Adaptation Template**

ROLE: Safety Watcher  
CLASSIFY: {ext, magic, path}  
DECIDE: {allow, quarantine, handler}  
OUTPUT: JSON receipt {event\_id, action, handler, sha256, ts}

### **Risk & Control Matrix**

| Risk | Control |
| :---- | :---- |
| Malicious content | Magic‑byte checks; sandboxed parsing |
| Runaway events | Debounce; batch mode |
| Unauthorised exfiltration | No egress; receipts only |

### **Ethical Considerations**

* Respect privacy; avoid opening personal docs unnecessarily.  
* Provide visibility: human‑readable receipts and an opt‑out.

### **Failure Modes & Recovery**

| Failure | Recovery |
| :---- | :---- |
| Handler crash | Retry with exponential backoff; move to `dead-letter/` |
| Classification unknown | Quarantine and request human label |

---

## **Chapter 4: Blueprint – The Janitor File‑Management**

### **Objective & Success Criteria**

* **Objective:** Curate project assets: normalise names, deduplicate, tag, archive.  
* **Success:** Storage footprint reduced; dedupe ratio reported; no data loss; reversible moves.

### **Real‑World Case Study**

A design team’s asset library is chaotic. The Janitor enforces naming conventions, computes hashes, deduplicates, and archives by project \+ date.

### **Agent Workflow Diagram**

flowchart TD  
A\[/Run /janitor/\] \--\> B\[Inventory files\]  
B \--\> C\[Hash & size\]  
C \--\> D\[Detect duplicates\]  
D \--\> E\[Plan moves\]  
E \--\> F\[Apply changes\]  
F \--\> G\[Write manifest \+ report\]

### **Custom Slash Command (`~/.claude_agents/commands/janitor.md`)**

\# /janitor – File Management v1.0

\#\# inputs  
\- root: string  
\- dry\_run: bool (default true)  
\- naming: regex (default "^\[a-z0-9.\_-\]+$")  
\- archive: string (default "/workspace/archive")

\#\# steps  
1\. Walk \`root\`, compute sha256 and sizes.  
2\. Propose rename plan using \`naming\`.  
3\. Identify duplicates; keep canonical path.  
4\. If not dry-run, perform moves and write \`manifest.json\`.

### **Invocation Script (`scripts/janitor.sh`)**

\#\!/usr/bin/env bash  
set \-euo pipefail  
ROOT=${1:-/workspace}  
claude run /janitor \--root "$ROOT" \--dry-run false \--archive "/workspace/archive"

### **Prompt Adaptation Template**

ROLE: Repository Curator  
GOAL: Maximise organisation and reversibility  
CONSTRAINTS: No deletions; moves only; manifest required

### **Risk & Control Matrix**

| Risk | Control |
| :---- | :---- |
| Accidental destruction | Dry‑run default; manifest; reversible moves |
| Naming collisions | Hash suffixing; idempotent planning |

### **Ethical Considerations**

* Preserve authorship; keep metadata.

### **Failure Modes & Recovery**

| Failure | Recovery |
| :---- | :---- |
| Move fails | Retry; leave breadcrumb in manifest |
| Disk full | Backoff and alert; partial rollback |

---

## **Chapter 5: Blueprint – The Automated Tester**

### **Objective & Success Criteria**

* **Objective:** Generate and run unit/property tests; summarise failures with fixes.  
* **Success:** Coverage uplift within target; failing tests reproducible; diffs reviewed via PR.

### **Real‑World Case Study**

Legacy module without tests: the agent proposes tests from code reading, runs them, and suggests fixes as patches, gated by code owners.

### **Agent Workflow Diagram**

flowchart TD  
A\[/Run /test/\] \--\> B\[Select target modules\]  
B \--\> C\[Generate tests\]  
C \--\> D\[Run test suite\]  
D \--\> E{Failures?}  
E \-- Yes \--\> F\[Summarise \+ propose patch\]  
E \-- No \--\> G\[Publish coverage report\]

### **Custom Slash Command (`~/.claude_agents/commands/test.md`)**

\# /test – Automated Tester v1.0

\#\# inputs  
\- path: string (default /workspace)  
\- framework: enum(pytest,jest) (auto)  
\- coverage\_target: float (default 0.7)

\#\# steps  
1\. Identify public functions/classes.  
2\. Generate unit \+ property tests.  
3\. Execute tests; collect coverage.  
4\. Propose patch for failures; open PR.

### **Invocation Script (`scripts/test.sh`)**

\#\!/usr/bin/env bash  
set \-euo pipefail  
claude run /test \--path "${1:-/workspace}"

### **Prompt Adaptation Template**

ROLE: Test Engineer  
FOCUS: Edge cases, invariants, property-based tests  
OUTPUT: Tests \+ coverage summary \+ minimal patches

### **Risk & Control Matrix**

| Risk | Control |
| :---- | :---- |
| Flaky tests | Seeded randomness; isolate side effects |
| Unsafe execution | Run in sandbox; no network; timeouts |

### **Ethical Considerations**

* Avoid generating tests with proprietary data; keep examples generic.

### **Failure Modes & Recovery**

| Failure | Recovery |
| :---- | :---- |
| Toolchain mismatch | Auto‑detect framework; provide setup hints |
| Infinite loop | Hard timeouts; kill‑switch |

---

## **Chapter 6: Blueprint – The CI/CD Security Analyst**

### **Objective & Success Criteria**

* **Objective:** Enforce secure coding policies in CI/CD: secrets scanning, dependency risk, IaC checks.  
* **Success:** Block unsafe changes; provide actionable guidance; low false positives; audit trail in PR.

### **Real‑World Case Study**

On each PR, the agent scans diffs, flags risks with CWE references, suggests fixed snippets, and records decisions with justifications.

### **Agent Workflow Diagram**

flowchart TD  
A\[PR event\] \--\> B\[Diff ingest\]  
B \--\> C\[Secrets scan\]  
B \--\> D\[Dependency SBoM risk\]  
B \--\> E\[IaC policy checks\]  
C & D & E \--\> F\[Risk aggregation\]  
F \--\> G{Block or warn}  
G \-- Block \--\> H\[Require owner approval\]  
G \-- Warn \--\> I\[Comment with fixes\]

### **Custom Slash Command (`~/.claude_agents/commands/secscan.md`)**

\# /secscan – CI/CD Security Analyst v1.0

\#\# inputs  
\- pr\_number: int  
\- repo: string  
\- policies: list \["secrets", "deps", "iac"\]

\#\# steps  
1\. Fetch PR diff metadata (CI token scope: read-only).  
2\. Run policy checks; annotate with CWE/SLSA tags.  
3\. Emit SARIF and PR comment body with fixes.  
4\. If severity \>= High, set status to "failure".

### **Invocation Script (`scripts/secscan.sh`)**

\#\!/usr/bin/env bash  
set \-euo pipefail  
PR=${1:?pr number}  
REPO=${2:-origin}  
claude run /secscan \--pr-number "$PR" \--repo "$REPO" \--policies "secrets,deps,iac"

### **Prompt Adaptation Template**

ROLE: Secure Code Reviewer  
OUTPUT: SARIF \+ human summary with exact line refs and safe patches  
POLICIES: SLSA supply chain, least privilege, secret hygiene, IaC guardrails

### **Risk & Control Matrix**

| Risk | Control |
| :---- | :---- |
| Token over‑scope | Read‑only CI token; scoped permissions |
| False positives | Confidence threshold; owner override workflow |

### **Ethical Considerations**

* Explain decisions plainly; avoid shaming; provide learning links internally.

### **Failure Modes & Recovery**

| Failure | Recovery |
| :---- | :---- |
| Rate limited | Backoff; cache dependency DB |
| Tool error | Fallback to minimal regex checks |

---

## **Chapter 7: Advanced Blueprint – The Adaptive Learning Agent**

### **Objective & Success Criteria**

* **Objective:** Improve performance over time using closed‑loop feedback from outcomes and human ratings.  
* **Success:** Objective metrics trend upward; versioned policy/prompts updated via PR; rollback path available.

### **Real‑World Case Study**

A customer‑support triage agent tunes classification prompts and tool routing using weekly feedback, improving first‑contact resolution while reducing cost per ticket.

### **Agent Workflow Diagram**

flowchart TD  
A\[Task input\] \--\> B\[Baseline policy \+ prompt\]  
B \--\> C\[Execute & capture outcome\]  
C \--\> D\[Collect feedback (human \+ automatic)\]  
D \--\> E\[Analyse deltas vs KPIs\]  
E \--\> F\[Propose prompt/policy change\]  
F \--\> G\[AB test in shadow\]  
G \--\> H{Win?}  
H \-- Yes \--\> I\[Promote new version\]  
H \-- No \--\> J\[Discard \+ learn\]

### **Custom Slash Command (`~/.claude_agents/commands/adapt.md`)**

\# /adapt – Adaptive Learning v1.0

\#\# inputs  
\- task\_name: string  
\- kpis: list (e.g., \["accuracy", "cost", "latency"\])  
\- horizon: int (windows of events)

\#\# steps  
1\. Query outcomes \+ ratings for task\_name.  
2\. Attribute errors (content, tools, data).  
3\. Propose prompt/policy edits; render as PR.  
4\. Run shadow AB; report uplift with confidence interval.

### **Invocation Script (`scripts/adapt.sh`)**

\#\!/usr/bin/env bash  
set \-euo pipefail  
TASK=${1:?task}  
claude run /adapt \--task-name "$TASK" \--kpis "accuracy,cost,latency" \--horizon 200

### **Prompt Adaptation Template**

ROLE: Optimisation Scientist  
GOAL: Maximise KPI uplift under risk and cost constraints  
OUTPUT: Diff-style prompt edits \+ rationale \+ rollback notes

### **Risk & Control Matrix**

| Risk | Control |
| :---- | :---- |
| Regressions in production | Shadow AB, feature flags, gradual rollout |
| Metric gaming | Cross‑metrics guard; human review |

### **Ethical Considerations**

* Avoid over‑optimising for cheapness at the cost of fairness or quality; keep multi‑objective balance.

### **Failure Modes & Recovery**

| Failure | Recovery |
| :---- | :---- |
| Insufficient data | Extend horizon; use Bayesian shrinkage |
| Conflicting KPIs | Pareto analysis; human arbitration |

---

## **Chapter 8: Advanced Blueprint – Collaborative Multi‑Agent Orchestrator**

### **Objective & Success Criteria**

* **Objective:** Coordinate specialised agents via a primary orchestrator using standardised schemas and fault‑tolerant patterns.  
* **Success:** Clear delegation; bounded concurrency; deterministic hand‑offs; robust recovery.

### **Real‑World Case Study**

A product discovery workflow orchestrates a Researcher, Synthesiser, Reviewer, and Publisher, each with distinct tools and policies. The orchestrator enforces JSON contracts and retries independently per role.

### **Orchestration Diagram**

flowchart TD  
O\[Orchestrator\] \--\> R\[Researcher\]  
O \--\> S\[Synthesiser\]  
O \--\> V\[Reviewer\]  
O \--\> P\[Publisher\]  
R \-- JSON(report)-\> O  
S \-- JSON(summary)-\> O  
V \-- JSON(findings)-\> O  
P \-- status-\> O

### **JSON Handoff Schema (core)**

{  
"task\_id": "uuid",  
"role": "researcher|synthesiser|reviewer|publisher",  
"inputs": {},  
"artifacts": \[ {"type": "md|csv|json", "path": "/tmp/..."} \],  
"evidence": \[ {"source": "string", "provenance": "string"} \],  
"status": "ok|needs\_review|blocked",  
"notes": "string"  
}

### **Custom Slash Command (`~/.claude_agents/commands/orchestrate.md`)**

\# /orchestrate – Multi‑Agent Orchestrator v1.0

\#\# inputs  
\- plan: json (roles, tasks, dependencies)  
\- max\_parallel: int (default 2\)

\#\# steps  
1\. Validate plan DAG; reject cycles.  
2\. Dispatch tasks to role agents with bounded concurrency.  
3\. Enforce JSON handoff schema; validate each response.  
4\. On failure, retry with exponential backoff and dead‑letter handoff.

### **Invocation Script (`scripts/orchestrate.sh`)**

\#\!/usr/bin/env bash  
set \-euo pipefail  
PLAN\_FILE=${1:?plan.json}  
claude run /orchestrate \--plan "$(cat "$PLAN\_FILE")" \--max-parallel 2

### **Prompt Adaptation Template**

ROLE: Orchestrator  
GOAL: Delegate precisely, enforce contracts, recover from partial failures  
OUTPUT: Execution ledger with start/stop, retries, artefacts, final summary

### **Fault‑Tolerant Patterns**

* **Sagas:** Break multi‑step work into compensating actions.  
* **Circuit breakers:** Trip on repeated role failures.  
* **Idempotent tasks:** Use content hashes to deduplicate.  
* **Dead‑letter queues:** Persist irrecoverable items for human review.

### **Risk & Control Matrix**

| Risk | Control |
| :---- | :---- |
| Contract drift | JSON schemas versioned; validation on every hop |
| Thundering herd | Concurrency caps; token budgets per role |

### **Ethical Considerations**

* Make responsibility lines explicit; attribute authorship and decisions.

### **Failure Modes & Recovery**

| Failure | Recovery |
| :---- | :---- |
| Role unresponsive | Reroute to backup; degrade gracefully |
| Partial success | Commit saga steps; compensate if needed |

---

## **Chapter 9: Patterns Summary – Cross‑Blueprint Principles**

**Human‑in‑the‑Loop:** Gate high‑impact actions; provide diff‑based approvals; surface confidence and evidence.

**Secure Tooling:** Run in Devcontainer; read‑only by default; short‑lived secrets; audited CLI wrappers; egress allow‑lists.

**Observability:** Structured logs; trace IDs; per‑command dashboards; cost meters; failure taxonomies.

**Resource Optimisation:** Model cascade (small→large); summarise early; reuse context via embeddings; cache retrieval; batch operations.

**Decision Tree (When to use multi‑agent?):**

* If tasks are independent and skill‑specific → multi‑agent.  
* If tasks are sequential with strong coupling → single agent with internal phases.  
* If failure isolation is paramount → multi‑agent with sagas.  
* If cost is tight → single agent \+ caching.

---

# **Part B: The Reference Manual – Technical Specifications**

Factual, dense, and scannable. Short, standalone subsections with tables.

## **Chapter 10: Core CLI Reference**

### **10.1 Command Summary**

| Command | Purpose | Key Flags | Outputs |
| :---- | :---- | :---- | :---- |
| `/doc` | Generate docs | `--path`, `--sections`, `--budget-aud` | Markdown files \+ trace JSON |
| `/watch` | File watcher | `--watch-path`, `--handlers` | JSON receipts |
| `/janitor` | Curate files | `--root`, `--dry-run`, `--archive` | Manifest \+ report |
| `/test` | Test generation | `--path`, `--framework` | Tests \+ coverage |
| `/secscan` | CI security | `--pr-number`, `--policies` | SARIF \+ PR notes |
| `/adapt` | Learn/optimise | `--task-name`, `--kpis` | PR with prompt/policy diffs |
| `/orchestrate` | Multi‑agent | `--plan`, `--max-parallel` | Execution ledger |

### **10.2 Exit Codes**

| Code | Meaning |
| :---- | :---- |
| 0 | Success |
| 10 | Validation error |
| 20 | Policy violation |
| 30 | Budget exceeded |
| 40 | Tool failure |

### **10.3 Logging Format (JSONL)**

| Field | Description |
| :---- | :---- |
| `ts` | ISO8601 timestamp |
| `cmd` | Command name |
| `args` | Sanitised arguments |
| `cost_aud` | Monetary estimate |
| `tokens_in/out` | Token use |
| `trace_id` | Correlates steps |

## **Chapter 11: Tooling Reference**

### **11.1 Built‑in Tools (Gated)**

| Tool | Capability | Security Defaults |
| :---- | :---- | :---- |
| `fs.read` | Safe file read | Read‑only; allow‑list glob |
| `fs.write` | Write within `/tmp` | Path prefix check |
| `shell.exec` | Run deterministic command | No network; timeout; whitelist |
| `git` | PR creation | Read‑only clone; signed commits |

### **11.2 Retrieval Utilities**

| Utility | Description | Notes |
| :---- | :---- | :---- |
| `embed.index` | Build local embeddings index | Chunk size 512–1024 tokens |
| `embed.query` | Query index for top‑k | Use cosine; store provenance |

## **Chapter 12: Extensibility Reference**

### **12.1 Adding a New Slash Command**

| Step | Detail |
| :---- | :---- |
| 1 | Create `~/.claude_agents/commands/<name>.md` with intent, inputs, policies, steps |
| 2 | Add wrapper script under `scripts/` for audit |
| 3 | Register in `commands.index.json` |
| 4 | Write minimal tests in `tests/commands/<name>_test.py` |

### **12.2 Schema Versioning**

| Concept | Rule |
| :---- | :---- |
| Backward‑compatible | Minor version bump |
| Breaking change | Major bump; migration notes |

## **Chapter 13: Configuration Reference**

### **13.1 Policy Files**

| File | Purpose |
| :---- | :---- |
| `common.policies.md` | Global deny/allow lists; content policy preamble |
| `canon.md` | Canonical style, tone, and evidence rules |

### **13.2 Budgets & Limits**

| Setting | Default | Description |
| :---- | :---- | :---- |
| `budget_aud` | 5.00 | Hard monetary cap per run |
| `max_tokens` | 6000 | Max model tokens per run |
| `max_parallel` | 2 | Orchestrator parallelism cap |

---

# **Appendices**

## **Appendix A: Core Agent Design Principles**

### **A.1 Scalability Heuristics: Multi‑Agent vs Single‑Agent**

* Prefer multi‑agent when responsibilities are separable and failure isolation is critical.  
* Prefer single‑agent when context sharing dominates and latency/cost are primary.

### **A.2 Observability Patterns**

* Correlate all runs with `trace_id`.  
* Emit structured metrics: latency, success rate, token cost.  
* Store artefacts with content hashes.

### **A.3 Evaluating Autonomy & Alignment**

* Classify actions as **read**, **propose**, **commit**; only **commit** requires human approval.  
* Maintain alignment cards: purpose, bounds, escalation paths.

## **Appendix B: Interoperability with Other Frameworks**

### **B.1 Patterns for Integrating with LangChain**

* Wrap slash commands as LangChain tools; preserve policy preambles; ensure schema validation at boundaries.

### **B.2 Calling Claude Code Agents from AutoGPT**

* Expose commands via HTTP façade with JSON in/out; rate‑limit; token budgets per caller.

## **Appendix C: Agent Simulation Toolkit**

**Goal:** Test multi‑agent plans locally without live tools.

**Pseudocode**

def simulate(plan, agents):  
state \= {"trace": \[\]}  
for task in topological\_sort(plan):  
agent \= agents\[task.role\]  
result \= agent.mock(task.inputs)  
assert validate(result, HANDOFF\_SCHEMA)  
state\[task.id\] \= result  
state\["trace"\].append({"task": task.id, "status": result\["status"\]})  
return state

## **Appendix D: Further Reading & Official Resources (Inline Summaries)**

* **Claude Code principles:** policy‑first, tool‑gated execution, deterministic contracts, containerised environments, human escalation points.  
* **Prompt engineering essentials:** role clarity, structured outputs, verification prompts, and explicit failure handling.  
* **Safety doctrine:** treat external inputs as untrusted; sanitise, validate, and isolate.

## **Appendix E: Contributions Guide**

**Scope:** Blueprints, patterns, commands, and policies.

**Process:**

1. Fork private repo; create feature branch.  
2. Include blueprint sections: objective, case study, diagram, command, script, template, risk matrix, ethics, failures.  
3. Add tests and example artefacts.  
4. Submit PR with signed commits and a change log entry.  
5. Maintainers review for security, determinism, and clarity.

**Style:** Australian English; concise, evidence‑forward; no external links; self‑contained examples.

**Licensing & Attribution:** Respect code ownership and internal policies; include provenance notes in all generated artefacts.

