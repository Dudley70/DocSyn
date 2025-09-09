---
source: "Claude Code Documentation"
retrieved: 2025-09-09
owner: "development-team"
tags: [core, integration, patterns]
part: A
order: 50
slug: claude-patterns
---

\# Claude Code: Agent Blueprints, Patterns & Reference Manual

\#\# Version History  
\- \*\*1.0 (7 September 2025):\*\* Initial synthesis of canonical blueprints, reference materials, and implementation details from core sources. Incorporates foundational risks, practical deployments, and enterprise patterns for responsible agentic development.

\#\# Introduction: A Framework for Responsible Agentic Development  
This master guide is the definitive, self-contained resource for building, deploying, and managing agentic systems using Claude Code. It synthesises high-level architectural principles, practical blueprints, and implementation details into a unified structure, optimised for both human practitioners and AI assistants like Gemini Gems. While focused on Claude Code, the patterns—modularity, fault tolerance, secure orchestration, and human-in-the-loop governance—are transferable to other frameworks.

Claude Code represents a paradigm shift in AI-assisted development: a terminal-based agentic framework that acts as an autonomous partner, maintaining persistent context and using tools to execute tasks. Unlike IDE copilots (reactive suggestions) or chat interfaces (ephemeral), it enables continuous, context-rich workflows for exploration, planning, and action. Key tenets: security-by-design, observability, and ethical alignment to mitigate risks like unintended actions or data leakage.

\#\#\# High-Level Risk & Control Overview  
This framework applies a proactive, multi-layered security model organised into four pillars: Governance, Environment, Data, and Operations. These pillars ensure agents are accountable, observable, and bounded, addressing risks across the lifecycle.

| Pillar | Risk Category | Description | Potential Impact | Canonical Control | Relevant Blueprint(s) |  
|--------|---------------|-------------|------------------|-------------------|-----------------------|  
| \*\*Governance\*\* | Excessive Agency & Unintended Actions | Agent exceeds scope due to ambiguous prompts or flawed reasoning. | Operational outages; financial loss. | Least privilege; HITL for destructive ops; command blocklists (e.g., deny \`rm \*\`). | All; esp. Multi-Agent Orchestrator. |  
| \*\*Governance\*\* | Disinformation/Manipulation | Generation of false content or phishing. | Reputational damage. | Content filtering; anomaly detection; HITL for public outputs. | N/A (misuse risk; controls in others). |  
| \*\*Environment\*\* | Supply Chain Vulnerabilities | Compromised dependencies or models. | System compromise. | Verified images; dependency scanning; isolated environments (e.g., Docker). | CI/CD Security Analyst. |  
| \*\*Data\*\* | Data Leakage & Privacy Violation | Exposure of PII or sensitive data in outputs/logs. | Fines; trust erosion. | Input sanitisation; encrypted credentials; restricted retention. | Automated Documenter; CI/CD Analyst. |  
| \*\*Operations\*\* | Lack of Traceability | Opaque decisions hinder audits. | Compliance failures. | Immutable logs; distributed tracing; JSONL formatting. | Adaptive Learning Agent; Multi-Agent Orchestrator. |  
| \*\*Operations\*\* | Financial Fraud | Erroneous transactions from hallucinations. | Monetary loss. | HITL gates; RBAC on APIs; transaction anomaly checks. | N/A (specialised; principles in Janitor/Orchestrator). |

\#\#\# Agent Query Index  
| Question | Section | Keywords for Semantic Search |  
|----------|---------|------------------------------|  
| “Secure dev setup?” | Ch.1 | Devcontainer, Docker isolation, permissions. |  
| “Automated documenter?” | Ch.2 | Blueprint, success criteria, risk matrix. |  
| “File-watcher guardian?” | Ch.3 | Notification logic, cooldown. |  
| “Janitor file-management?” | Ch.4 | Human-in-loop, plan review. |  
| “Automated tester?” | Ch.5 | Test-on-save, property-based. |  
| “CI/CD security analyst?” | Ch.6 | GitHub .yml, risk matrix. |  
| “Adaptive learning agent?” | Ch.7 | Feedback loops, self-improvement. |  
| “Multi-agent orchestrator?” | Ch.8 | Handoffs, fault tolerance. |  
| “Patterns summary?” | Ch.9 | Decision trees, heuristics. |  
| “CLI/tools reference?” | Ch.10-13 | Flags, syntax, secure patterns. |

\# Part A: Agent Blueprints & Patterns

\#\# Chapter 1: The Standard Development Environment

\*\*Chapter Primer\*\*    
\*Synopsis:\* This chapter establishes the baseline architecture for secure and consistent agentic development using Devcontainers, providing the foundational environment for all subsequent blueprints.    
\*Key Concepts:\* Devcontainer isolation, reproducibility, least-privilege security, dependency management, centralised configuration.    
\*For the Beginner:\* Learn the simple steps to set up a safe, consistent workspace that protects your system while enabling agentic tools.    
\*For the Expert:\* Understand the architectural rationale for Devcontainers as the canonical security model, including advanced troubleshooting and integration patterns for enterprise-scale deployments.

\#\#\# 1.1 The Recommended Architecture: Why We Use Devcontainers  
Devcontainers are the canonical approach for security and consistency, providing isolated, reproducible environments with non-root execution and controlled dependencies. Why: They eliminate "works on my machine" issues by enforcing immutable bases and pinned versions, harden supply chains against vulnerabilities (e.g., via SBOM generation), and enable least-privilege principles by mounting projects read-only with writable temps. This prevents unintended file access or environmental drift, crucial for agentic systems where autonomy could amplify errors. Alternatives like native installs are for niche cases but lack built-in isolation, increasing risks of tool misuse or data leakage in production workflows.

\#\#\# 1.2 Setting Up Your First Devcontainer for Claude Code  
\`\`\`json  
// .devcontainer/devcontainer.json  
{  
  "name": "Claude Code Dev",  
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",  
  "features": {"node": "lts"},  
  "postCreateCommand": "npm install \-g @anthropic-ai/claude-code",  
  "customizations": {"vscode": {"extensions": \["anthropic.claude-code"\]}}  
}  
\`\`\`  
Build with VS Code Dev Containers extension. Why this setup: Ensures consistent tooling; post-command installs Claude Code securely, while features pin dependencies to avoid drift.

\#\#\# 1.3 Creating a Centralised, Version-Controlled Agent Configuration (\`\~/.claude\_agents\`)  
Create \`\~/.claude\_agents\` for commands/hooks; git init for versioning. Why: Enables traceability and collaboration—commit changes to configs like CLAUDE.md for auditability and rollback, essential for team environments where agent behaviours evolve.

\#\#\# 1.4 Troubleshooting Common Devcontainer Issues  
Issues: Docker compatibility—ensure Desktop installed. Solutions: For auth errors, use host borrowing; for permissions, \`--allowedTools\`. Why troubleshooting matters: Maintains operational reliability in agentic setups, where failures could cascade.

\#\# Chapter 2: Blueprint: The Automated Documenter Agent

\*\*Chapter Primer\*\*    
\*Synopsis:\* This chapter details a blueprint for an agent that automatically generates and maintains project documentation, encapsulating code analysis and Markdown formatting logic.    
\*Key Concepts:\* Context gathering, custom slash commands, output sanitisation, documentation coverage metrics.    
\*For the Beginner:\* Discover how to create an agent that turns code into readable docs without manual effort.    
\*For the Expert:\* Explore patterns for robust context provision and integration with CI/CD for continuous documentation.

\*\*Objective & Success Criteria:\*\* Generate comprehensive, accurate documentation for codebases, achieving 95% coverage of functions/classes, measurable via output completeness and user verification.    
\*\*Real-World Case Study:\*\* In a software team, auto-generate README updates on commits, reducing manual doc time by 80%.    
\*\*Agent Workflow Diagram:\*\*    
\`\`\`mermaid  
graph TD  
A\[Invoke Script\] \--\> B\[Gather Context: Files/Deps\]  
B \--\> C\[Invoke /documenter with Context\]  
C \--\> D\[Format into Markdown\]  
D \--\> E\[Output & Review\]  
\`\`\`  
\*\*Custom Slash Command (.md):\*\*    
\`\`\`  
\---  
name: "/documenter"  
intent: "Formats provided project context into a professional Markdown report."  
\---  
You are an expert technical writer. Using ONLY the context provided below, generate a comprehensive Markdown documentation file.

\*\*RULES:\*\*  
1\. Structure as: Overview, Structure, Dependencies, Key Components.  
2\. Use relative paths (e.g., src/file.js).  
3\. Be concise yet complete; avoid hallucinations.

\#\# Project Structure  
\`\`\`  
${args\[0\]}  
\`\`\`

\#\# Key Dependencies  
\`\`\`json  
${args\[1\]}  
\`\`\`  
\`\`\`  
\*\*Invocation Script (.sh):\*\*    
\`\`\`bash  
\#\!/bin/bash  
set \-e  \# Exit on error

PROJECT\_PATH="${1:-.}"  \# Default to current dir  
echo "Gathering context for ${PROJECT\_PATH}..."

\# Pre-flight checks  
if \[ \! \-d "$PROJECT\_PATH" \]; then  
  echo "Error: Directory not found: $PROJECT\_PATH"  
  exit 1  
fi

\# Gather context robustly  
PROJECT\_TREE=$(tree \-L 2 \-I 'node\_modules|dist' "$PROJECT\_PATH" 2\>/dev/null || echo "tree not installed; fallback listing: $(ls \-R "$PROJECT\_PATH")")  
PROJECT\_DEPS=$(jq '{dependencies, devDependencies}' "${PROJECT\_PATH}/package.json" 2\>/dev/null || echo "No package.json found.")

\# Sanitize for sensitive data (example: mask API keys if present)  
PROJECT\_DEPS=$(echo "$PROJECT\_DEPS" | sed 's/"sk-\[a-zA-Z0-9\]\*"/"REDACTED"/g')

echo "Invoking agent..."

\# Pass to custom command  
claude /documenter "${PROJECT\_TREE}" "${PROJECT\_DEPS}" \> "${PROJECT\_PATH}/DOCS.md"

\# Log invocation  
echo "\[$(date)\] Documentation generated for ${PROJECT\_PATH}" \>\> \~/.claude\_agents/logs/documenter.log

echo "✅ Documentation at ${PROJECT\_PATH}/DOCS.md"  
\`\`\`  
\*\*Prompt Adaptation Template:\*\* "You are a documenter agent. Given \[context: files/deps\], generate \[sections: overview, usage\]: 1\. Analyze structure..."    
\*\*Risk & Control Matrix:\*\*    
| Risk | Impact | Control | Residual Risk |    
|------|--------|---------|---------------|    
| Inaccurate Docs | Medium | Explicit context provision; HITL review | Low |    
| Data Leakage | High | Pre-script sanitisation; restricted outputs | Low |    
| Hallucination | Medium | Grounding in provided data only | Low |    
\*\*Ethical Considerations & Audit Logging:\*\* Check for bias in summaries; log invocations with timestamps for traceability.    
\*\*Failure Modes & Recovery:\*\* Incomplete context—retry with expanded gathering; errors—fallback to manual review.

\#\# Chapter 3: Blueprint: The Guardian File-Watcher Agent

\*\*Chapter Primer\*\*    
\*Synopsis:\* This chapter provides a blueprint for a persistent, long-running agent that serves as an active monitor for filesystem events. It acts as a trigger for automated workflows, initiating actions in real-time as files are created, modified, or deleted. This pattern is fundamental for building event-driven automation.    
\*Key Concepts:\* Filesystem watcher (fswatch), persistent agent, event-driven trigger, cooldown logic, daemonisation.    
\*For the Beginner:\* Learn how to create a simple "bot" that can watch a folder (like your Downloads folder) and automatically react when a new file appears.    
\*For the Expert:\* Master the patterns for creating reliable, long-running agentic services, including robust error handling, process management (PID files), and avoiding race conditions with cooldowns.

\*\*Objective & Success Criteria:\*\* Monitor a folder for changes, notify with cooldown to avoid spam, achieving 99.9% detection with \<5% false positives.    
\*\*Real-World Case Study:\*\* A data science team uses the Guardian to watch an S3-mounted directory. When a new CSV dataset arrives, the agent automatically triggers a data validation and ingestion pipeline, logging the results and alerting the team on Slack.    
\*\*Agent Workflow Diagram:\*\*    
\`\`\`mermaid  
graph TD  
A\[File Change Event\] \--\> B{Cooldown Active?};  
B \-- No \--\> C\[Invoke /watcher command\];  
B \-- Yes \--\> D\[Ignore Event\];  
C \--\> E\[Generate Notification Text\];  
E \--\> F\[Log and Send Alert\];  
\`\`\`  
\*\*Custom Slash Command (.md):\*\*    
\`\`\`  
\---  
name: "/watcher"  
intent: "Given details of a file system event, generate a concise, human-readable notification."  
\---  
You are a File System Guardian. Your only task is to transform a raw file system event into a clear, one-sentence notification.

\*\*RULES:\*\*  
1\.  Be concise. Do not add conversational filler.  
2\.  State the file name and the action that occurred.  
3\.  If given \`ls \-l\` output, include the file size.

\*\*EXAMPLE INPUT:\*\*  
\`Mon Sep 8 10:30:01 2025 /Users/dev/project/src/api.js\`  
\`-rw-r--r-- 1 dev staff 4096 Sep 8 10:30 /Users/dev/project/src/api.js\`

\*\*EXAMPLE OUTPUT:\*\*  
\`File modified: src/api.js (4.1 KB)\`  
\`\`\`  
\*\*Invocation Script (.sh):\*\*    
\`\`\`bash  
\#\!/bin/bash  
set \-e \# Exit on error

\# \--- Configuration \---  
WATCH\_PATH="$1"  
LOG\_FILE="$HOME/.claude\_agents/logs/guardian.log"  
COOLDOWN\_SECONDS=10 \# Ignore rapid-fire changes  
LAST\_EVENT\_TIME=0

\# \--- Pre-flight Checks \---  
if \[ \-z "$WATCH\_PATH" \]; then  
    echo "Usage: $0 /path/to/watch"  
    exit 1  
fi  
if \[ \! \-d "$WATCH\_PATH" \]; then  
    echo "Error: Directory not found at ${WATCH\_PATH}"  
    exit 1  
fi

echo "\[$(date)\] Guardian Agent started. Watching: ${WATCH\_PATH}" | tee \-a "${LOG\_FILE}"

\# \--- Main Loop \---  
fswatch \-o "$WATCH\_PATH" | while read \-r file\_path; do  
    CURRENT\_TIME=$(date \+%s)  
    if (( CURRENT\_TIME \- LAST\_EVENT\_TIME \< COOLDOWN\_SECONDS )); then  
        continue \# Skip if within cooldown period  
    fi  
    LAST\_EVENT\_TIME=$CURRENT\_TIME

    echo "\[$(date)\] Event detected for file: ${file\_path}" \>\> "${LOG\_FILE}"

    \# Explicitly gather context for the agent  
    EVENT\_DETAILS=$(ls \-l "$file\_path")

    \# Invoke agent to generate the notification message  
    NOTIFICATION=$(claude /watcher "${EVENT\_DETAILS}")

    \# Log and send the notification (macOS example)  
    echo "  \- Notification: ${NOTIFICATION}" \>\> "${LOG\_FILE}"  
    osascript \-e "display notification \\"${NOTIFICATION}\\" with title \\"Guardian Alert\\""  
done  
\`\`\`  
\*\*Prompt Adaptation Template:\*\* "You are a watcher agent. Given \[change\], notify: 1\. Describe impact..."    
\*\*Risk & Control Matrix:\*\*    
| Risk | Impact | Control | Residual Risk |    
|------|--------|---------|---------------|    
| Spam Alerts | Low | Cooldown logic | Low |    
| Missed Changes | High | Robust fswatch | Low |    
| Privacy Breach | Medium | Sanitise logs | Low |    
\*\*Ethical Considerations & Audit Logging:\*\* Ensure notifications don't expose sensitive data; log all detections.    
\*\*Failure Modes & Recovery:\*\* Watch failure—restart script; false positives—refine matcher.

\#\# Chapter 4: Blueprint: The Janitor File-Management Agent

\*\*Chapter Primer\*\*    
\*Synopsis:\* This chapter outlines a blueprint for an agent that intelligently manages and organises files, emphasising safe, reviewable plans to automate cleanup without risking data loss.    
\*Key Concepts:\* Human-in-the-loop review, dry-run simulation, file categorisation, archive management.    
\*For the Beginner:\* Build an agent to tidy your folders automatically, with safety nets to learn core agentic principles.    
\*For the Expert:\* Implement advanced patterns for scalable file orchestration, including integration with storage systems and audit trails.

\*\*Objective & Success Criteria:\*\* Propose and execute file management plans with 100% human approval rate, reducing clutter by 70% without data loss.    
\*\*Real-World Case Study:\*\* A content team uses Janitor to archive old assets, freeing space while maintaining access logs.    
\*\*Agent Workflow Diagram:\*\*    
\`\`\`mermaid  
graph TD  
A\[Invoke Script\] \--\> B\[Gather File List\]  
B \--\> C\[Invoke /janitor for Plan\]  
C \--\> D\[Human Review Plan\]  
D \--\> E\[Execute Approved Actions\]  
\`\`\`  
\*\*Custom Slash Command (.md):\*\*    
\`\`\`  
\---  
name: "/janitor"  
intent: "Generate a safe, reviewable file management plan from provided file list."  
\---  
You are a File Janitor. Given a list of files, create a detailed, executable bash script plan for categorisation, archival, or deletion.

\*\*RULES:\*\*  
1\. Never suggest destructive actions without dry-run flags.  
2\. Categorise: e.g., images to /archive/images.  
3\. Output as bash script with comments.

\#\# File List  
\`\`\`  
${args\[0\]}  
\`\`\`  
\`\`\`  
\*\*Invocation Script (.sh):\*\*    
\`\`\`bash  
\#\!/bin/bash  
set \-e

ROOT\_PATH="${1:-\~/Downloads}"  
PLAN\_FILE="janitor\_plan.sh"

echo "Scanning ${ROOT\_PATH}..."

\# Gather files safely  
FILE\_LIST=$(find "$ROOT\_PATH" \-type f \-maxdepth 1 2\>/dev/null || echo "No files found.")

\# Invoke agent for plan  
claude /janitor "${FILE\_LIST}" \> "${PLAN\_FILE}"

\# Human review  
cat "${PLAN\_FILE}"  
read \-p "Approve plan? (y/n): " APPROVE  
if \[ "$APPROVE" \!= "y" \]; then  
  echo "Plan aborted."  
  exit 0  
fi

\# Execute if approved  
bash "${PLAN\_FILE}"

\# Log  
echo "\[$(date)\] Janitor executed on ${ROOT\_PATH}" \>\> \~/.claude\_agents/logs/janitor.log  
\`\`\`  
\*\*Prompt Adaptation Template:\*\* "You are a janitor agent. Given \[files\], plan: 1\. Categorise..."    
\*\*Risk & Control Matrix:\*\*    
| Risk | Impact | Control | Residual Risk |    
|------|--------|---------|---------------|    
| Data Loss | High | Dry-run/HITL approval | Low |    
| Privacy | Medium | Restricted scanning | Low |    
| Inefficiency | Low | Maxdepth limits | Low |    
\*\*Ethical Considerations & Audit Logging:\*\* Avoid bias in categorisation; log all plans/executions.    
\*\*Failure Modes & Recovery:\*\* Scan errors—fallback listing; unapproved—abort.

\#\# Chapter 5: Blueprint: The Automated Tester Agent

\*\*Chapter Primer\*\*    
\*Synopsis:\* This chapter presents a blueprint for an agent that automates testing workflows, integrating with save events for continuous validation.    
\*Key Concepts:\* Test-on-save, property-based testing, coverage metrics, integration hooks.    
\*For the Beginner:\* Create an agent to run tests automatically, learning basic quality assurance.    
\*For the Expert:\* Leverage advanced techniques like Hypothesis for robust, scalable testing in CI/CD.

\*\*Objective & Success Criteria:\*\* Execute tests on saves with 95% coverage, detecting 99% of regressions.    
\*\*Real-World Case Study:\*\* DevOps team auto-tests PRs, reducing bugs by 60%.    
\*\*Agent Workflow Diagram:\*\*    
\`\`\`mermaid  
graph TD  
A\[Save Event\] \--\> B\[Run Tests & Capture Output\]  
B \--\> C\[Invoke /tester with Output\]  
C \--\> D\[Generate Report\]  
D \--\> E\[Notify on Failures\]  
\`\`\`  
\*\*Custom Slash Command (.md):\*\*    
\`\`\`  
\---  
name: "/tester"  
intent: "Summarise test output and generate coverage report."  
\---  
You are a Tester Agent. Given captured test output, create a summary report.

\*\*RULES:\*\*  
1\. Include pass/fail counts, coverage %.  
2\. Highlight failures with snippets.  
3\. Suggest fixes if errors.

\#\# Test Output  
${args\[0\]}  
\`\`\`  
\*\*Invocation Script (.sh):\*\*    
\`\`\`bash  
\#\!/bin/bash  
set \-e

TEST\_PATH="${1:-.}"

echo "Testing ${TEST\_PATH}..."

\# Detect framework  
FRAMEWORK=$(grep \-q "jest" package.json && echo "npm test" || echo "pytest")

\# Run tests and capture output  
TEST\_OUTPUT=$($FRAMEWORK 2\>&1 || true)  \# Capture even on fail

echo "Invoking agent..."

\# Pass to agent for summary  
claude /tester "${TEST\_OUTPUT}" \> test\_report.log

\# Notify on failures  
if grep \-q "FAIL" test\_report.log; then  
  osascript \-e 'display notification "Tests Failed" with title "Tester Alert"'  
fi

\# Log  
echo "\[$(date)\] Tests run on ${TEST\_PATH}" \>\> \~/.claude\_agents/logs/tester.log  
\`\`\`  
\*\*Prompt Adaptation Template:\*\* "You are a tester agent. Given \[output\], summarise: 1\. Counts/coverage..."    
\*\*Risk & Control Matrix:\*\*    
| Risk | Impact | Control | Residual Risk |    
|------|--------|---------|---------------|    
| Side Effects | High | Containerised runs | Low |    
| False Negatives | Medium | Property-based adds | Low |    
| Resource Use | Low | Timeouts | Low |    
\*\*Ethical Considerations & Audit Logging:\*\* Ensure tests cover bias cases; log results.    
\*\*Failure Modes & Recovery:\*\* Test failures—retry; framework missing—fallback.

\#\# Chapter 6: Blueprint: The CI/CD Security Analyst

\*\*Chapter Primer\*\*    
\*Synopsis:\* This chapter details a blueprint for an agent that analyses CI/CD pipelines for security vulnerabilities, integrating with GitHub Actions.    
\*Key Concepts:\* Workflow .yml, SARIF reports, policy checks, PR integration.    
\*For the Beginner:\* Learn to secure automated builds with an agentic reviewer.    
\*For the Expert:\* Implement enterprise-grade scanning with custom policies and anomaly detection.

\*\*Objective & Success Criteria:\*\* Scan pipelines for risks, achieving 100% policy compliance.    
\*\*Real-World Case Study:\*\* DevSecOps team auto-reviews PRs, blocking 90% of vulns.    
\*\*Agent Workflow Diagram:\*\*    
\`\`\`mermaid  
graph TD  
A\[PR Event\] \--\> B\[Invoke /secscan\]  
B \--\> C\[Analyse .yml\]  
C \--\> D\[Generate SARIF\]  
D \--\> E\[Post PR Comments\]  
\`\`\`  
\*\*Custom Slash Command (.md):\*\*    
\`\`\`  
\---  
name: "/secscan"  
intent: "Analyse CI/CD workflow for security risks."  
\---  
You are a Security Analyst. Given .yml content, check policies and create SARIF report.

\*\*RULES:\*\*  
1\. Scan for secrets, untrusted actions.  
2\. Output as JSON SARIF format.

\#\# Workflow  
${args\[0\]}  
\`\`\`  
\*\*Invocation Script (.sh):\*\*    
\`\`\`bash  
\#\!/bin/bash  
set \-e

PR\_NUMBER="$1"  
YML\_PATH=".github/workflows/ci.yml"

\# Gather workflow  
WORKFLOW=$(cat "$YML\_PATH")

\# Invoke  
claude /secscan "${WORKFLOW}" \> sec\_report.sarif

\# Post to PR (GitHub CLI)  
gh pr comment "$PR\_NUMBER" \--body-file sec\_report.sarif

\# Log  
echo "\[$(date)\] Scanned PR $PR\_NUMBER" \>\> \~/.claude\_agents/logs/secscan.log  
\`\`\`  
\`\`\`yaml  
\# .github/workflows/ci.yml example  
name: CI  
on: \[push\]  
jobs:  
  build:  
    runs-on: ubuntu-latest  
    steps:  
      \- uses: actions/checkout@v3  
      \- run: npm test  
\`\`\`  
\*\*Prompt Adaptation Template:\*\* "You are a security analyst. Given \[.yml\], scan: 1\. Check policies..."    
\*\*Risk & Control Matrix:\*\*    
| Risk | Impact | Control | Residual Risk |    
|------|--------|---------|---------------|    
| Vuln Miss | High | Policy preambles | Low |    
| False Positives | Medium | Anomaly tuning | Low |    
| Integration Fail | Low | Error handling | Low |    
\*\*Ethical Considerations & Audit Logging:\*\* Flag compliance issues; log scans.    
\*\*Failure Modes & Recovery:\*\* Parse errors—fallback scan; no PR—manual report.

\#\# Chapter 7: Blueprint: The Adaptive Learning Agent

\*\*Chapter Primer\*\*    
\*Synopsis:\* This chapter blueprints an agent that self-improves through feedback, adapting prompts and behaviours for efficiency.    
\*Key Concepts:\* Feedback loops, RL-like optimisation, prompt diffs, learning propagation.    
\*For the Beginner:\* Build an agent that gets smarter over time from your input.    
\*For the Expert:\* Implement self-optimising systems with monitoring and ethical safeguards.

\*\*Objective & Success Criteria:\*\* Improve task KPIs (e.g., accuracy \+20%) via loops.    
\*\*Real-World Case Study:\*\* ML team adapts agent for better model tuning.    
\*\*Agent Workflow Diagram:\*\*    
\`\`\`mermaid  
graph TD  
A\[Task Outcome\] \--\> B\[Analyse Success\]  
B \--\> C\[Invoke /adapt\]  
C \--\> D\[Update Config/PR\]  
D \--\> E\[Propagate Learnings\]  
\`\`\`  
\*\*Custom Slash Command (.md):\*\*    
\`\`\`  
\---  
name: "/adapt"  
intent: "Analyse outcome and generate config updates."  
\---  
You are an Adaptive Learner. Given outcome, extract patterns and suggest diffs.

\*\*RULES:\*\*  
1\. Focus on prompt/behaviour improvements.  
2\. Output as git diff format.

\#\# Outcome  
${args\[0\]}  
\`\`\`  
\*\*Invocation Script (.sh):\*\*    
\`\`\`bash  
\#\!/bin/bash  
set \-e

TASK\_OUTCOME="$1"

\# Gather metrics  
METRICS=$(echo "$TASK\_OUTCOME" | jq '.metrics' || echo "No metrics.")

\# Invoke  
claude /adapt "${TASK\_OUTCOME}" \> adapt\_diff.patch

\# Apply if approved  
git apply adapt\_diff.patch

\# Log/PR  
echo "\[$(date)\] Adapted from outcome" \>\> \~/.claude\_agents/logs/adapt.log  
gh pr create \--title "Agent Adaptation" \--body-file adapt\_diff.patch  
\`\`\`  
\*\*Prompt Adaptation Template:\*\* "You are an adaptive agent. Given \[outcome\], optimise: 1\. Extract patterns..."    
\*\*Risk & Control Matrix:\*\*    
| Risk | Impact | Control | Residual Risk |    
|------|--------|---------|---------------|    
| Overfitting | Medium | Metric validation | Low |    
| Ethical Drift | High | Bias checks | Low |    
| Instability | Low | Versioned diffs | Low |    
\*\*Ethical Considerations & Audit Logging:\*\* Monitor for bias amplification; log adaptations.    
\*\*Failure Modes & Recovery:\*\* Poor outcomes—revert diff; no metrics—manual input.

\#\# Chapter 8: Blueprint: The Collaborative Multi-Agent Orchestrator

\*\*Chapter Primer\*\*    
\*Synopsis:\* This chapter blueprints an orchestrator for coordinating multiple sub-agents, enabling complex workflows through delegation and consensus.    
\*Key Concepts:\* Agent handoffs, parallelism caps, fault-tolerant sagas, swarm patterns.    
\*For the Beginner:\* Learn to build a "team" of agents for bigger tasks.    
\*For the Expert:\* Master distributed execution with monitoring and recovery for scalable systems.

\*\*Objective & Success Criteria:\*\* Orchestrate agents with 99% success, handling failures gracefully.    
\*\*Real-World Case Study:\*\* Research team orchestrates sub-agents for data pipeline.    
\*\*Agent Workflow Diagram:\*\*    
\`\`\`mermaid  
graph TD  
A\[Plan\] \--\> B\[Spawn Sub-Agents\]  
B \--\> C\[Parallel Execution\]  
C \--\> D\[Consensus/Handoff\]  
D \--\> E\[Aggregate Results\]  
\`\`\`  
\*\*Custom Slash Command (.md):\*\*    
\`\`\`  
\---  
name: "/orchestrate"  
intent: "Coordinate sub-agents for a multi-step plan."  
\---  
You are an Orchestrator. Given a plan, coordinate sub-agents.

\*\*RULES:\*\*  
1\. Use JSON for handoffs.  
2\. Limit parallelism to ${args\[1\]}.

\#\# Plan  
${args\[0\]}  
\`\`\`  
\*\*Invocation Script (.sh):\*\*    
\`\`\`bash  
\#\!/bin/bash  
set \-e

PLAN="$1"  
MAX\_PARALLEL="${2:-2}"

\# Gather sub-tasks  
SUB\_TASKS=$(echo "$PLAN" | jq '.tasks\[\]')

\# Invoke orchestrator  
claude /orchestrate "${PLAN}" "${MAX\_PARALLEL}" \> orchestrate.log

\# Execute in parallel (example with xargs)  
echo "$SUB\_TASKS" | xargs \-P "${MAX\_PARALLEL}" \-I {} claude /sub "{}"

\# Note: For production, replace xargs with robust queue like Redis/Celery for state/retries.

\# Log  
echo "\[$(date)\] Orchestrated plan" \>\> \~/.claude\_agents/logs/orchestrate.log  
\`\`\`  
\*\*Prompt Adaptation Template:\*\* "You are an orchestrator. Given \[plan\], coordinate: 1\. Spawn subs..."    
\*\*Risk & Control Matrix:\*\*    
| Risk | Impact | Control | Residual Risk |    
|------|--------|---------|---------------|    
| Deadlocks | High | Saga compensations | Low |    
| Overload | Medium | Parallel caps | Low |    
| Miscommunication | Medium | JSON schemas | Low |    
\*\*Ethical Considerations & Audit Logging:\*\* Ensure collective decisions align ethically; log handoffs.    
\*\*Failure Modes & Recovery:\*\* Sub-failure—retry with backoff; deadlock—timeout abort.

\#\# Chapter 9: Patterns Summary & Decision Trees  
Synthesise recurring advice: HITL trees, scalability heuristics (multi vs. single-agent).

\# Part B: The Reference Manual: Technical Specifications

\#\# Chapter 10: Core CLI Reference

\*\*Chapter Primer\*\*    
\*Synopsis:\* This chapter provides an exhaustive lookup for CLI commands and flags, serving as the quick-reference core for invocation patterns.    
\*Key Concepts:\* Flags, slash syntax, non-interactive modes.    
\*For the Beginner:\* Quickly find how to start and customise sessions.    
\*For the Expert:\* Detailed flags for advanced scripting and permissions.

\#\#\# 10.1 Invocation Commands & Flags  
Exhaustive list:  
| Flag | Purpose | Example Usage |  
|------|---------|---------------|  
| claude | Start REPL | claude |  
| claude "query" | Initial prompt | claude "explain codebase" |  
| claude \-p "query" | Non-interactive | claude \-p "fix lint" |  
| \--model | Select model | \--model opus |  
| \--allowedTools | Tool gating | \--allowedTools "Bash(npm:\*)" |  
| \--disallowedTools | Block tools | \--disallowedTools "Bash(rm:\*)" |  
| \--add-dir | Multi-dir access | \--add-dir ../lib |  
| mcp | MCP config | claude mcp add github |  
| \-c | Continue session | claude \-c |  
| \-r \<id\> | Resume ID | claude \-r abc123 "continue" |  
| \--dangerously-skip-permissions | Bypass (container only) | \--dangerously-skip-permissions |

\#\#\# 10.2 Built-in Slash Commands  
| Command | Syntax | Purpose |  
|---------|--------|---------|  
| /init | /init | Initialise project |  
| /status | /status | Check state |  
| /test | /test \[path\] | Run tests |  
| /doc | /doc \--path | Generate docs |  
| /watch | /watch \--path | Watch files |  
| /janitor | /janitor \--root | Manage files |  
| /secscan | /secscan \--pr | Security scan |  
| /adapt | /adapt \--task | Optimise |  
| /orchestrate | /orchestrate \--plan | Multi-agent run |

\#\# Chapter 11: Tooling Reference

\*\*Chapter Primer\*\*    
\*Synopsis:\* This chapter catalogues built-in tools for file/system interactions, with secure usage patterns.    
\*Key Concepts:\* Tool schemas, gating, MCP servers.    
\*For the Beginner:\* Understand basic read/write/execute.    
\*For the Expert:\* Detailed schemas for custom integrations.

\#\#\# 11.1 File System Tools (\`Read\`, \`Write\`, \`Edit\`)  
\`Read\`: Input: {path: str}; Output: {text: str}; Secure: Allow-list globs.    
\`Write\`: Input: {path: str, content: str}; Output: {success: bool}; Secure: Prefix checks.    
\`Edit\`: Input: {path: str, changes: str}; Output: {diff: str}; Secure: Dry-run.

\#\#\# 11.2 Command Execution Tools (\`Bash\`) and Secure Usage Patterns  
Input: {cmd: str}; Output: {stdout: str, stderr: str, code: int}; Secure: No network; timeouts; whitelists.

\#\#\# 11.3 Model Context Protocol (MCP) Server Configuration  
Config: {mcp: {servers: \[{type: "github", key: env}\]}}}; Why: External context safely.

\#\# Chapter 12: Extensibility Reference

\*\*Chapter Primer\*\*    
\*Synopsis:\* This chapter details how to extend Claude Code with custom logic, hooks, and sub-agents.    
\*Key Concepts:\* Syntax, events, matchers, invocation patterns.    
\*For the Beginner:\* Add simple commands.    
\*For the Expert:\* Build complex hooks with env vars.

\#\#\# 12.1 Creating Custom Slash Commands (Syntax, Arguments, Frontmatter)  
.md with YAML frontmatter; Args: ${args\[0\]}; Example as above.

\#\#\# 12.2 Implementing Hooks (Events, Matchers, \`settings.json\` Syntax)  
Events/Matchers/Table:  
| Event | Description | Available Vars | Matcher Example |  
|-------|-------------|----------------|-----------------|  
| PreToolUse | Before tool exec | $CLAUDE\_TOOL, $CLAUDE\_ARGS | "Bash.\*" |  
| PostToolUse | After tool | $CLAUDE\_TOOL, $CLAUDE\_OUTPUT | "Write.\*" |  
| OnError | On failure | $CLAUDE\_ERROR, $CLAUDE\_TOOL | ".\*" |  
| Notification | On alerts | $CLAUDE\_MESSAGE | "change.\*" |  
| SessionStart | On start | $CLAUDE\_SESSION\_ID | N/A |  
| Stop | On end | $CLAUDE\_SESSION\_ID | N/A |  
settings.json: {hooks: \[{event: "PreToolUse", script: "logger.sh", matcher: ".\*"}\]}.

\#\#\# 12.3 Designing Sub-Agents (Definition File Syntax, Invocation Patterns)  
.md syntax like commands; Invocation: /agents run "sub-name" \[args\]; Patterns: JSON handoffs, max parallel.

\#\# Chapter 13: Configuration Reference

\*\*Chapter Primer\*\*    
\*Synopsis:\* This chapter provides the complete syntax for configuration files.    
\*Key Concepts:\* Hierarchy, key references.    
\*For the Beginner:\* Set basic rules.    
\*For the Expert:\* Fine-tune for enterprise.

\#\#\# 13.1 \`CLAUDE.md\` Hierarchy and Syntax (User, Project, and Directory-level)  
User: \~/.claude/CLAUDE.md (global rules); Project: ./CLAUDE.md (standards); Directory: ./CLAUDE.local.md (optional overrides for local tweaks). Syntax: \#\# Sections (e.g., \#\# Architecture: Microservices). Maintain "Context Hygiene" to avoid "Contextual Debt"—regularly refactor CLAUDE.md to prevent bloat/degradation in agent performance.

\#\#\# 13.2 \`settings.json\` Complete Key Reference  
| Key | Type | Description |  
|-----|------|-------------|  
| model | str | Default (opus/sonnet/haiku) |  
| allowedTools | arr | Whitelist (e.g., \["Bash(npm:\*)"\]) |  
| disallowedTools | arr | Blocklist |  
| hooks | obj | Event scripts |  
| mcp | obj | Servers \[{type, key}\] |  
| budget | num | Token cap |  
| max\_parallel | num | Orchestrator limit |  
| latency\_slo\_ms | num | Warning threshold |  
| log\_format | str | JSONL default |  
| sub\_agents | obj | Sub-agent defs \[{name, path}\] |  
| advanced\_logging | bool | Enable verbose |

\# Appendices

\#\# Appendix A: Principles of Cost and Performance Optimisation  
Understand model tiers: Flagship (complex reasoning); Balanced (general dev); High-speed (simple tasks). Use cases: Cascade for efficiency. Strategies: Caching, batching, monitoring. Disclaimer: Check official site for current details.

\#\# Appendix B: Measuring Agentic Value  
Pilot: Design with KPIs (cycle time). Metrics: Quality (bugs), efficiency (time). Present: ROI reports.

\#\# Appendix C: Interoperability with Other Frameworks  
LangChain: Wrap as tools with schemas. AutoGPT: HTTP with quotas.

\#\# Appendix D: Further Reading & Official Resources (Inline Summaries)  
From Anthropic: Use plan mode to reduce tokens; tools with JSON schemas.

\#\# Appendix E: Contributions Guide  
Fork; add blueprints with gold standard; PR with tests.

\#\# Appendix F: Enterprise Deployment Blueprint  
Phase 1: Pilot—select devs, monitor.    
Phase 2: Expansion—CI/CD, policies.    
Phase 3: Production—multi-agent, optimisation.  
