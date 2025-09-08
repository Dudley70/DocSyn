

### **Version History**

* **1.0 (7 September 2025):** Initial release of the canonical guide. This version establishes the foundational blueprints, reference materials, and the core Risk & Control Framework for responsible agentic development.

### **Introduction: A Framework for Responsible Agentic Development**

Welcome to the Claude Code manual, the canonical guide for practitioners building, deploying, and managing sophisticated agentic systems. This document is engineered to be the definitive source of truth for both human developers and AI assistants, providing a comprehensive framework grounded in disciplined engineering, security, and ethical principles.

The rise of agentic AI marks a significant paradigm shift in software development. These systems, capable of autonomous reasoning, planning, and tool use, offer unprecedented potential for automation and problem-solving. However, this power necessitates a commensurate level of responsibility. An agent with excessive or misaligned agency can introduce significant risks, from data leakage and financial loss to operational disruption.1 Therefore, this manual is not merely a collection of techniques; it is an architectural philosophy. It mandates a secure-by-design approach, where safety, observability, and human oversight are not afterthoughts but core, non-negotiable components of the development lifecycle.

The blueprints and patterns detailed herein are designed to be transferable. While the implementation specifics are tailored for the Claude Code environment, the underlying architectural principles—modularity, fault tolerance, secure orchestration, and human-in-the-loop governance—are universal. They represent a durable foundation for building trustworthy AI systems, regardless of the specific model or framework. This guide is your blueprint for harnessing the power of agentic AI responsibly, ensuring that innovation proceeds in lockstep with safety and control.

* **High-level Risk & Control Overview**

The Claude Code framework is built upon a proactive and multi-layered security model designed to mitigate the inherent risks of autonomous systems. A comprehensive governance structure is essential to ensure every agent is accountable, observable, and limited by design.3 This overview maps the primary risk categories to the framework's canonical controls, which are enforced across all blueprints.

| Risk Category | Description of Risk | Potential Impact (Operational, Reputational, Financial) | Canonical Control | Relevant Blueprint(s) |
| :---- | :---- | :---- | :---- | :---- |
| **Excessive Agency & Unintended Actions** | Agent performs actions beyond its intended scope due to ambiguous instructions, prompt injection, or flawed reasoning, potentially leading to system damage or data corruption.4 | **Operational:** System misconfiguration, service outages. **Financial:** Unauthorised transactions, resource waste. **Reputational:** Loss of trust in automated systems. | Devcontainer Isolation, Tool-Use Sandboxing, Principle of Least Privilege, Mandatory Human-in-the-Loop (HITL) for destructive commands. | All Blueprints, esp. Janitor, Multi-Agent Orchestrator. |
| **Data Leakage & Privacy Violation** | Agent inadvertently accesses, processes, or exposes sensitive, confidential, or personally identifiable information (PII) in its outputs or logs.1 | **Financial:** Regulatory fines (e.g., GDPR). **Reputational:** Breach of customer trust. **Operational:** Loss of intellectual property. | Strict Input/Output Sanitisation, Data Minimisation Principles, Encrypted Communication (TLS 1.3+), Role-Based Access Control (RBAC) for tools. | All Blueprints, esp. Automated Documenter, CI/CD Security Analyst. |
| **Supply Chain & Dependency Vulnerabilities** | Agent utilises compromised or vulnerable third-party libraries, models, or services, introducing a backdoor into the system.5 | **Operational:** System compromise, data exfiltration. **Financial:** Cost of remediation, potential for ransomware. **Reputational:** Damage to brand integrity. | Devcontainer Environment Sandboxing, Continuous Dependency Scanning (SAST/SCA), Use of Verified Base Images and Models. | All Blueprints, esp. CI/CD Security Analyst. |
| **Lack of Traceability & Accountability** | The agent's decision-making process is opaque ("black box"), making it impossible to audit actions, debug failures, or assign responsibility for errors.1 | **Operational:** Inability to perform root cause analysis. **Reputational:** Loss of trust. **Financial:** Compliance failures, legal liability. | Immutable, Centralised Audit Logging for all agent actions and tool calls; Structured (JSON) Logging; Distributed Tracing for multi-agent systems. | All Blueprints, esp. Multi-Agent Orchestrator, Adaptive Learning Agent. |
| **Disinformation & Manipulation** | Malicious actors exploit agents to autonomously generate and distribute false narratives, manipulate public opinion, or conduct sophisticated phishing attacks at scale.1 | **Reputational:** Severe brand damage if an agent is co-opted. **Financial:** Fraud. **Operational:** Social engineering attacks against employees. | Output Content Filtering, Anomaly Detection in content generation patterns, HITL review for public-facing content generation. | N/A (This is a risk of agent *misuse*, addressed by controls in other blueprints). |
| **Financial Fraud & Market Manipulation** | An agent with access to financial systems makes unauthorised or erroneous transactions due to hallucinations, compromise, or flawed logic.1 | **Financial:** Direct monetary loss, market instability. **Reputational:** Loss of investor and customer confidence. | Mandatory HITL Approval Gate for all financial transactions, Strict RBAC on financial APIs, Real-time Anomaly Detection on transaction patterns. | N/A (This is a specialised risk; principles are covered in Janitor and Orchestrator blueprints). |

* **Agent Query Index**

This index is designed to facilitate rapid, Retrieval-Augmented Generation (RAG) lookups by mapping common developer questions to the most relevant sections of this manual. It serves as a semantic bridge between user intent and the structured knowledge contained herein.

| Common Developer Question / Goal | Relevant Blueprint or Section | Keywords for Semantic Search |
| :---- | :---- | :---- |
| "How do I set up a secure and consistent environment for my agents?" | Chapter 1: The Standard Development Environment | devcontainer, docker, setup, environment, configuration, security, isolation, sandbox |
| "How do I build an agent that automatically writes documentation for my code?" | Chapter 2: The Automated Documenter | documentation, docstrings, code analysis, technical writing, markdown, sphinx, pydoc |
| "I need an agent to watch a folder and process new files as they arrive." | Chapter 3: The Guardian File-Watcher | file watcher, file integrity monitoring, FIM, directory monitoring, watchdog, real-time processing |
| "How can I create an agent to automatically clean up old log files or temporary data?" | Chapter 4: The Janitor File-Management | file cleanup, automated deletion, data retention, janitor, temporary files, archiving, log rotation |
| "How do I get an AI to write unit tests for my functions?" | Chapter 5: The Automated Tester | automated testing, unit tests, pytest, TDD, test generation, quality assurance, QA |
| "I want to integrate automated security scanning into my CI/CD pipeline." | Chapter 6: The CI/CD Security Analyst | DevSecOps, CI/CD security, SAST, DAST, vulnerability scanning, bandit, security analysis |
| "How can I build an agent that learns and improves from user feedback?" | Chapter 7: The Adaptive Learning Agent | self-improving, adaptive learning, RLHF, feedback loop, reward hacking, catastrophic forgetting |
| "How do I design a system where multiple agents work together on a complex task?" | Chapter 8: The Collaborative Multi-Agent Orchestrator | multi-agent, orchestration, supervisor, worker, delegation, collaboration, communication protocol |
| "What are the most important design patterns for building reliable agents?" | Chapter 9: Patterns Summary: Cross-Blueprint Principles | design patterns, best practices, human-in-the-loop, HITL, secure tooling, resource efficiency |
| "Where can I find a quick reference for the claude command-line tool?" | Chapter 10: Core CLI Reference | CLI, command line, reference, flags, commands, options |
| "What tools can my agents use out of the box?" | Chapter 11: Tooling Reference | tools, filesystem, shell, API, security scanner, python libraries |
| "How do I create my own custom tools for my agents to use?" | Chapter 12: Extensibility Reference | plugins, custom tools, extensibility, API, schema, developing tools |
| "Where can I find all the configuration options for this framework?" | Chapter 13: Configuration Reference | configuration, settings, devcontainer.json, config.yml |
| "When should I use a multi-agent system versus a powerful single agent?" | Appendix A.1: Scalability Heuristics | architecture, scalability, multi-agent vs single-agent, design choice |
| "How do I monitor and debug my agent systems in production?" | Appendix A.2: Observability Patterns for Agentic Systems | observability, monitoring, logging, metrics, tracing, debugging, production |

# **Part A: Agent Blueprints & Patterns: Practical Recipes**

## **Chapter 1: The Standard Development Environment**

The foundation of any robust and secure software system is its development environment. For agentic systems, this foundation is not merely a matter of convenience; it is the first and most critical security control. An inconsistent or insecure environment exposes the host system to risk, introduces difficult-to-diagnose bugs, and undermines collaboration. This chapter establishes the single, canonical architecture for all Claude Code development: the Devcontainer. Adherence to this standard is mandatory for all blueprints in this manual, as it enforces the core principles of isolation, consistency, and reproducibility from the very first line of code.

### **1.1 The Recommended Architecture: Why We Use Devcontainers**

The choice of a development environment is a pivotal architectural decision. The Claude Code framework mandates the use of Development Containers (Devcontainers) as the sole supported environment. This is not a suggestion but a core tenet of our secure-by-design philosophy, directly addressing the primary risks associated with agentic AI development. Devcontainers provide a fully containerised development environment, leveraging Docker to encapsulate all dependencies, tools, and configurations required for a project.8 This approach yields four non-negotiable benefits:

1. **Isolation and Security:** An agent, by its nature, executes code and interacts with the filesystem. Running an agent directly on a host machine creates an unacceptable risk. A compromised or misbehaving agent could access sensitive local files, traverse the network, or install malicious software. Devcontainers provide a robust sandbox, isolating the agent's environment from the host operating system at the filesystem, network, and process levels.9 This containment ensures that even if an agent is compromised, the impact is confined within the disposable container, preventing lateral movement and protecting the developer's machine and the wider network.10  
2. **Consistency:** The perennial problem of "it works on my machine" is a significant source of inefficiency and bugs in collaborative projects. Discrepancies in operating systems, library versions, or environment variable settings can cause subtle, non-deterministic failures that are difficult to debug. Devcontainers eliminate this entire class of problems by ensuring that every team member, from a new hire to a CI/CD runner, operates within an identical, version-controlled environment defined by the project's Dockerfile and devcontainer.json.8  
3. **Reproducibility:** Scientific and engineering rigour demands reproducibility. The ability to precisely replicate the conditions under which a bug occurred or a result was generated is essential for effective debugging and validation. Because a Devcontainer packages the entire toolchain and all dependencies into a version-controlled definition, it provides a perfect, reproducible snapshot of the development environment. This guarantees that any developer can check out a specific commit and recreate the exact environment in which that code was written and tested.9  
4. **Simplified Onboarding:** Configuring a complex development environment can be a time-consuming and error-prone process for new team members. Devcontainers streamline onboarding to a simple, two-step process: clone the repository and open it in a container-aware editor.9 The  
   postCreateCommand feature automatically handles the installation of dependencies, allowing a new developer to be productive within minutes, not days.

By mandating Devcontainers, we shift the principles of sandboxing and immutable infrastructure "left" to the earliest possible stage of the development lifecycle. This establishes a secure, consistent, and efficient foundation upon which all subsequent agentic development can be safely built.

### **1.2 Setting Up Your First Devcontainer for Claude Code**

This section provides a step-by-step guide to configuring a standard Devcontainer for Claude Code projects.

**Prerequisites:**

* **Docker:** Ensure Docker Desktop (or a compatible Docker engine) is installed and running on your host machine.9  
* **Editor with Devcontainer Support:** A code editor that supports the Devcontainer specification is required. Visual Studio Code with the "Dev Containers" extension is the reference implementation.

**Step-by-Step Configuration:**

1. Create the .devcontainer Directory:  
   In the root of your project repository, create a new directory named .devcontainer. This directory will house the configuration files for your development environment.  
   Bash  
   mkdir.devcontainer  
   cd.devcontainer

2. Create the devcontainer.json File:  
   Inside the .devcontainer directory, create a file named devcontainer.json. This file defines the container's properties, such as the base image, extensions to install, and ports to forward.  
   **./.devcontainer/devcontainer.json:**  
   JSON  
   {  
     "name": "Claude Code Standard Environment",  
     "build": {  
       "dockerfile": "Dockerfile",  
       "context": "."  
     },  
     "customizations": {  
       "vscode": {  
         "extensions": \[  
           "ms-python.python",  
           "ms-python.vscode-pylance",  
           "charliermarsh.ruff"  
         \],  
         "settings": {  
           "terminal.integrated.shell.linux": "/bin/bash"  
         }  
       }  
     },  
     "forwardPorts": ,  
     "postCreateCommand": "pip install \--user \-r requirements.txt && npm install \-g @anthropic-ai/claude-code",  
     "remoteUser": "vscode"  
   }

   Explanation of Properties 13:  
   * name: A human-readable name for the environment.  
   * build: Specifies how to build the container image. dockerfile points to the Dockerfile in the same directory, and context sets the build context to the .devcontainer directory.  
   * customizations.vscode: Configures the VS Code editor inside the container, installing specified extensions and applying settings.  
   * forwardPorts: Automatically forwards port 8000 from the container to the host machine, useful for web development.  
   * postCreateCommand: A crucial lifecycle hook. This command runs once after the container is created, perfect for installing project dependencies from requirements.txt and the Claude Code CLI itself.11  
   * remoteUser: Specifies the non-root user that the editor and terminal will run as inside the container, which is a security best practice.  
3. Create the Dockerfile:  
   Next, create the Dockerfile that defines the container image itself. This file specifies the base operating system, installs system-level dependencies, and sets up the non-root user.  
   **./.devcontainer/Dockerfile:**  
   Dockerfile  
   \# Use a minimal, secure base image from Microsoft's official repository  
   FROM mcr.microsoft.com/devcontainers/python:3.11\-bullseye

   \# Avoid prompts from apt  
   ENV DEBIAN\_FRONTEND=noninteractive

   \# Install system dependencies. 'jq' is useful for processing JSON in shell scripts.  
   RUN apt-get update && apt-get \-y install \--no-install-recommends \\  
       jq \\  
       && apt-get clean && rm \-rf /var/lib/apt/lists/\*

   \# Switch back to the non-root 'vscode' user created in the base image  
   USER vscode

4. Reopen in Container:  
   Once these two files are saved, your editor should prompt you to "Reopen in Container." Accepting this prompt will trigger Docker to build the image and launch the development environment. Your terminal, file explorer, and debugger will now be operating entirely inside the isolated container.

### **1.3 Creating a Centralised, Version-Controlled Agent Configuration (\~/.claude\_agents)**

A key architectural pattern for managing a suite of reusable agents is to decouple their definitions from any single project repository. Instead of scattering agent logic across various projects, this framework advocates for a centralised, version-controlled directory in the user's home directory: \~/.claude\_agents.

This approach is inspired by established practices in configuration management, where centralised repositories for tools like Ansible or Terraform provide a single source of truth for infrastructure and automation logic.14 Applying this principle to AI agents offers significant advantages:

* **Reusability:** An agent defined once in \~/.claude\_agents can be invoked from any project directory on the system, promoting the creation of a personal or team-wide library of standard, reusable agents.  
* **Simplified Management:** Updating an agent's logic or prompt requires changing it in only one place. This is far more efficient and less error-prone than hunting down and updating copies of the agent in multiple repositories.  
* **Atomic Versioning:** The entire \~/.claude\_agents directory can be managed as a Git repository. This allows you to version your entire suite of agents atomically. You can create branches to experiment with new agent logic, review changes through pull requests, and roll back to a previous known-good state if an update causes issues.  
* **Consistent Security & Auditing:** By using a shared template for invocation scripts, you can enforce consistent security controls—such as audit logging or environment variable sanitisation—across all your agents from a single point of control.

**Recommended Directory Structure:**

The \~/.claude\_agents directory is organised by agent name. Each agent has its own subdirectory containing its core logic files.

\~/.claude\_agents/  
├── config.yml                \# Global configuration for the Claude Code CLI  
├── documenter/  
│   ├── documenter.md         \# The custom slash command (agent prompt)  
│   └── documenter.sh         \# The invocation script  
├── janitor/  
│   ├── janitor.md  
│   └── janitor.sh  
└── templates/  
    └── prompt\_template.txt   \# A reusable prompt adaptation template

**Implementation Steps:**

1. **Initialise the Directory and Git Repository:**  
   Bash  
   mkdir \~/.claude\_agents  
   cd \~/.claude\_agents  
   git init

2. Create Agent Subdirectories:  
   For each new agent you create (such as those in the following blueprint chapters), create a corresponding subdirectory.  
3. Populate with Agent Files:  
   Place the agent's slash command (.md), invocation script (.sh), and any associated prompt templates into its directory.  
4. Version Control:  
   Commit your changes regularly. It is highly recommended to host this repository on a private Git server to share and synchronise your agent suite across multiple machines.  
   Bash  
   git add.  
   git commit \-m "feat: Add initial version of the Documenter agent"

This centralised structure transforms a collection of disparate scripts into a managed, secure, and reusable agentic framework.

### **1.4 Troubleshooting Common Devcontainer Issues**

While Devcontainers provide a stable and consistent environment, issues can arise, often related to the underlying Docker configuration or host system interactions. This section provides solutions to common problems.

| Problem / Error Message | Root Cause | Solution |
| :---- | :---- | :---- |
| **"Cannot connect to the Docker daemon. Is the docker daemon running?"** | The Docker service on your host machine is not running or has crashed. | **1\. Verify Docker Status:** Check the Docker Desktop application or run docker ps in your host terminal. **2\. Restart Docker:** If it is not running, start or restart the Docker Desktop application. On Linux, you may need to run sudo systemctl start docker. 16 |
| **Devcontainer is very slow or processes are crashing (e.g., Webpack).** | The Docker daemon has insufficient memory or CPU resources allocated. This is common on macOS where Docker defaults to a low memory limit (e.g., 2 GB). 17 | **1\. Increase Docker Resources:** Open Docker Desktop Preferences/Settings. **2\. Navigate to Resources:** Go to the "Resources" tab. **3\. Adjust Limits:** Increase the allocated Memory (e.g., to 8 GB or more) and CPUs. **4\. Apply & Restart:** Apply the changes. Docker will restart, and subsequent Devcontainer sessions will use the new limits. 17 |
| **"Error: EACCES: permission denied..." when accessing mounted files.** | The user ID (UID) and group ID (GID) inside the container do not match the user's UID/GID on the host machine, causing file permission mismatches on bind-mounted volumes. 18 | **1\. Use a Non-Root User:** Ensure your Dockerfile and devcontainer.json specify a non-root user (e.g., vscode). **2\. Synchronise UIDs/GIDs:** The base images (e.g., mcr.microsoft.com/devcontainers/\*) often handle this automatically. If using a custom Dockerfile, you may need to add script logic in your postCreateCommand to synchronise the container user's UID/GID with the mounted workspace folder's owner. |
| **"Error response from daemon: driver failed programming external connectivity...: bind: address already in use."** | A port that the Devcontainer is trying to forward (defined in forwardPorts) is already being used by another process on your host machine or another Docker container. 17 | **1\. Identify the Conflicting Process:** On your host, use a command like lsof \-i :\<port\_number\> (macOS/Linux) or \`netstat \-ano |
| **Git commands fail inside the container (e.g., "Permission denied (publickey)").** | The container does not have access to your host machine's SSH keys, which are required to authenticate with Git services like GitHub. | **1\. Use SSH Agent Forwarding:** The recommended method is to ensure your SSH agent is running on the host and your SSH keys are added (ssh-add). Devcontainer-aware editors typically forward the SSH agent socket into the container automatically, making your keys available without copying them. **2\. Verify Permissions:** On your host, ensure your SSH key files (e.g., \~/.ssh/id\_rsa) have strict permissions (chmod 600). 16 |
| **Initial container build fails with network errors.** | The Docker build process requires an internet connection to pull the base image and install packages. A firewall, proxy, or network outage can cause it to fail. | **1\. Check Internet Connection:** Ensure your host machine has a stable internet connection. **2\. Configure Docker for Proxies:** If you are behind a corporate proxy, you must configure Docker Desktop's network settings to use that proxy. **3\. Retry the Build:** After resolving the network issue, use your editor's "Rebuild Container" command to try again. 12 |

## **Chapter 2: Core Agent Blueprint: The Automated Documenter**

This blueprint provides a complete engineering specification for an agent designed to automate the creation and maintenance of source code documentation. By parsing code and extracting meaningful information, this agent ensures that documentation remains synchronised with the implementation, reducing manual effort and improving the accuracy of technical references.

### **Objective & Success Criteria**

* **Objective:** To create a robust, autonomous agent that scans a given directory of Python source code, parses function and class definitions, and generates a comprehensive, human-readable Markdown documentation file.  
* **Success Criteria:**  
  1. **Coverage:** The agent successfully generates documentation for at least 95% of all non-private (i.e., not prefixed with an underscore) functions and classes within the target directory.  
  2. **CI/CD Integration:** The agent can be successfully integrated into a CI/CD pipeline, automatically regenerating the documentation file on every commit to the main branch.  
  3. **Quality:** The generated Markdown file is well-formed, passes a standard Markdown linting check, and contains no broken internal links.  
  4. **Accuracy:** The function signatures, parameters, and return types in the documentation exactly match those in the source code.

### **Real-World Case Study**

A fast-moving software development team at a financial technology company struggled to keep their API reference documentation up-to-date. Manual updates were frequently forgotten during rapid development cycles, leading to a growing gap between the code and the documentation. They deployed the /document agent within their GitHub Actions workflow. Now, when a developer merges a pull request containing changes to their Python backend, the agent automatically scans the modified files, updates the docs/api\_reference.md file with new and changed function definitions, and commits the updated documentation back to the repository as part of the workflow. This "docs-as-code" approach ensures the documentation is always a faithful representation of the current codebase, significantly reducing onboarding time for new developers and improving clarity for all stakeholders.19

### **Agent Workflow Diagram**

Code snippet

flowchart TD  
    A \--\> B{Target path exists?};  
    B \-- No \--\> B\_Error\[Log error and exit\];  
    B \-- Yes \--\> C\[Use \`glob\` tool to find all \`\*.py\` files in path\];  
    C \--\> D\[Initialise empty Markdown string\];  
    D \--\> E{For each Python file};  
    E \--\> F\[Use \`readFile\` tool to get file content\];  
    F \--\> G\[Use \`parse\_python\_ast\` tool to extract functions and classes\];  
    G \--\> H{For each function/class};  
    H \--\> I{Is it a private member (starts with '\_')?};  
    I \-- Yes \--\> H;  
    I \-- No \--\> J\[Extract signature, docstring, and type hints\];  
    J \--\> K\[Format extracted info into a Markdown block\];  
    K \--\> L\[Append Markdown block to main string\];  
    L \--\> H;  
    H \-- All members processed \--\> E;  
    E \-- All files processed \--\> M\[Use \`writeFile\` tool to save Markdown string to output file\];  
    M \--\> N\[Log success message with file path\];  
    N \--\> O\[End\];

### **The Custom Slash Command (documenter.md)**

This file contains the core prompt and logic for the Automated Documenter agent. It is stored at \~/.claude\_agents/documenter/documenter.md.

You are an expert technical writer AI agent. Your purpose is to generate clear, concise, and accurate Markdown documentation from Python source code.

Your Goal:  
Scan a directory of Python files, parse the functions and classes, and create a single, well-structured Markdown file summarising the public API.  
Your Tools:  
You have access to the following tools:

* glob(pattern: str): Finds files matching a pattern.  
* readFile(path: str): Reads the content of a file.  
* parse\_python\_ast(code: str): Parses Python code and returns a JSON structure of functions and classes with their signatures, docstrings, and type hints.  
* writeFile(path: str, content: str): Writes content to a file.

**Step-by-Step Instructions:**

1. **Identify Target Files:** The user will provide a path. Use the glob tool to find all Python files (\*.py) within that path recursively.  
2. Process Each File: Iterate through the list of files found. For each file:  
   a. Use the readFile tool to load its content.  
   b. Use the parse\_python\_ast tool to extract all function and class definitions.

3. ### **Filter and Format: For each extracted function and class:**    **a. IGNORE any item whose name begins with an underscore (\_). These are considered private and should not be documented.**    **b. Format the information into a standard Markdown structure. Use the following template for each item:markdown**     **function\_name(parameter: type) \-\> return\_type**     **Description:**    **{docstring\_summary}**    **Parameters:**

   * parameter\_name (type): {docstring\_parameter\_description}

   **Returns:**

   * return\_type: {docstring\_return\_description}  
4. **Aggregate and Write:** Concatenate the formatted Markdown for all functions and classes from all files into a single string. Add a main title to the document, like \# API Reference.  
5. **Final Output:** Use the writeFile tool to save the complete Markdown string to the output path specified by the user.

**Important Rules:**

* Be precise. The signatures and types must exactly match the source code.  
* Be clear. Use simple, accessible language in your formatting.  
* Be disciplined. Do not document private members.  
* Do not invent or "hallucinate" descriptions. If a docstring is missing, state "No description provided."

\#\#\# \*\*The Invocation Script (\`documenter.sh\`)\*\*  
This script provides a robust, logged wrapper for executing the agent. It is stored at \`\~/.claude\_agents/documenter/documenter.sh\`.

\`\`\`bash  
\#\!/bin/bash  
\# Invocation script for the Automated Documenter agent

\# \--- Configuration \---  
AGENT\_LOG\_FILE="/var/log/claude\_agents.log"  
AGENT\_COMMAND\_FILE="$HOME/.claude\_agents/documenter/documenter.md"  
TARGET\_PATH=${1:-.} \# Default to current directory if no path is provided  
OUTPUT\_FILE=${2:-"API\_DOCUMENTATION.md"} \# Default output file name

\# \--- Pre-flight Checks \---  
if; then  
    echo "Error: Target path '$TARGET\_PATH' does not exist or is not a directory." | tee \-a "$AGENT\_LOG\_FILE"  
    exit 1  
fi

if; then  
    echo "Error: Agent command file not found at '$AGENT\_COMMAND\_FILE'." | tee \-a "$AGENT\_LOG\_FILE"  
    exit 1  
fi

\# \--- Audit Logging \---  
echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- User '$USER' initiated /documenter agent." \>\> "$AGENT\_LOG\_FILE"  
echo "  \- Target Path: $(realpath "$TARGET\_PATH")" \>\> "$AGENT\_LOG\_FILE"  
echo "  \- Output File: $(realpath "$OUTPUT\_FILE")" \>\> "$AGENT\_LOG\_FILE"

\# \--- Agent Invocation \---  
\# The prompt is constructed to give the agent its task and necessary parameters.  
PROMPT="Please generate documentation for the Python files in the path '${TARGET\_PATH}' and write the output to '${OUTPUT\_FILE}'."

echo "Invoking documenter agent on '$TARGET\_PATH'..."  
claude /documenter \--prompt "$PROMPT"

\# \--- Post-flight Check \---  
if \[ $? \-eq 0 \] &&; then  
    echo "Agent executed successfully. Documentation generated at '$OUTPUT\_FILE'."  
    echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- Agent /documenter completed successfully." \>\> "$AGENT\_LOG\_FILE"  
else  
    echo "Error: Agent execution failed. Check logs for details."  
    echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- Agent /documenter failed." \>\> "$AGENT\_LOG\_FILE"  
    exit 1  
fi

exit 0

### **Prompt Adaptation Template**

This template allows for easy customisation of the agent's task for different contexts.

"Generate documentation for the Python files located in the '{directory\_path}' directory. The output should be a single Markdown file named '{output\_filename}'. The documentation should follow the '{style\_guide}' conventions (e.g., 'Google Style', 'NumPy Style'). Exclude any files or directories matching the following patterns: \[{exclude\_patterns}\]."

### **The Risk & Control Matrix**

Automated documentation generation introduces unique risks beyond simple inaccuracy. The primary threat is the inadvertent exposure of sensitive information or internal implementation details that should not be public-facing.

| Risk ID | Risk Description | Likelihood | Impact | Control Measure | Control Owner |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **DOC-01** | **Sensitive Data Exposure:** Agent documents an internal function containing hardcoded secrets (API keys, passwords) or proprietary business logic, exposing it in the generated file.20 | Medium | High | **1\. Prompt-based Filtering:** The agent's prompt explicitly instructs it to ignore functions containing keywords like secret, password, api\_key, or marked with an @internal decorator. **2\. Post-processing Scan:** As a mandatory CI/CD step, run an automated secrets scanner (e.g., gitleaks) on the generated documentation file before it is published or committed. Fail the build if secrets are found. | DevSecOps Team |
| **DOC-02** | **Inaccurate or Misleading Documentation:** The agent hallucinates or misinterprets the purpose of a function, generating documentation that is factually incorrect and could mislead developers.22 | Medium | Medium | **1\. Human-in-the-Loop Review:** The CI/CD workflow must be configured to generate documentation on a feature branch and assign a human developer for review via a pull request. The documentation must not be merged to main without human approval. **2\. Grounding in Docstrings:** The agent's prompt must heavily prioritise information from the source code's docstrings over its own general knowledge. | Development Team Lead |
| **DOC-03** | **Incomplete Coverage:** The agent fails to parse complex code files or specific language features, leading to gaps in the documentation and a false sense of completeness. | Low | Medium | **1\. Coverage Metrics:** The CI/CD job that runs the agent should also calculate a documentation coverage metric (e.g., percentage of public functions with generated docs) and fail the build if it drops below a predefined threshold (e.g., 95%). **2\. Error Handling:** The agent must be designed to log parsing errors for specific files but continue processing others, rather than failing the entire job. | QA Team |

### **Ethical Considerations**

* **Accountability and Transparency:** The generated documentation must be clearly marked as AI-generated to manage expectations about its quality and accuracy. A header should be automatically included in every generated file, stating: This document was auto-generated by the /documenter agent on YYYY-MM-DD. It should be reviewed for accuracy. This ensures that accountability for the content ultimately remains with the human developers who review and approve it.24  
* **Bias and Inclusivity:** AI models can be trained on text that contains non-inclusive language or overly technical jargon. The agent's prompt must include a specific instruction to "write in clear, simple language that is accessible to developers from diverse backgrounds and skill levels." This helps mitigate the risk of producing documentation that is exclusionary or difficult to understand.26  
* **Intellectual Property:** The agent must be strictly instructed to base its documentation *only* on the provided source code and its associated docstrings. It must be explicitly forbidden from incorporating external knowledge or copyrighted material from its training data into the documentation, which could lead to IP infringement.26

### **Failure Modes & Recovery**

* **Failure Mode: Code Parsing Error**  
  * **Description:** The agent encounters a Python file with complex syntax or experimental features that its AST parsing tool cannot handle, causing the agent to halt.  
  * **Recovery Strategy:** The agent's internal logic should wrap the parsing of each file in a try...except block. If a file fails to parse, the agent should log the specific error and the file path, then skip that file and continue processing the rest of the directory. The invocation script should check the final log for any parsing errors and report them as warnings, ensuring that a single problematic file does not prevent the entire documentation job from completing.  
* **Failure Mode: Large Codebase Timeout**  
  * **Description:** When run on a very large repository, the agent process exceeds its allocated time limit in the CI/CD environment before it can finish processing all files.  
  * **Recovery Strategy:**  
    1. **Incremental Processing:** The invocation script should be designed to work incrementally. It should get the list of changed files from Git (git diff \--name-only main...) and pass only that list to the agent. This is far more efficient than re-scanning the entire repository on every commit.29  
    2. **Parallelisation:** For the initial full documentation build, the invocation script can be enhanced to partition the list of all files into batches and invoke multiple instances of the documenter agent in parallel, each working on a subset of the files. The final step would be to concatenate the partial Markdown outputs.  
* **Failure Mode: Overwriting Manual Edits**  
  * **Description:** A developer manually adds a valuable explanatory diagram or a "getting started" section to the auto-generated documentation file. The next time the agent runs, it overwrites the entire file, destroying the manual contributions.  
  * **Recovery Strategy:** The agent should be designed to work with structured "injection points." Instead of overwriting the entire file, it should be instructed to only replace content between specific markers.

**Example (API\_DOCUMENTATION.md):**API ReferenceHere is a manually written introduction and a helpful diagram.old\_function()

### **...**

Here is some more manually written context.  
The agent's prompt would be updated to instruct it to read the file, find the and markers, and replace only the content between them. This preserves human-authored content while keeping the API reference section up-to-date.

## **Chapter 3: Core Agent Blueprint: The Guardian File-Watcher**

This blueprint specifies a persistent, long-running agent that serves as an active monitor for filesystem events. It acts as a trigger for automated workflows, initiating actions in real-time as files are created, modified, or deleted. This pattern is fundamental for building event-driven automation and data processing pipelines.

### **Objective & Success Criteria**

* **Objective:** To create a persistent agent that reliably monitors a specified directory for new file creations and, upon detection, triggers a predefined shell command or script with the path of the new file as an argument.  
* **Success Criteria:**  
  1. **Latency:** The agent detects a new file and triggers the associated action within 5 seconds of the file write being completed.  
  2. **Reliability:** The agent successfully triggers the action for 99.9% of new files that match the specified pattern over a 24-hour period.  
  3. **Filtering:** The agent correctly ignores temporary files (e.g., those ending in .tmp or \~) and events other than file creation.  
  4. **Durability:** The agent process can run continuously for at least 7 days without crashing or requiring a manual restart.

### **Real-World Case Study**

A media company uses an automated pipeline to process video uploads. Videographers upload raw footage files to a network-mounted /uploads/video/incoming directory. The /watch agent is configured to monitor this directory for new .mp4 files. As soon as a new video file is fully uploaded, the agent triggers a transcoding script. This script adds the video to a processing queue, converts it into multiple formats for web and mobile streaming, and updates a central database with the new content's metadata. This event-driven architecture removes the need for manual polling and significantly accelerates the time it takes for new content to become available to viewers.

### **Agent Workflow Diagram**

Code snippet

flowchart TD  
    subgraph Initialisation  
        A \--\> B\[Validate parameters: path exists, action is executable\];  
        B \-- Invalid \--\> B\_Error\[Log error and exit\];  
        B \-- Valid \--\> C;  
    end

    subgraph Monitoring Loop  
        C \--\> D\[Enter persistent monitoring loop\];  
        D \--\> E{Await file system event};  
        E \--\> F{Event type is 'file created'?};  
        F \-- No \--\> D;  
        F \-- Yes \--\> G{File name matches pattern?};  
        G \-- No \--\> D;  
        G \-- Yes \--\> H;  
        H \-- Lock Acquired \--\> I\[Execute action script with file path as argument\];  
        I \--\> J\[Log action execution (success or failure)\];  
        J \--\> D;  
        H \-- Lock Failed (Timeout) \--\> K\[Log file lock error and ignore file\];  
        K \--\> D;  
    end

### **The Custom Slash Command (watcher.md)**

This file defines the agent's core behaviour. It is stored at \~/.claude\_agents/watcher/watcher.md.

You are a File System Guardian agent. Your purpose is to run as a persistent background process, monitoring a directory for new files and triggering a command when one appears.

Your Goal:  
Watch a specified directory for file creation events that match a given pattern. When a new, complete file is detected, execute a specified shell command.  
**Your Tools:**

* file\_watcher(path: str, pattern: str): A persistent tool that monitors a directory. It yields an event object for each new file matching the pattern. This tool is a generator and will block indefinitely.  
* execute\_shell(command: str): Executes a shell command.  
* check\_file\_lock(path: str): A tool that returns true if a file can be opened with an exclusive write lock, and false otherwise. This is used to verify a file is no longer being written to.

**Step-by-Step Instructions:**

1. **Initialise the Watcher:** The user will provide a path and a file pattern. Start the file\_watcher tool with these parameters.  
2. **Enter the Main Loop:** Begin an infinite loop to process events yielded by file\_watcher.  
3. Handle New File Event: When a new file event is received:  
   a. Log the detection of the new file path.  
   b. CRITICAL: Verify Write Completion. Before taking any action, enter a loop to check if the file is complete.  
   i. Call check\_file\_lock(path).  
   ii. If it returns false, wait for 500 milliseconds and retry.  
   iii. Repeat up to 10 times. If the file is still locked after 10 retries, log a timeout error and ignore the file.  
   iv. If it returns true, proceed to the next step.  
   c. Execute Action: The user will have provided a command template (e.g., process\_file.sh {filepath}). Replace {filepath} with the actual path of the new file.  
   d. Use the execute\_shell tool to run the fully formed command.  
   e. Log the command that was executed and its exit code.  
4. **Continue Monitoring:** The file\_watcher tool will continue to yield new events, so the loop will continue automatically.

**Important Rules:**

* **Patience is a Virtue:** Never act on a file immediately upon creation. Always use the check\_file\_lock tool to prevent processing incomplete files. This is your most important safety instruction.  
* **Be Specific:** Only act on file creation events. Ignore modifications and deletions.  
* **Log Everything:** Log every detected event, every lock check, and every action taken. This is crucial for debugging.

### **The Invocation Script (watcher.sh)**

This script is designed to launch the watcher agent as a daemonised process. It is stored at \~/.claude\_agents/watcher/watcher.sh.

Bash

\#\!/bin/bash  
\# Invocation script for the Guardian File-Watcher agent.

\# \--- Configuration \---  
AGENT\_LOG\_FILE="/var/log/claude\_agents\_watcher.log"  
AGENT\_COMMAND\_FILE="$HOME/.claude\_agents/watcher/watcher.md"  
PID\_FILE="/var/run/claude\_watcher.pid"

\# \--- Command Line Arguments \---  
TARGET\_PATH=$1  
FILE\_PATTERN=$2  
ACTION\_COMMAND=$3

\# \--- Usage \---  
if \[ "$\#" \-ne 3 \]; then  
    echo "Usage: $0 \<path\_to\_watch\> \<file\_pattern\> '\<action\_command\>'"  
    echo "Example: $0 /data/incoming '\*.csv' 'python /app/process.py {filepath}'"  
    exit 1  
fi

\# \--- Pre-flight Checks \---  
if; then  
    echo "Error: PID file exists. Watcher may already be running. (PID: $(cat "$PID\_FILE"))" | tee \-a "$AGENT\_LOG\_FILE"  
    exit 1  
fi

if; then  
    echo "Error: Target path '$TARGET\_PATH' does not exist." | tee \-a "$AGENT\_LOG\_FILE"  
    exit 1  
fi

\# \--- Audit Logging & Daemonisation \---  
echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- User '$USER' starting /watcher agent." \>\> "$AGENT\_LOG\_FILE"  
echo "  \- Watching Path: $TARGET\_PATH" \>\> "$AGENT\_LOG\_FILE"  
echo "  \- File Pattern: $FILE\_PATTERN" \>\> "$AGENT\_LOG\_FILE"  
echo "  \- Action Command: $ACTION\_COMMAND" \>\> "$AGENT\_LOG\_FILE"

PROMPT="Please monitor the directory '${TARGET\_PATH}' for new files matching '${FILE\_PATTERN}'. When a new file is found, execute the command: '${ACTION\_COMMAND}'."

\# Launch the agent in the background using nohup to ensure it keeps running  
\# after the terminal session closes. Redirect stdout and stderr to the log file.  
nohup claude /watcher \--prompt "$PROMPT" \>\> "$AGENT\_LOG\_FILE" 2\>&1 &

\# Store the Process ID (PID) of the background job  
AGENT\_PID=$\!  
echo $AGENT\_PID \> "$PID\_FILE"

echo "Guardian File-Watcher agent started successfully."  
echo "  \- PID: $AGENT\_PID"  
echo "  \- Log File: $AGENT\_LOG\_FILE"  
echo "To stop the agent, run: kill $(cat $PID\_FILE) && rm $PID\_FILE"

exit 0

### **Prompt Adaptation Template**

This template allows for flexible configuration of the watcher's behaviour.

"Monitor the directory '{directory\_to\_watch}' for files matching the pattern '{file\_pattern}'. When a new file is created, execute the command: '{command\_to\_execute} {new\_filepath}'. Implement a debounce period of {debounce\_seconds} seconds to process files in batches. Ignore all file events other than creation."

### **The Risk & Control Matrix**

Persistent monitoring agents introduce risks related to resource consumption, race conditions, and reliability. The controls must ensure both stability and correctness.

| Risk ID | Risk Description | Likelihood | Impact | Control Measure | Control Owner |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **WAT-01** | **Race Condition:** Agent attempts to process a file that is still being written to disk, leading to data corruption or a failed processing job.30 | High | High | **1\. File Lock Verification:** The agent's logic *must* include a "wait and check" loop. After detecting a file, it must repeatedly attempt to acquire an exclusive file lock. Only after successfully acquiring and releasing the lock should it proceed, confirming the write operation is complete. **2\. Use a Trigger File:** A more robust pattern is to have the writing process create a separate, empty trigger file (e.g., data.csv.done) after the main file is written. The agent watches only for .done files. | Developer |
| **WAT-02** | **Event Storm/Denial of Service:** A large batch of files created simultaneously triggers a high volume of events, overwhelming the agent or the downstream processing system.32 | Medium | High | **1\. Event Debouncing:** The agent's logic should implement debouncing. It should collect all file creation events within a short time window (e.g., 2-5 seconds) and then trigger the action for the entire batch, rather than for each file individually. **2\. Rate Limiting:** The agent must enforce a limit on the number of concurrent actions it can trigger to prevent overwhelming downstream systems. | Developer |
| **WAT-03** | **Missed Events:** The underlying OS file watcher buffer overflows during a burst of high activity, causing the agent to miss file creation events entirely.32 | Low | High | **1\. Hybrid Watch-and-Poll Model:** The agent should supplement its real-time watching with a periodic polling mechanism. Every few minutes, it should scan the entire directory and compare the file list against its internal record of processed files. Any files present in the directory but not in its record are then added to the processing queue. This reconciliation ensures 100% reliability. | Developer |
| **WAT-04** | **Unmonitored Agent Failure:** The agent process crashes silently, and no one is aware that the directory is no longer being monitored, leading to a backlog of unprocessed files. | Medium | High | **1\. Health Check Endpoint:** The agent should expose a simple health check endpoint (e.g., a local HTTP port or by updating a file's timestamp). An external monitoring system (e.g., Prometheus, Nagios) should be configured to periodically check this endpoint and raise an alert if the agent becomes unresponsive. **2\. Process Supervision:** Run the agent under a process supervisor like systemd or supervisorctl, which can automatically restart the agent if it crashes. | DevOps Team |

### **Ethical Considerations**

* **Privacy and Surveillance:** A file-watching agent is a powerful surveillance tool. Its use must be strictly limited to non-human, service-oriented directories (e.g., data ingest folders, log directories). **Under no circumstances should this agent be deployed to monitor employee home directories or other personal spaces without explicit, informed, and written consent.** Deploying such a tool for covert employee monitoring is a severe ethical breach and may have legal consequences.34  
* **Transparency:** The operation of any persistent agent must be transparent to system administrators. The invocation script's practice of logging its startup parameters, PID, and all subsequent actions to a well-known log file is a mandatory transparency measure. This ensures that an administrator can always determine what the agent is doing, why it is running, and who started it.  
* **Data Handling:** The agent itself does not process file contents, but it triggers processes that do. The overall workflow must adhere to data protection principles. If the monitored directory contains PII or other sensitive data, the triggered action script must be designed with appropriate security and privacy controls.

### **Failure Modes & Recovery**

* **Failure Mode: Network Share Unavailability**  
  * **Description:** The agent is monitoring a directory on a network share (e.g., NFS, SMB), and the network connection is temporarily lost. The underlying OS watcher may fail silently or terminate.32  
  * **Recovery Strategy:** The agent's main loop must include a heartbeat check to ensure the target directory is still accessible. If it becomes inaccessible, the agent should enter a "reconnect" state, where it periodically attempts to access the directory with an exponential backoff delay. Once the connection is restored, it must immediately trigger the "reconciliation" process described in risk WAT-03 to process any files that were created during the outage.  
* **Failure Mode: Action Script Failure**  
  * **Description:** The agent successfully detects a file and triggers the action script, but the script itself fails (e.g., due to a bug, misconfiguration, or downstream system failure).  
  * **Recovery Strategy:** The agent should not be responsible for the internal logic of the action script, but it must be resilient to its failures.  
    1. **Error Logging:** The agent must capture the stderr and exit code of the action script and log them clearly.  
    2. **Dead Letter Queue:** If an action script fails repeatedly for the same file, the agent should move the problematic file to a designated "quarantine" or "dead\_letter" directory. This prevents the agent from getting stuck in an infinite retry loop on a poison pill file and allows a human operator to investigate the issue manually.

**Code Snippet (Bash \- in watcher.sh):**Bash  
\# Inside the agent's logic for executing the action  
FULL\_COMMAND=$(echo "$ACTION\_COMMAND" | sed "s/{filepath}/$FILE\_PATH/g")

\# Execute the command, capturing output and exit code  
OUTPUT=$($FULL\_COMMAND 2\>&1)  
EXIT\_CODE=$?

if; then  
    log\_error "Action for $FILE\_PATH failed with exit code $EXIT\_CODE. Output: $OUTPUT"  
    \# Implement retry logic here...  
    \# If retries fail, move to quarantine  
    mv "$FILE\_PATH" "/data/incoming\_quarantine/"  
    log\_warning "Moved problematic file $FILE\_PATH to quarantine."  
else  
    log\_info "Action for $FILE\_PATH succeeded."  
fi

## **Chapter 4: Core Agent Blueprint: The Janitor File-Management**

This blueprint details an agent designed for automated filesystem hygiene. The Janitor agent systematically enforces data retention policies by cleaning up temporary files, old logs, and other ephemeral data, preventing disk space exhaustion and reducing data clutter. Its design prioritises safety above all else, incorporating multiple safeguards against accidental data loss.

### **Objective & Success Criteria**

* **Objective:** To create a configurable agent that scans a target directory and its subdirectories, identifies files older than a specified age, and moves them to a designated quarantine directory for later review and permanent deletion.  
* **Success Criteria:**  
  1. **Effectiveness:** After a successful run, 100% of files older than the specified retention period in the target directory (and not on the exclusion list) are moved to the quarantine directory.  
  2. **Safety:** 0% of files younger than the retention period or on the exclusion list are moved.  
  3. **Auditability:** The agent produces a comprehensive, machine-readable (JSON) log file detailing every file that was moved, its original location, its size, its modification date, and a timestamp for the action.  
  4. **Confirmation:** The agent will not perform any move operations without first performing a "dry run" and receiving explicit confirmation from a human operator or a \--force flag.

### **Real-World Case Study**

A large e-commerce platform generates gigabytes of application and access logs daily across its server fleet. To manage storage costs and comply with a 30-day log retention policy, the DevOps team schedules the /janitor agent to run nightly on each server. The agent is configured to scan /var/log/app/, identify all .log files with a modification date older than 30 days, and move them to /var/log/quarantined/. A separate, heavily restricted process purges the quarantine directory weekly. This automated workflow ensures compliance and prevents disk-full alerts without risking the accidental deletion of critical, recent logs needed for debugging.

### **Agent Workflow Diagram**

Code snippet

flowchart TD  
    A \--\> B\[Validate parameters\];  
    B \--\> C;  
    C \--\> D{For each file};  
    D \--\> E{Is file path in exclusion list?};  
    E \-- Yes \--\> D;  
    E \-- No \--\> F{Is file modification time \> 'days' ago?};  
    F \-- No \--\> D;  
    F \-- Yes \--\> G\[Add file to 'files\_to\_move' list\];  
    G \--\> D;  
    D \-- All files scanned \--\> H;  
    H \--\> I{Is \--force flag present OR user confirms 'yes'?};  
    I \-- No \--\> J\[Log 'Operation cancelled by user' and exit\];  
    I \-- Yes \--\> K{For each file in 'files\_to\_move'};  
    K \--\> L\[Move file to quarantine directory\];  
    L \--\> M{Move successful?};  
    M \-- Yes \--\> N\[Log successful move to audit log\];  
    M \-- No \--\> O\[Log failed move to audit log and raise warning\];  
    N \--\> K;  
    O \--\> K;  
    K \-- All files moved \--\> P\[Log summary and exit\];

### **The Custom Slash Command (janitor.md)**

This file contains the agent's core logic, emphasising the "dry run" safety mechanism. It is stored at \~/.claude\_agents/janitor/janitor.md.

You are a meticulous and cautious System Janitor AI agent. Your primary directive is to clean up old files safely, with an absolute priority on preventing accidental data loss.

Your Goal:  
Identify and quarantine files in a specified directory that are older than a given number of days, while respecting an exclusion list.  
**Your Tools:**

* find\_files(path: str, older\_than\_days: int): Returns a list of files in the path older than the specified number of days.  
* move\_file(source\_path: str, destination\_path: str): Moves a file from source to destination.  
* log\_audit\_event(event\_type: str, details: dict): Writes a structured JSON event to the audit log.

**Step-by-Step Instructions:**

1. **Identify Candidates:** The user will provide a target path, an age in days, and an exclusion list. Use the find\_files tool to get an initial list of all files older than the specified age.  
2. **Apply Exclusions:** Filter the list from the previous step. Remove any file whose path is present in the user-provided exclusion list.  
3. Perform Dry Run:  
   a. This is the most important step. DO NOT move any files yet.  
   b. Present the final, filtered list of files that are candidates for quarantine to the user.  
   c. Explicitly ask for confirmation. State clearly: "The following files will be moved to quarantine. Do you want to proceed? (yes/no)".  
4. Await Confirmation:  
   a. If the user provided a \--force flag, you may skip the confirmation prompt and proceed directly to the next step.  
   b. Otherwise, wait for the user to respond "yes". If they respond with anything else, abort the operation immediately and log that the user cancelled.  
5. Execute Quarantine:  
   a. Once confirmation is received (or was skipped), iterate through the list of candidate files.  
   b. For each file, use the move\_file tool to move it to the specified quarantine directory.  
   c. For every single file movement, use the log\_audit\_event tool to create a detailed record. The details dictionary should include the original\_path, quarantined\_path, file\_size\_bytes, and last\_modified\_date.

**Important Rules:**

* **Safety First:** The dry run and confirmation step is **MANDATORY** unless a \--force flag is explicitly used. Never proceed with a destructive operation without it.  
* **Quarantine, Don't Delete:** Your primary action is to *move* files to a safe quarantine location, not to permanently delete them. The word "delete" should not be in your operational vocabulary.  
* **Impeccable Record Keeping:** Every action must be logged. The audit trail is non-negotiable.

### **The Invocation Script (janitor.sh)**

This script is designed for scheduled execution (e.g., via cron). It is stored at \~/.claude\_agents/janitor/janitor.sh.

Bash

\#\!/bin/bash  
\# Invocation script for the Janitor File-Management agent.  
\# Intended for automated, non-interactive execution (e.g., cron).

\# \--- Configuration \---  
AGENT\_LOG\_FILE="/var/log/claude\_agents\_janitor.log"  
AUDIT\_LOG\_FILE="/var/log/claude\_janitor\_audit.json"  
AGENT\_COMMAND\_FILE="$HOME/.claude\_agents/janitor/janitor.md"

\# \--- Parameters \---  
\# Example: Clean up log files older than 14 days  
TARGET\_PATH="/var/log/app"  
QUARANTINE\_PATH="/var/log/quarantined"  
DAYS\_OLD=14  
\# Comma-separated list of files to exclude  
EXCLUSIONS="important.log,metrics.log"

\# \--- Pre-flight Checks \---  
mkdir \-p "$QUARANTINE\_PATH" \# Ensure quarantine directory exists

\# \--- Audit Logging \---  
echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- Scheduled /janitor job started." \>\> "$AGENT\_LOG\_FILE"  
echo "  \- Target Path: $TARGET\_PATH" \>\> "$AGENT\_LOG\_FILE"  
echo "  \- Quarantine Path: $QUARANTINE\_PATH" \>\> "$AGENT\_LOG\_FILE"  
echo "  \- Max Age: $DAYS\_OLD days" \>\> "$AGENT\_LOG\_FILE"  
echo "  \- Exclusions: $EXCLUSIONS" \>\> "$AGENT\_LOG\_FILE"

\# \--- Agent Invocation \---  
\# For a scheduled script, we use the \--force flag to bypass the interactive confirmation.  
\# The safety is provided by the quarantine pattern and careful configuration.  
PROMPT="As a scheduled task, perform a cleanup of the directory '${TARGET\_PATH}'. Quarantine all files older than ${DAYS\_OLD} days to '${QUARANTINE\_PATH}'. Exclude the following files:. Log all actions to '${AUDIT\_LOG\_FILE}'."

echo "Invoking janitor agent..."  
claude /janitor \--prompt "$PROMPT" \--force

\# \--- Post-flight Check \---  
if \[ $? \-eq 0 \]; then  
    echo "Janitor agent completed successfully."  
    echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- Scheduled /janitor job completed." \>\> "$AGENT\_LOG\_FILE"  
else  
    echo "Error: Janitor agent failed. Check logs for details."  
    echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- Scheduled /janitor job failed." \>\> "$AGENT\_LOG\_FILE"  
    \# In a production environment, this would trigger an alert (e.g., to PagerDuty).  
    exit 1  
fi

exit 0

### **Prompt Adaptation Template**

This template allows for flexible rule definition for cleanup tasks.

"Perform a cleanup of the directory '{directory\_path}'. First, do a dry run and list all files matching the pattern '{file\_pattern}' that are older than {days\_old} days and are NOT in the exclusion list: \[{exclusion\_list}\]. Await my confirmation before moving them to the quarantine directory '{quarantine\_path}'. Log every moved file to '{log\_file}'."

### **The Risk & Control Matrix**

The primary risk of any automated file deletion system is catastrophic, irreversible data loss. The entire design of this agent is a set of layered controls to mitigate this single, critical risk.

| Risk ID | Risk Description | Likelihood | Impact | Control Measure | Control Owner |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **JAN-01** | **Accidental Deletion of Critical Data:** A misconfiguration of the target path, retention period, or exclusion list causes the agent to delete critical operational or business data.37 | Low | Catastrophic | **1\. Quarantine Pattern (Recycle Bin):** This is the primary control. The agent *never* permanently deletes files. It only moves them to a quarantine directory. Permanent deletion must be a separate, manual, and highly restricted process. This provides a crucial recovery window. **2\. Mandatory Dry Run:** The agent's default mode is a "dry run" that only lists the files it would move. Destructive action requires an explicit \--force flag or interactive confirmation. **3\. Path Safety Guards:** The agent's prompt and underlying tool implementation must include logic to refuse to operate on high-risk root-level directories (e.g., /, /etc, /usr). | DevOps Team |
| **JAN-02** | **Violation of Data Retention Regulations:** The agent is configured to delete data (e.g., financial records, audit logs) before its legally mandated retention period has expired.39 | Medium | High | **1\. Policy as Code:** Data retention rules should not be based on ad-hoc script parameters. They should be defined in a version-controlled configuration file that is reviewed and approved by legal/compliance teams. The agent should read its rules from this file. **2\. Separate Archival Process:** The agent's documentation and training must clearly state it is for *ephemeral* data only (caches, temporary files). Data subject to legal retention must be handled by a separate *archival* system, not this deletion agent. | Compliance/Legal Team |
| **JAN-03** | **Incomplete Cleanup:** The agent fails to clean up files due to permission errors or other filesystem issues, leading to disk space exhaustion over time. | Medium | Medium | **1\. Robust Error Handling:** The agent must not terminate on a single file error. It should log the permission error for the specific file, increment a failure counter, and continue with the rest of the files. **2\. Post-run Alerting:** The invocation script must check the agent's summary output or audit log for failures. If any files failed to be moved, the script should trigger an alert to notify operators of the incomplete run. | DevOps Team |

### **Ethical Considerations**

* **Data Lifecycle Responsibility:** The automated deletion of data is a significant action. This agent must be deployed as part of a comprehensive, documented data retention policy that has been approved by relevant stakeholders, including legal and compliance teams. Using this agent to arbitrarily delete data without a governing policy is irresponsible.38  
* **Accountability and Auditability:** In the event of an incident, it is crucial to have an irrefutable record of what was deleted, when, and by what authority. The agent's mandatory, detailed audit logging is a critical ethical requirement. The log must be immutable and retained according to the organisation's own compliance standards.37  
* **"Defensible Deletion":** The process must be "legally defensible".38 This means the organisation must be able to prove that the deletion was part of a routine, policy-driven process, not a deliberate attempt to destroy evidence in response to litigation or an investigation. The combination of a formal policy, scheduled execution, and detailed audit logs provides this defensibility.

### **Failure Modes & Recovery**

* **Failure Mode: Incorrect Age Calculation**  
  * **Description:** The agent misinterprets file timestamps (e.g., due to timezone issues or relying on access time instead of modification time), causing it to select the wrong files for deletion.  
  * **Recovery Strategy:** The agent's logic must be standardised to use only the file's modification timestamp (mtime) in UTC. The "dry run" output should explicitly include the last modified date for each file it proposes to move, allowing the human operator to sanity-check the agent's age calculation before giving approval.  
* **Failure Mode: Quarantine Directory Fills Up**  
  * **Description:** The Janitor agent works correctly, but the separate process for purging the quarantine directory fails or is forgotten. Over time, the quarantine directory itself consumes all available disk space.  
  * **Recovery Strategy:** The invocation script for the Janitor agent should include a check on the available disk space in the quarantine volume. If the available space is below a critical threshold (e.g., 10%), the script should refuse to run the agent and instead send a high-priority alert to the operations team, warning them that the quarantine area requires attention. This acts as a circuit breaker to prevent the cleanup process from causing its own outage.  
* **Failure Mode: Race Condition with Log Rotation**  
  * **Description:** The Janitor agent runs at the same time as a traditional log rotation utility. The log rotator renames app.log to app.log.1, and at that exact moment, the Janitor agent's scan is in progress. Depending on the timing, the agent might miss the newly rotated file or incorrectly assess its age.  
  * **Recovery Strategy:** Use a locking mechanism. Before the Janitor agent begins its scan, it should create a lock file (e.g., /var/run/janitor.lock). Other system processes, like the log rotation script, should be configured to check for the existence of this lock file and delay their own execution if it is present. The Janitor agent must reliably remove the lock file upon completion or failure. This ensures that filesystem reorganisation tasks do not run concurrently.

## **Chapter 5: Core Agent Blueprint: The Automated Tester**

This blueprint outlines an agent that leverages the reasoning capabilities of a large language model to generate unit tests for source code. It acts as a "pair programmer" for Quality Assurance, accelerating the creation of test suites and helping developers adopt a Test-Driven Development (TDD) workflow.

### **Objective & Success Criteria**

* **Objective:** To create an agent that, given a specific Python function, analyses its logic, signature, and docstrings to generate a comprehensive and correct Pytest unit test file.  
* **Success Criteria:**  
  1. **Coverage:** The agent-generated tests achieve a minimum of 80% line coverage for the target function, as measured by a standard coverage tool.  
  2. **Correctness:** The generated tests pass without modification when run against a known-good implementation of the function.  
  3. **Fault Detection:** The agent generates at least one failing test when run against a deliberately faulty implementation of the function (e.g., one with an off-by-one error).  
  4. **Completeness:** The generated test suite includes tests for the "happy path" (normal inputs), common edge cases (e.g., None, empty lists, zero), and expected exceptions using pytest.raises.

### **Real-World Case Study**

A junior developer is tasked with writing a utility function to validate email addresses based on a complex regular expression. Unsure how to test all the edge cases of the regex, they invoke the /test agent and point it at their new function. The agent generates a test\_email\_validator.py file containing a dozen test cases, including tests for valid emails, emails with subdomains, emails with special characters, and various malformed inputs that should raise a ValueError. The developer reviews the comprehensive suite, learns about edge cases they hadn't considered, and gains confidence that their function is robust before submitting it for code review.

### **Agent Workflow Diagram**

Code snippet

flowchart TD  
    A \--\> B;  
    B \--\> C\[Isolate the target function's code block\];  
    C \--\> D;  
    subgraph Test Case Generation  
        D \--\> D1;  
        D \--\> D2;  
        D \--\> D3;  
    end  
    D1 & D2 & D3 \--\> E;  
    E \--\> F\[Generate Pytest code for each scenario, using \`assert\` for valid cases and \`pytest.raises\` for error cases\];  
    F \--\> G\[Assemble all generated test functions into a single, valid Python file with necessary imports\];  
    G \--\> H;  
    H \--\> I{User requested to run tests?};  
    I \-- No \--\> K\[End\];  
    I \-- Yes \--\> J\[Execute \`pytest\` on the newly created file and report results\];  
    J \--\> K;

### **The Custom Slash Command (tester.md)**

This file contains the prompt that guides the agent's test generation process. It is stored at \~/.claude\_agents/tester/tester.md.

You are an expert Senior Quality Assurance (QA) Engineer AI agent with deep expertise in Python and the Pytest framework. Your specialty is Test-Driven Development (TDD) and writing robust, comprehensive unit tests.

Your Goal:  
Analyse a given Python function and generate a complete Pytest test file that thoroughly validates its behaviour.  
**Your Tools:**

* read\_function\_code(file\_path: str, function\_name: str): Reads and returns the source code for a specific function from a file.  
* writeFile(path: str, content: str): Writes content to a file.  
* execute\_shell(command: str): Executes a shell command, like pytest.

**Step-by-Step Instructions:**

1. **Analyse the Function:** The user will provide a file path and a function name. Use read\_function\_code to get the source code. Carefully analyse its signature (parameters, type hints), its docstring, and its internal logic.  
2. **Think Like a Tester:** Before writing any code, think step-by-step about the test strategy. Consider the following categories:  
   * **Happy Path:** What are 2-3 examples of typical, valid inputs and their expected outputs?  
   * **Edge Cases:** What are the boundary conditions? Consider None, empty strings/lists, 0, negative numbers, very large numbers, etc.  
   * **Error Conditions:** What inputs should cause the function to raise an exception? Identify the specific exception type (ValueError, TypeError, etc.) that should be raised.  
3. Generate Test Code:  
   a. Create a new Python script. Import pytest and the function you are testing.  
   b. For each test case you identified, write a corresponding test\_ function.  
   c. Use simple assert function(input) \== expected\_output for happy path and edge case tests.  
   d. For error condition tests, use the pytest.raises context manager. For example: with pytest.raises(ValueError): function(invalid\_input).  
   e. Ensure each test function has a descriptive name (e.g., test\_function\_with\_empty\_list).  
4. **Write the Test File:** Use the writeFile tool to save the complete, runnable Pytest script to a new file. The filename should be prefixed with test\_, as is standard for Pytest discovery.  
5. **Optional: Run Tests:** If the user requests it, use execute\_shell to run pytest on the file you just created and report the output.

**Important Rules:**

* **Isolate Tests:** Each test function must be independent. Do not rely on state from other tests.  
* **Be Explicit:** Use clear and descriptive variable names for inputs and expected outputs.  
* **Follow Best Practices:** Adhere to standard Python (PEP 8\) and Pytest conventions.

### **The Invocation Script (tester.sh)**

This script provides a command-line interface for the tester agent. It is stored at \~/.claude\_agents/tester/tester.sh.

Bash

\#\!/bin/bash  
\# Invocation script for the Automated Tester agent.

\# \--- Configuration \---  
AGENT\_LOG\_FILE="/var/log/claude\_agents\_tester.log"  
AGENT\_COMMAND\_FILE="$HOME/.claude\_agents/tester/tester.md"

\# \--- Command Line Arguments \---  
FILE\_PATH=$1  
FUNCTION\_NAME=$2  
RUN\_TESTS=${3:-false} \# Optional third argument, e.g., 'true'

\# \--- Usage \---  
if \[ "$\#" \-lt 2 \]; then  
    echo "Usage: $0 \<file\_path\> \<function\_name\> \[run\_tests\_boolean\]"  
    echo "Example: $0 src/utils.py calculate\_tax true"  
    exit 1  
fi

\# \--- Pre-flight Checks \---  
if; then  
    echo "Error: Source file '$FILE\_PATH' not found." | tee \-a "$AGENT\_LOG\_FILE"  
    exit 1  
fi

\# \--- Audit Logging \---  
echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- User '$USER' initiated /tester agent." \>\> "$AGENT\_LOG\_FILE"  
echo "  \- Target File: $(realpath "$FILE\_PATH")" \>\> "$AGENT\_LOG\_FILE"  
echo "  \- Target Function: $FUNCTION\_NAME" \>\> "$AGENT\_LOG\_FILE"

\# \--- Agent Invocation \---  
OUTPUT\_TEST\_FILE="test\_$(basename "$FILE\_PATH")"  
PROMPT="You are a QA expert. Generate a Pytest test file named '${OUTPUT\_TEST\_FILE}' for the function '${FUNCTION\_NAME}' in the file '${FILE\_PATH}'. After generating the file, if I requested it, run the tests."

echo "Invoking tester agent for '${FUNCTION\_NAME}'..."  
claude /tester \--prompt "$PROMPT"

\# \--- Post-flight Actions \---  
if \[ $? \-ne 0 \]; then  
    echo "Error: Agent execution failed."  
    echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- Agent /tester failed during generation." \>\> "$AGENT\_LOG\_FILE"  
    exit 1  
fi

echo "Agent generated test file at '$OUTPUT\_TEST\_FILE'."  
echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- Agent /tester completed generation." \>\> "$AGENT\_LOG\_FILE"

if; then  
    echo "Running generated tests..."  
    pytest "$OUTPUT\_TEST\_FILE"  
    if \[ $? \-eq 0 \]; then  
        echo "All generated tests passed."  
    else  
        echo "One or more generated tests failed."  
    fi  
fi

exit 0

### **Prompt Adaptation Template**

This template allows for more specific test generation requirements.

"You are a QA expert. Analyse the function '{function\_name}' in the file '{file\_path}'. Generate a complete Pytest test file named '{output\_test\_file}'. The tests must be parameterised using '@pytest.mark.parametrize' to cover the following input/output pairs: \[{test\_cases\_json}\]. Additionally, generate tests to verify that the function correctly raises a '{expected\_exception}' when given invalid input."

### **The Risk & Control Matrix**

The primary risk of AI-generated tests is not that they are wrong, but that they are superficially correct, creating a dangerous illusion of safety and leading to "automation bias."

| Risk ID | Risk Description | Likelihood | Impact | Control Measure | Control Owner |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **TEST-01** | **False Confidence / Incomplete Coverage:** The agent generates plausible-looking tests that cover basic cases but miss subtle business logic, complex edge cases, or security vulnerabilities. This leads to a false sense of security.42 | High | High | **1\. Mandatory Human Review:** AI-generated tests must *always* be treated as a first draft. The development process must include a mandatory code review step where a human developer reviews, augments, and approves the generated tests before they are merged. **2\. Treat AI as a Pair Programmer:** Frame the agent's role as a helpful assistant that generates boilerplate, not as an autonomous QA authority. The prompt should encourage this by asking it to "suggest test cases for review." | Development Team Lead |
| **TEST-02** | **Test Suite Bias:** The agent, reflecting biases in its training data, consistently fails to generate tests for certain categories of issues, such as accessibility, internationalisation, or specific types of security flaws.44 | Medium | High | **1\. Explicit Prompting for Diversity:** The agent's prompt should be augmented with explicit instructions to consider diverse inputs, such as non-ASCII characters for internationalisation or very large numbers for overflow checks. **2\. Hybrid Testing Strategy:** Do not rely solely on AI-generated unit tests. Maintain a balanced testing pyramid with manual exploratory testing and integration tests designed by humans to cover areas where AI is weak. | QA Team |
| **TEST-03** | **Generation of "Flaky" Tests:** The agent generates tests that are not isolated and depend on external state (e.g., time, network, database), causing them to fail intermittently and eroding trust in the test suite.46 | Medium | Medium | **1\. Mandate Mocking:** The agent's prompt must explicitly instruct it to use mocking and patching libraries (e.g., Python's unittest.mock, freezegun) to isolate the unit under test from its dependencies. **2\. Automated Flakiness Detection:** The CI/CD pipeline should track test results over time. If a test passes and fails inconsistently across different runs of the same code, it should be automatically flagged as "flaky" and quarantined for human review. | Developer |

### **Ethical Considerations**

* **Accountability:** If a production bug is missed by an AI-generated test suite, the accountability does not lie with the AI. It lies with the human developer who reviewed and approved the tests. The team's processes and culture must reinforce that AI is a tool to augment human expertise, not replace human responsibility.7  
* **Skill Erosion (Over-reliance):** A significant long-term risk is that developers may become over-reliant on the agent for test creation, leading to an atrophy of their own critical testing and debugging skills. To mitigate this, the agent should be used as a teaching tool. Its output can be used in training sessions to show junior developers what a comprehensive test suite looks like.44  
* **Intellectual Property:** The agent must be instructed not to generate test cases that use or replicate proprietary data or copyrighted algorithms from its training set. Test data should be synthetic and directly related to the function under test.44

### **Failure Modes & Recovery**

* **Failure Mode: Syntactically Incorrect Test Code**  
  * **Description:** The agent generates a Python file that contains syntax errors, causing the test runner to fail before any tests can be executed.  
  * **Recovery Strategy:** Implement a self-correction loop. The invocation script should first run a linter (e.g., ruff check \--select E999) on the generated file. If a syntax error is detected, the script should automatically re-invoke the agent with the original prompt, appended with: "The code you previously generated had the following syntax error: {linter\_output}. Please correct the syntax and provide the full, corrected test file." This loop can be repeated 2-3 times.  
* **Failure Mode: Infinite Loop or Timeout during Generation**  
  * **Description:** When analysing a very complex or poorly written function (e.g., with deep recursion or convoluted logic), the agent's reasoning process consumes too much time or tokens and times out.  
  * **Recovery Strategy:**  
    1. **Set Timeouts:** The invocation script must wrap the claude command with a timeout (e.g., timeout 300s claude...).  
    2. **Simplify the Task:** If a timeout occurs, the recovery process should be to simplify the problem for the agent. Instead of asking for a complete test suite at once, the user can prompt the agent to generate tests for just one category at a time: "First, just write the happy path tests for function X." This breaks the complex reasoning task into smaller, more manageable chunks.  
* **Failure Mode: Inability to Import Target Function**  
  * **Description:** The agent generates a test file that fails immediately because the import statement for the function under test is incorrect, often due to complex project structures or circular dependencies.  
  * **Recovery Strategy:** The agent's prompt should include an instruction to determine the correct import path based on the project's root directory and the file's location. The invocation script should pass the project root as a parameter.

Prompt Snippet:"The project root is at '{project\_root}'. Given that the function is in '{file\_path}', determine the correct relative import statement to use in the test file."

## **Chapter 6: Core Agent Blueprint: The CI/CD Security Analyst**

This blueprint details an agent designed to be a vigilant, automated security reviewer within a Continuous Integration/Continuous Delivery (CI/CD) pipeline. It performs static analysis on every code change, identifying potential vulnerabilities before they can be merged into the main codebase, effectively "shifting left" the practice of security.

### **Objective & Success Criteria**

* **Objective:** To create an agent that integrates seamlessly into a CI/CD workflow, performs Static Application Security Testing (SAST) on new or modified code, and provides immediate, actionable feedback to developers.  
* **Success Criteria:**  
  1. **Pipeline Integration:** The agent is successfully triggered and executes on 100% of pull requests submitted to the repository.  
  2. **Vulnerability Detection:** The agent correctly identifies known vulnerability patterns (e.g., hardcoded secrets, SQL injection, use of insecure functions) in submitted code.  
  3. **Gating Mechanism:** The CI/CD build fails (is "gated") if the agent detects any new vulnerabilities with a severity of "High" or "Critical".  
  4. **Actionable Feedback:** The agent posts its findings as a clear, concise comment on the pull request, including the vulnerability type, the file path, the line number, and a brief remediation suggestion.

### **Real-World Case Study**

A cloud services company enforces a strict DevSecOps culture. They have integrated the /secure-scan agent into their GitLab CI pipeline. When a developer pushes commits to a merge request, a new pipeline job is initiated. The agent checks out the code, runs the bandit SAST tool against the Python codebase, and compares the results to a baseline scan of the target main branch. If a new high-severity issue, such as the use of a weak cryptographic algorithm, is detected, the agent fails the pipeline job. It then uses the GitLab API to post a comment on the merge request, pinpointing the exact line of problematic code. This immediate feedback loop allows the developer to fix the security issue before a human reviewer even sees the code, dramatically reducing the time and cost of remediation.48

### **Agent Workflow Diagram**

Code snippet

flowchart TD  
    A \--\> B\[Checkout base branch (e.g., 'main')\];  
    B \--\> C;  
    C \--\> D\[Checkout feature branch\];  
    D \--\> E;  
    E \--\> F\[Compare new.json with baseline.json to identify \*new\* issues\];  
    F \--\> G{New issues found?};  
    G \-- No \--\> H;  
    G \-- Yes \--\> I\[Filter new issues by severity \>= HIGH\];  
    I \--\> J{High/Critical severity issues remain?};  
    J \-- No \--\> H;  
    J \-- Yes \--\> K\[Format remaining issues into a Markdown report\];  
    K \--\> L;  
    L \--\> M\[Log 'Critical vulnerabilities found' and exit with status 1 (Failure)\];

### **The Custom Slash Command (secure-scan.md)**

This file defines the agent's logic for performing a differential security scan. It is stored at \~/.claude\_agents/secure-scan/secure-scan.md.

You are an automated DevSecOps Analyst AI agent. Your mission is to perform static code analysis and identify *new* security vulnerabilities introduced in a code change, preventing them from reaching production.

Your Goal:  
Compare a security scan of a feature branch against a baseline scan of the main branch and report only the newly introduced, high-severity vulnerabilities.  
**Your Tools:**

* execute\_shell(command: str): Executes a shell command and returns its output.  
* read\_json(path: str): Reads and parses a JSON file.  
* post\_pr\_comment(comment\_body: str): Posts a comment to the current pull request.

**Step-by-Step Instructions:**

1. **Establish Baseline:** The user will provide the path to a baseline security report (baseline.json). Use read\_json to load it into memory. This report contains the vulnerabilities present in the main branch.  
2. Run New Scan:  
   a. The user will specify the SAST command to run (e.g., bandit \-r. \-f json \-o new.json).  
   b. Use execute\_shell to run this command.  
   c. Use read\_json to load the results from the newly created report (new.json).  
3. Perform Differential Analysis:  
   a. Compare the list of vulnerabilities in the new report against the baseline report.  
   b. Create a final list containing only the vulnerabilities that are present in the new report but NOT in the baseline report. This is the list of newly introduced issues.  
4. Filter by Severity:  
   a. From the list of new issues, filter out any that have a severity of LOW or MEDIUM.  
   b. The remaining list contains only new, high-impact vulnerabilities that require immediate attention.  
5. Report and Act:  
   a. If the final filtered list is empty, the job is successful. Print a success message and terminate.  
   b. If the list contains vulnerabilities, format them into a clear Markdown table for a pull request comment. The table should include columns for Severity, File, Line, and Issue.  
   c. Use the post\_pr\_comment tool to post this table to the pull request.  
   d. After posting the comment, explicitly state that the build is failing due to these critical security issues.

**Important Rules:**

* **Focus on the Delta:** Your primary value is in reducing noise. Do not report pre-existing vulnerabilities from the baseline. Only report what is new in this change.  
* **Be Actionable:** The report must be clear and provide enough context (file, line number) for a developer to immediately locate and fix the problem.  
* **Enforce the Gate:** If high-severity issues are found, you must signal a failure.

### **The Invocation Script (secure-scan.sh)**

This script is designed to be executed by a CI/CD runner. It is stored at \~/.claude\_agents/secure-scan/secure-scan.sh.

Bash

\#\!/bin/bash  
\# Invocation script for the CI/CD Security Analyst agent.  
\# This script assumes it's running in a CI environment where a PR has triggered it.

set \-e \# Exit immediately if a command exits with a non-zero status.

\# \--- Configuration \---  
AGENT\_LOG\_FILE="claude\_security\_scan.log"  
AGENT\_COMMAND\_FILE="$HOME/.claude\_agents/secure-scan/secure-scan.md"  
SAST\_COMMAND="bandit \-r. \-f json" \# Example for Python/Bandit

\# \--- CI Environment Variables (examples for GitHub Actions) \---  
BASE\_BRANCH=${GITHUB\_BASE\_REF:-"main"}  
FEATURE\_BRANCH=${GITHUB\_HEAD\_REF}  
PR\_NUMBER=${GITHUB\_REF\#\#\*/merge}

\# \--- Audit Logging \---  
echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- Starting /secure-scan agent." \> "$AGENT\_LOG\_FILE"  
echo "  \- Base Branch: $BASE\_BRANCH" \>\> "$AGENT\_LOG\_FILE"  
echo "  \- Feature Branch: $FEATURE\_BRANCH" \>\> "$AGENT\_LOG\_FILE"  
echo "  \- PR Number: $PR\_NUMBER" \>\> "$AGENT\_LOG\_FILE"

\# \--- Baseline Scan \---  
echo "Generating baseline scan for branch '$BASE\_BRANCH'..."  
git checkout "$BASE\_BRANCH"  
$SAST\_COMMAND \-o baseline.json |

| echo "Baseline scan found issues, proceeding with diff."  
git checkout "$FEATURE\_BRANCH" \# Switch back to the feature branch

\# \--- Agent Invocation \---  
PROMPT="Perform a differential security scan. The baseline report is at 'baseline.json'. The command to generate the new report is '${SAST\_COMMAND} \-o new.json'. If new high-severity issues are found, post them as a comment on PR \#${PR\_NUMBER} and then fail."

echo "Invoking security analyst agent..."  
claude /secure-scan \--prompt "$PROMPT"

\# The agent's internal logic will cause an exit(1) if it finds issues,  
\# which will fail the CI job due to 'set \-e'.  
EXIT\_CODE=$?

if; then  
    echo "Security scan passed. No new high-severity vulnerabilities found."  
    echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- /secure-scan completed successfully." \>\> "$AGENT\_LOG\_FILE"  
else  
    echo "Security scan failed. New high-severity vulnerabilities detected."  
    echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- /secure-scan failed due to new vulnerabilities." \>\> "$AGENT\_LOG\_FILE"  
fi

exit $EXIT\_CODE

### **Prompt Adaptation Template**

This template allows for customising the scanner's behaviour and thresholds.

"As a security analyst, scan the codebase in the current directory using the command '{sast\_command}'. Analyse the output and report only new vulnerabilities with a severity of '{severity\_threshold}' or higher that are not present in the baseline scan '{baseline\_scan\_file}'. The report should be formatted as '{output\_format}' (e.g., 'Markdown', 'JSON', 'SARIF') and posted to '{reporting\_endpoint}'."

### **The Risk & Control Matrix**

The greatest risk in automated CI/CD security is not tool failure, but developer rejection due to friction. If the tool is noisy, slow, or perceived as a blocker, teams will find ways to bypass it, rendering it useless.

| Risk ID | Risk Description | Likelihood | Impact | Control Measure | Control Owner |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **SEC-01** | **Alert Fatigue:** The SAST tool generates a high volume of false positives or low-priority warnings, causing developers to ignore all alerts, including legitimate ones.50 | High | High | **1\. Differential Scanning:** The agent's core logic *must* only report vulnerabilities newly introduced in the pull request. This is the single most important control against noise. **2\. Customisable Rulesets:** The SAST tool's configuration must be tailored to the project's tech stack and risk profile. Disable rules that are irrelevant or have a high false-positive rate. **3\. In-code Suppression:** Provide a mechanism for developers to suppress a specific finding they have reviewed and deemed a false positive (e.g., via a \# nosec comment). The agent must respect these suppression comments. | Security Team |
| **SEC-02** | **Pipeline Slowdown:** The security scan takes too long to complete, significantly increasing CI/CD pipeline duration and frustrating developers who are waiting for feedback.48 | Medium | Medium | **1\. Incremental Scanning:** Configure the agent and SAST tool to scan only the files that have been changed in the pull request, rather than the entire codebase. This dramatically reduces scan time. **2\. Asynchronous Scans:** For very large projects where even incremental scans are slow, run the security scan as an asynchronous, non-blocking job. It would still post comments but would not "gate" the merge, trading some prevention for velocity. | DevOps Team |
| **SEC-03** | **Insufficient Tool Coverage (False Negatives):** The SAST tool is misconfigured or lacks rules for a specific type of vulnerability (e.g., a new library with known exploits), giving a false sense of security.52 | Medium | High | **1\. Layered Security:** SAST is not a silver bullet. The CI/CD pipeline must include other automated security checks, such as Software Composition Analysis (SCA) for vulnerable dependencies and Dynamic Application Security Testing (DAST) for runtime issues. **2\. Regular Ruleset Updates:** The SAST tool's ruleset must be updated automatically and regularly to include checks for the latest known vulnerabilities. | Security Team |
| **SEC-04** | **Pipeline Compromise:** An attacker gains control of the CI/CD environment and modifies the security agent's script to bypass checks or exfiltrate secrets.6 | Low | Critical | **1\. Immutable Runner Environments:** CI/CD jobs should run in ephemeral, isolated environments (like containers) that are destroyed after each run. **2\. Strict Access Controls:** Enforce the principle of least privilege on the CI/CD system itself. The security agent's job should have read-only access to code and should not have access to production deployment secrets. **3\. Code Signing:** Implement code signing for build artifacts to ensure that what is scanned is what gets deployed. | DevOps Team |

### **Ethical Considerations**

* **Accountability and Blame:** An automated security tool can create a culture of blame if not implemented carefully. The agent's feedback should be framed constructively, as a helpful suggestion from a "teammate" rather than a punitive judgment. The goal is to empower developers to write secure code, not to penalise them for mistakes.54  
* **Bias in Tooling:** Security scanning tools are not infallible. They may have inherent biases, favouring certain coding styles or being more effective on code written by native English speakers. The security team must be aware of these potential biases and be open to feedback from developers if a tool is perceived as being unfair or consistently wrong.55  
* **Transparency:** The agent must be fully transparent about its operations. The PR comment should state exactly which tool was used (e.g., "Bandit v1.7.5"), which ruleset was applied, and provide a link to the full, unfiltered scan report. This allows developers to understand the context of a finding and, if necessary, challenge its validity.

### **Failure Modes & Recovery**

* **Failure Mode: Baseline Scan Failure**  
  * **Description:** The SAST tool fails when scanning the base (main) branch, preventing the agent from establishing a baseline for comparison.  
  * **Recovery Strategy:** The invocation script should be configured to treat a baseline scan failure as a non-fatal warning. It should log the error and proceed with the scan of the feature branch. In this mode, the agent's prompt should be dynamically altered to report *all* high-severity findings, not just the new ones, with a clear disclaimer: "Warning: Unable to generate a baseline. Reporting all findings on this branch." This ensures that security scanning still occurs, even if the differential analysis is temporarily unavailable.  
* **Failure Mode: Misconfiguration Leads to Zero Findings**  
  * **Description:** A misconfiguration in the SAST tool (e.g., an incorrect path in an exclusion rule) causes it to scan no files and report zero vulnerabilities, leading the agent to incorrectly pass the build.  
  * **Recovery Strategy:** Implement a sanity check. The agent's logic should verify that the SAST tool's report indicates a non-zero number of files were scanned. If it reports that zero files were scanned, the agent must treat this as a critical error, fail the build, and report a "Misconfiguration Detected" error. This prevents a silent failure from giving a false sense of security.  
* **Failure Mode: API Rate Limiting**  
  * **Description:** In a busy repository with many pull requests, the agent's attempts to post comments via the platform's API (e.g., GitHub API) are rate-limited.  
  * **Recovery Strategy:** The agent's post\_pr\_comment tool must be implemented with a retry mechanism that respects API rate limit headers. It should use an exponential backoff strategy when it receives a rate-limiting error (e.g., HTTP 429). Furthermore, for multiple findings, the agent should be instructed to aggregate all findings into a single, concise comment rather than posting one comment per finding, which minimises API calls.

## **Chapter 7: Advanced Blueprint: The Adaptive Learning Agent**

This advanced blueprint moves beyond static, pre-programmed agents to a system capable of self-improvement. It specifies an agent that learns and adapts its behaviour over time by incorporating human feedback. This pattern is foundational for creating AI systems that become more aligned, accurate, and useful through interaction, drawing heavily on the principles of Reinforcement Learning from Human Feedback (RLHF).

### **Objective & Success Criteria**

* **Objective:** To create a two-part agent system (a "Worker" agent and a "Meta" agent) that refines its internal prompt for a specific, subjective task (e.g., summarising complex legal documents) based on structured ratings provided by human experts.  
* **Success Criteria:**  
  1. **Performance Improvement:** After 100 rated interactions, the Worker agent's average user rating (on a 1-5 scale for 'Clarity' and 'Accuracy') demonstrates a statistically significant increase of at least 1.0 point.  
  2. **Failure Mode Reduction:** The frequency of a specific, tracked failure mode (e.g., feedback tagged as "missed key clause") is reduced by at least 50% after the Meta agent has performed five learning updates.  
  3. **Alignment:** The updated prompts generated by the Meta agent demonstrably incorporate instructions that address common negative feedback patterns.

### **Real-World Case Study**

A customer support organisation uses an AI agent to generate the first draft of responses to complex technical support tickets. Initially, the drafts were generic. They implemented an adaptive learning system where support engineers could rate each draft on a scale of 1-5 and provide a short reason for their rating (e.g., "too technical," "missed the user's real question"). Every night, a Meta agent analyses the day's feedback. It discovered that low-rated responses often failed to acknowledge the user's frustration. The Meta agent updated the Worker's prompt to include a new instruction: "Always begin the response by validating the user's reported problem and expressing empathy." Over several weeks, this self-correcting loop led to a measurable increase in the quality of first-draft responses and a reduction in the time engineers spent editing them.

### **Agent Workflow Diagram**

Code snippet

flowchart TD  
    subgraph Worker Agent \- Real-time Interaction  
        A\[User provides input text\] \--\> B;  
        B \--\> C;  
        C \--\> D;  
        D \--\> E\[Human provides feedback F (e.g., ratings, tags, corrections)\];  
        E \--\> F\_DB;  
        E \-- Store (Input, P\_n, S, F) \--\> F\_DB;  
    end

    subgraph Meta Agent \- Asynchronous Learning Cycle  
        G \--\> H;  
        H \--\> I\["Meta agent analyses feedback for patterns (e.g., common reasons for low ratings)"\];  
        I \--\> J\[Meta agent generates a new, improved prompt P\_n+1 designed to mitigate failures\];  
        J \--\> K{Human-in-the-Loop Approval};  
        K \-- Approve \--\> L;  
        J \-- Update prompt \--\> L;  
        K \-- Reject \--\> M;  
    end

### **The Custom Slash Command (adaptive-summariser.md)**

This is the prompt for the "Worker" agent. It is designed to be dynamically updated. It is stored in a database or file store, not a static .md file.

# **Prompt Version: 1.0**

# **Base Instructions**

You are an expert legal assistant. Your task is to summarise the provided legal document. The summary should be clear, concise, and accurate.

# **Dynamic Instructions (Updated by Meta Agent)**

* Focus on identifying the primary obligations and liabilities of each party.  
* Do not include boilerplate sections like 'Definitions' unless they are highly unusual.  
* The tone should be neutral and objective.

### **The Invocation Script (adaptive-summariser.sh)**

This script manages the interactive session with the user, capturing both the agent's output and the user's feedback.

Bash

\#\!/bin/bash  
\# Interactive script for the Adaptive Learning Agent.

\# \--- Configuration \---  
PROMPT\_FILE="/etc/claude\_agents/prompts/legal\_summariser\_v1.0.md"  
FEEDBACK\_DB="/var/lib/claude\_agents/feedback.sqlite"  
INPUT\_DOCUMENT=$1

\# \--- Pre-flight Checks \---  
if; then  
    echo "Usage: $0 \<path\_to\_document\>"  
    exit 1  
fi

\# \--- Agent Invocation \---  
echo "Generating summary for $INPUT\_DOCUMENT..."  
SUMMARY=$(claude \--prompt\_file "$PROMPT\_FILE" \--input\_file "$INPUT\_DOCUMENT")

\# \--- Feedback Capture \---  
echo \-e "\\n--- AGENT SUMMARY \---"  
echo "$SUMMARY"  
echo \-e "\\n--- PLEASE PROVIDE FEEDBACK \---"  
read \-p "Rate Accuracy (1-5): " accuracy\_rating  
read \-p "Rate Clarity (1-5): " clarity\_rating  
read \-p "Enter optional comments/tags (e.g., 'missed key clause'): " comments

\# \--- Store Feedback \---  
\# In a real system, this would be a structured database insert.  
sqlite3 "$FEEDBACK\_DB" "INSERT INTO feedback (document, prompt, summary, accuracy, clarity, comments) VALUES ('$(cat $INPUT\_DOCUMENT)', '$(cat $PROMPT\_FILE)', '$SUMMARY', $accuracy\_rating, $clarity\_rating, '$comments');"

echo "Thank you for your feedback. It will be used to improve the agent."  
exit 0

### **Prompt Adaptation Template (for Meta Agent)**

This is the prompt used by the learning component of the system.

"You are an expert in prompt engineering and reinforcement learning. You will be given a JSON object containing the 50 most recent interactions with a summarisation agent. Each interaction includes the prompt used, the generated summary, and the human's feedback (ratings and comments). Your task is to identify the most common reasons for low ratings and then rewrite the 'Dynamic Instructions' section of the original prompt to mitigate these failures. Output only the new 'Dynamic Instructions' section. For example, if many comments say 'too long', you should add an instruction like '- Keep the summary under 250 words.'"

### **The Risk & Control Matrix**

Self-improving systems introduce second-order risks that are not present in static agents. The primary dangers are **reward hacking**, where the agent optimises for a flawed metric, and **catastrophic forgetting**, where learning new skills erases old ones.

| Risk ID | Risk Description | Likelihood | Impact | Control Measure | Control Owner |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **ADAPT-01** | **Reward Hacking:** The agent learns to "game" the feedback system. For example, it discovers that generating very short, generic, and non-committal summaries always avoids low accuracy scores, thus increasing its average rating while decreasing its actual usefulness.56 | High | High | **1\. Multi-dimensional Feedback:** Use a structured feedback mechanism that captures multiple dimensions (e.g., separate ratings for accuracy, clarity, and completeness). This makes it harder for the agent to optimise for a single, simple proxy. **2\. Human Oversight of Learning:** The Meta agent only *proposes* a new prompt. A human expert *must* review and approve the new prompt before it is deployed into production. This HITL gate is the ultimate defence against reward hacking. | AI Architect |
| **ADAPT-02** | **Catastrophic Forgetting:** In learning to satisfy a new pattern of feedback (e.g., "be more concise"), the Meta agent generates a new prompt that causes the Worker agent to forget a foundational skill (e.g., "be factually accurate").58 | Medium | High | **1\. Golden Set Regression Testing:** Maintain a curated "golden set" of diverse, high-quality input-output examples. Before a new prompt is approved, it must be automatically run against this set. If performance on the golden set degrades by more than a set threshold (e.g., 5%), the new prompt is automatically rejected. **2\. Incremental Prompt Changes:** The Meta agent's prompt should instruct it to make small, incremental changes to the existing prompt rather than rewriting it from scratch. This reduces the risk of drastic, unintended shifts in behaviour. | QA Team |
| **ADAPT-03** | **Feedback Loop Instability:** The agent's behaviour oscillates or diverges instead of converging to a better state, as it over-corrects for noisy or conflicting feedback.60 | Medium | Medium | **1\. Champion/Challenger Deployment:** A newly approved prompt (the "challenger") is initially deployed to only a small fraction of live traffic (e.g., 5%). It is only promoted to the "champion" (100% of traffic) if it demonstrates a statistically significant performance improvement over the existing prompt. This prevents a bad update from impacting all users. **2\. Learning Rate Control:** The Meta agent should be configured to update the prompt only after a sufficiently large batch of new feedback (e.g., 100 data points) is collected. This smooths out the impact of individual noisy ratings. | DevOps Team |
| **ADAPT-04** | **Data Poisoning / Adversarial Feedback:** A malicious user intentionally provides incorrect feedback to steer the agent towards generating biased, incorrect, or harmful content.55 | Low | High | **1\. Anomaly Detection in Feedback:** The Meta agent should include a step to identify and down-weight or exclude feedback from users whose ratings are statistical outliers compared to the expert consensus. **2\. Rater Reputation Scoring:** Implement a system to track rater agreement over time. Feedback from raters who consistently disagree with the consensus can be given a lower weight in the learning process. | Security Team |

### **Ethical Considerations**

* **Bias Amplification:** The system is a direct reflection of the feedback it receives. If the human experts providing feedback share a collective bias, the agent will learn, codify, and amplify that bias. It is ethically imperative that the pool of human raters is diverse and trained to identify and avoid their own biases.62  
* **Transparency of Learning:** Users interacting with the system, especially those providing feedback, must be made aware that their input is being used to retrain the AI. A clear disclaimer such as, "Your feedback helps our AI to learn and improve," should be present in the UI.65  
* **Accountability for Learned Behaviour:** While the agent learns autonomously, the organisation deploying it remains fully accountable for its behaviour. The HITL approval gate for new prompts is a critical accountability mechanism, creating a clear audit trail of the human decision to alter the agent's behaviour. The person who approves a new prompt is accountable for the consequences of that change.

### **Failure Modes & Recovery**

* **Failure Mode: Prompt Degradation**  
  * **Description:** The Meta agent, in an attempt to optimise, generates a prompt that is overly complex, self-contradictory, or nonsensical, leading to a sharp decline in the Worker agent's performance.  
  * **Recovery Strategy:**  
    1. **Prompt Versioning and Instant Rollback:** Every approved prompt must be versioned and stored. The system must have a one-click mechanism for an operator to instantly roll back the active prompt to any previous version.  
    2. **Automated Sanity Check:** Before a new prompt is even presented for human review, it should be run against a small set of 5-10 "sanity check" examples. If it produces gibberish or fails catastrophically on these, it should be automatically rejected without requiring human time.  
* **Failure Mode: Insufficient or Low-Quality Feedback**  
  * **Description:** The system fails to improve because not enough feedback is being collected, or the feedback provided is low-effort (e.g., users always give a '3' rating with no comments).  
  * **Recovery Strategy:** This is a human/process problem, not just a technical one.  
    1. **Incentivise Quality Feedback:** The UI for feedback collection should be as frictionless as possible. Consider gamification or other incentives for providing detailed, high-quality feedback.  
    2. **Active Learning:** Instead of waiting for feedback passively, the agent can be programmed to identify summaries it is "uncertain" about (e.g., where its internal confidence score is low) and proactively request feedback for those specific outputs. This focuses the limited human attention where it is most needed.

## **Chapter 8: Advanced Blueprint: The Collaborative Multi-Agent Orchestrator**

This blueprint specifies a sophisticated multi-agent system architecture. It moves beyond the capabilities of a single, monolithic agent by employing a "team" of specialised agents that collaborate to solve complex, multi-domain problems. A central "Supervisor" agent acts as an orchestrator, decomposing a high-level goal into a plan and delegating sub-tasks to appropriate "Worker" agents. This pattern is essential for tackling tasks that require diverse skills, parallel execution, and modular reasoning.

### **Objective & Success Criteria**

* **Objective:** To create a multi-agent system that can successfully plan and execute a complex research task: "Generate a comprehensive market analysis report and accompanying presentation for Company X's performance in the last fiscal quarter."  
* **Success Criteria:**  
  1. **Successful Decomposition:** The Supervisor agent correctly decomposes the high-level goal into a logical sequence of sub-tasks (e.g., fetch financial statements, analyse revenue, research news sentiment, create presentation).  
  2. **Correct Delegation:** Each sub-task is successfully routed to the correct specialist agent (e.g., financial data is handled by the AnalystAgent, web searches by the ResearchAgent).  
  3. **End-to-End Completion:** The system successfully executes the full workflow, with the PresenterAgent generating a final presentation file that correctly synthesises the outputs from the other agents.  
  4. **Fault Tolerance:** The system can recover from a transient failure of a single worker agent (e.g., a network error during a web search) by retrying the task.

### **Real-World Case Study**

A software development team uses a multi-agent system to automate their release process. A developer issues the command: /release version 2.5. The Supervisor agent receives this and creates a plan. It first delegates to the TestAgent to run the full regression suite. Upon success, it delegates to the DocsAgent to regenerate API documentation. Concurrently, it asks the ChangelogAgent to compile a list of changes from Git commits. Finally, after all preceding steps are complete, it delegates to the DeployAgent, which takes the build artifact, the new docs, and the changelog, and pushes them to the production environment. This orchestration of specialised agents ensures a consistent, reliable, and fully documented release process.

### **Agent Workflow Diagram**

Code snippet

flowchart TD  
    subgraph SupervisorAgent  
        A \--\> B;  
        B \--\> C{For each step in plan};  
        C \--\> D;  
        D \--\> E;  
        E \--\> F{Wait for result from agent};  
        F \--\> G{Result successful?};  
        G \-- Yes \--\> C;  
        G \-- No \--\> H;  
        C \-- Plan complete \--\> I;  
        I \--\> J;  
        J \--\> K\[End\];  
    end

    subgraph MessageBus  
        E \-- Task \--\> MB;  
        MB \-- "Fetch financial data for X" \--\> ResearchAgent;  
        MB \-- "Analyse JSON data" \--\> AnalystAgent;  
        MB \-- "Create.pptx slides" \--\> PresenterAgent;  
        ResearchAgent \-- Result \--\> MB\_Result;  
        AnalystAgent \-- Result \--\> MB\_Result;  
        PresenterAgent \-- Result \--\> MB\_Result;  
        MB\_Result \-- Result \--\> F;  
    end

    subgraph WorkerAgents  
        ResearchAgent;  
        AnalystAgent;  
        PresenterAgent;  
    end

### **The Custom Slash Command (Agent Prompts)**

This system requires a separate prompt file for each agent role.

supervisor.md:  
You are a highly efficient Project Manager AI. Your job is to take a complex user goal, break it down into a logical plan of discrete steps, and delegate each step to a team of specialist agents.  
**Your Team:**

* ResearchAgent: Expert at finding information from the web and APIs.  
* AnalystAgent: Expert at analysing structured data (JSON, CSV) and generating insights.  
* PresenterAgent: Expert at creating presentation slides from text and data.

**Your Tool:**

* delegate\_task(agent\_name: str, task\_description: str, context: dict): Assigns a task to a specialist agent and returns the result.

**Step-by-Step Instructions:**

1. **Understand the Goal:** Analyse the user's request.  
2. **Create a Plan:** Think step-by-step to create a sequence of tasks needed to achieve the goal. Identify dependencies (e.g., you must research data before you can analyse it).  
3. Execute the Plan: For each step in your plan:  
   a. Choose the correct agent from your team.  
   b. Formulate a clear, specific task\_description.  
   c. Provide all necessary context from previous steps.  
   d. Use the delegate\_task tool to assign the task.  
   e. Await the result before proceeding to the next dependent step.  
4. **Synthesise and Report:** Once all steps are complete, combine the results into a final, coherent response for the user.

**Important Rules:**

* **Manage State:** You are responsible for maintaining the state of the project, passing the output of one step as the input to the next.  
* **Validate Results:** Before passing a result to the next agent, perform a quick sanity check. If a result seems incorrect or incomplete, consider retrying the task or asking a different agent for help.

researcher.md:  
You are a Research Specialist AI. Your only purpose is to find and retrieve information using web search and API tools. You do not analyse or format data. You simply return the raw information you find.

### **The Invocation Script (orchestrator.sh)**

This script initiates the entire multi-agent workflow by tasking the Supervisor.

Bash

\#\!/bin/bash  
\# Invocation script for the Multi-Agent Orchestrator.

\# \--- Configuration \---  
AGENT\_LOG\_FILE="/var/log/claude\_agents\_orchestrator.log"  
SUPERVISOR\_COMMAND\_FILE="$HOME/.claude\_agents/supervisor/supervisor.md"  
USER\_GOAL=$1

\# \--- Usage \---  
if; then  
    echo "Usage: $0 '\<complex\_goal\>'"  
    echo "Example: $0 'Create a market analysis presentation for Apple Inc.'"  
    exit 1  
fi

\# \--- Audit Logging \---  
echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- User '$USER' initiated multi-agent orchestrator." \>\> "$AGENT\_LOG\_FILE"  
echo "  \- Goal: $USER\_GOAL" \>\> "$AGENT\_LOG\_FILE"

\# \--- Agent Invocation \---  
echo "Delegating goal to Supervisor Agent..."  
claude /supervisor \--prompt "$USER\_GOAL"

\# \--- Post-flight Check \---  
if \[ $? \-eq 0 \]; then  
    echo "Orchestration completed successfully."  
    echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- Orchestrator completed successfully." \>\> "$AGENT\_LOG\_FILE"  
else  
    echo "Error: Orchestration failed. Check logs for details."  
    echo "AUDIT LOG: $(date \-u \+"%Y-%m-%dT%H:%M:%SZ") \- Orchestrator failed." \>\> "$AGENT\_LOG\_FILE"  
    exit 1  
fi

exit 0

### **Prompt Adaptation Template (for Supervisor)**

"You are an orchestrator for a team of AI agents. Your goal is to '{complex\_goal}'. Decompose this into a plan and delegate steps to the following agents: {agent\_definitions\_json}. The final output must be a '{final\_artifact\_type}' that synthesises all intermediate results. You have a maximum of {max\_steps} steps to complete the task."

### **The Risk & Control Matrix**

In multi-agent systems, risks become systemic. Failures in communication, coordination, and error handling can cascade through the system, leading to complete and difficult-to-debug failures.

| Risk ID | Risk Description | Likelihood | Impact | Control Measure | Control Owner |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **ORCH-01** | **Cascading Failure:** An early agent in the chain returns a subtly incorrect result (e.g., data for the wrong fiscal year), which is accepted as fact by all subsequent agents, rendering the final output completely invalid.67 | High | High | **1\. Handoff Validation:** The Supervisor agent's workflow must include a validation step. After receiving a result from a worker, the Supervisor must perform a sanity check (e.g., asking itself, "Does this data seem plausible for the requested task?") before passing it to the next agent. **2\. Standardised Schemas:** All inter-agent communication must use a strictly enforced, versioned JSON schema. This prevents ambiguity and ensures data contracts are met at each step. | AI Architect |
| **ORCH-02** | **Coordination Deadlock or Infinite Loop:** Two or more agents pass a task back and forth indefinitely due to ambiguous instructions, conflicting goals, or a cyclical dependency in the Supervisor's plan.69 | Medium | High | **1\. Maximum Step Count:** The Supervisor must enforce a hard limit on the total number of steps in any plan. If the goal is not achieved within this limit, the process must be terminated and escalated to a human operator. **2\. State Machine Orchestration:** Model the workflow as a formal state machine (using a framework like LangGraph) rather than a simple loop. This makes illegal state transitions and infinite loops impossible by design. | Developer |
| **ORCH-03** | **Accountability Diffusion:** When a failure occurs, it is difficult to determine which agent or which step in the process was the root cause, making debugging and accountability nearly impossible.67 | High | Medium | **1\. Distributed Tracing:** Implement distributed tracing across the system. Every task delegated by the Supervisor must be assigned a unique trace\_id. Each worker agent must include this trace\_id in all its logs. This allows operators to reconstruct the entire end-to-end journey of a single user request across all agents. **2\. Immutable Audit Log:** The Supervisor must maintain an immutable, append-only log of every delegation decision, including the task, the target agent, the inputs provided, and the result received. | DevOps Team |
| **ORCH-04** | **Emergent Malicious Behaviour:** The complex interaction of individually benign agents leads to unforeseen and potentially harmful emergent behaviour, such as collusion to bypass a security control.71 | Low | Critical | **1\. Centralised Policy Enforcement:** Security and ethical policies should not be left to individual worker agents. They must be enforced by the Supervisor. For example, the Supervisor should be responsible for redacting sensitive data from context before delegating a task. **2\. Adversarial Red Teaming:** Periodically conduct red teaming exercises where a "malicious" agent is introduced into the system to test its resilience against collusion and manipulation. | Security Team |

### **Ethical Considerations**

* **Accountability and Responsibility:** In a multi-agent system, accountability can become dangerously diffuse. The framework must establish a clear principle: **the orchestrating Supervisor agent is ultimately accountable for the final output of the system.** The detailed, traceable audit log it produces is the mechanism for enforcing this accountability. It must be possible to determine *why* the Supervisor made a specific delegation decision.70  
* **Bias Amplification:** If one agent in the chain has a bias (e.g., a ResearchAgent that only sources information from certain websites), that bias can be amplified and cemented as fact by subsequent agents. The system design must include diversity in tooling and data sources, and the Supervisor should be capable of cross-referencing results from multiple, diverse agents if a task is particularly sensitive.  
* **Autonomy and Human Oversight:** The level of autonomy granted to the system must be commensurate with the risk of the task. For high-stakes workflows (e.g., financial analysis, medical diagnosis), the Supervisor's plan must include mandatory HITL approval gates at critical junctures. The system should not be allowed to proceed with high-impact actions without explicit human sign-off.64

### **Failure Modes & Recovery: Fault-Tolerant Orchestration Patterns**

This section details architectural patterns for building resilient multi-agent systems.

* **Failure Mode: Transient Worker Failure**  
  * **Description:** A specialist worker agent fails temporarily due to a transient issue like a network timeout, a brief API outage, or a temporary resource constraint.  
  * **Recovery Pattern: Retry with Exponential Backoff.** The delegate\_task tool used by the Supervisor must not fail immediately. It should be implemented with a built-in retry mechanism. Upon failure, it should wait for a short period (e.g., 1 second) and retry. If the failure persists, it should double the waiting period and retry again, up to a maximum number of attempts (e.g., 3-5 retries). This handles the vast majority of transient network and service issues without manual intervention.  
* **Failure Mode: Persistent Worker Failure**  
  * **Description:** A worker agent is consistently failing due to a persistent bug, a permanent outage of a critical API it relies on, or resource exhaustion on its host.  
  * **Recovery Pattern: Redundant Workers and Failover.** For critical systems, deploy multiple instances of each specialist worker type (e.g., ResearchAgent-1, ResearchAgent-2). The Supervisor's delegate\_task tool should be aware of this pool of workers. If a task delegated to ResearchAgent-1 fails after all retries are exhausted, the tool should automatically failover and re-delegate the same task to ResearchAgent-2. This is a standard high-availability pattern adapted for agentic systems.74  
* **Failure Mode: Corrupted State / Lost Messages**  
  * **Description:** The communication between agents is unreliable. A result message from a worker is lost, or the Supervisor crashes mid-workflow, losing the entire state of the ongoing task.  
  * **Recovery Pattern: Persistent Task Queues and State Management.** Instead of direct, synchronous calls between agents, use a persistent message queue (e.g., Redis, RabbitMQ) as the communication bus.  
    1. The Supervisor places a task message on a queue for the appropriate worker type.  
    2. A worker agent picks up the message, which moves it to an "in-flight" state.  
    3. The worker processes the task and places the result on a "results" queue.  
    4. Only after the result is successfully queued does the worker acknowledge the original task message, removing it permanently.  
       If the worker crashes mid-task, the task message is never acknowledged and will be automatically re-assigned to another available worker after a timeout. The Supervisor's state (the overall plan and intermediate results) should also be persisted to a database after every successful step, allowing it to resume a workflow from the last completed step if it restarts.76  
* Standardised Communication Schemas:  
  To prevent miscommunication and ensure interoperability, all messages passed between agents must adhere to a strict, version-controlled JSON schema. This acts as a formal contract between agents.  
  **Example Task Message Schema (task.json):**  
  JSON  
  {  
    "$schema": "http://json-schema.org/draft-07/schema\#",  
    "title": "Agent Task Message",  
    "type": "object",  
    "required": \["trace\_id", "task\_id", "target\_agent\_role", "task\_description", "payload"\],  
    "properties": {  
      "trace\_id": { "type": "string", "description": "Unique ID for the entire end-to-end workflow." },  
      "task\_id": { "type": "string", "description": "Unique ID for this specific task." },  
      "target\_agent\_role": { "type": "string", "enum": },  
      "task\_description": { "type": "string", "description": "Natural language instruction for the worker

#### **Works cited**

1. Key Security Risks Posed by Agentic AI and How to Mitigate Them ..., accessed on September 7, 2025, [https://www.activefence.com/key-security-risks-posed-by-agentic-ai-and-how-to-mitigate-them/](https://www.activefence.com/key-security-risks-posed-by-agentic-ai-and-how-to-mitigate-them/)  
2. The rise and risks of agentic AI: PwC, accessed on September 7, 2025, [https://www.pwc.com/us/en/industries/tmt/library/trust-and-safety-outlook/rise-and-risks-of-agentic-ai.html](https://www.pwc.com/us/en/industries/tmt/library/trust-and-safety-outlook/rise-and-risks-of-agentic-ai.html)  
3. Best Practices for Mitigating the Security Risks of Agentic AI \- Prey Project, accessed on September 7, 2025, [https://preyproject.com/blog/mitigating-agentic-ai-security-risks](https://preyproject.com/blog/mitigating-agentic-ai-security-risks)  
4. Agentic AI: The Future of Automation and Associated Risks \- HUMAN Security, accessed on September 7, 2025, [https://www.humansecurity.com/learn/blog/agentic-ai-the-future-of-automation-and-associated-risks/](https://www.humansecurity.com/learn/blog/agentic-ai-the-future-of-automation-and-associated-risks/)  
5. Top 8 AI Security Best Practices \- Sysdig, accessed on September 7, 2025, [https://www.sysdig.com/learn-cloud-native/top-8-ai-security-best-practices](https://www.sysdig.com/learn-cloud-native/top-8-ai-security-best-practices)  
6. CI/CD Security: What is It, Risks & 20 Best Practices \- Spacelift, accessed on September 7, 2025, [https://spacelift.io/blog/ci-cd-security](https://spacelift.io/blog/ci-cd-security)  
7. Ethical Considerations for AI in Software Testing | by The Test Mage \- Medium, accessed on September 7, 2025, [https://medium.com/@thetestmage/ethical-considerations-for-ai-in-software-testing-863f4394a0dc](https://medium.com/@thetestmage/ethical-considerations-for-ai-in-software-testing-863f4394a0dc)  
8. DevContainers: Streamlining Your Development Environment | by GirishCodeAlchemy, accessed on September 7, 2025, [https://girishcodealchemy.medium.com/devcontainers-streamlining-your-development-environment-5adb8f44f3e0](https://girishcodealchemy.medium.com/devcontainers-streamlining-your-development-environment-5adb8f44f3e0)  
9. Power of Dev Containers \- Codeanywhere, accessed on September 7, 2025, [https://codeanywhere.com/blog/power-of-dev-containers](https://codeanywhere.com/blog/power-of-dev-containers)  
10. 7 Proven Tips to Secure AI Agents from Cyber Attacks \- Jit.io, accessed on September 7, 2025, [https://www.jit.io/resources/devsecops/7-proven-tips-to-secure-ai-agents-from-cyber-attacks](https://www.jit.io/resources/devsecops/7-proven-tips-to-secure-ai-agents-from-cyber-attacks)  
11. Use Devcontainers for safe and replicable research \- Vincent Codes Finance, accessed on September 7, 2025, [https://vincent.codes.finance/posts/devcontainers/](https://vincent.codes.finance/posts/devcontainers/)  
12. Ultimate Guide to Dev Containers \- Daytona, accessed on September 7, 2025, [https://www.daytona.io/dotfiles/ultimate-guide-to-dev-containers](https://www.daytona.io/dotfiles/ultimate-guide-to-dev-containers)  
13. Dev Container metadata reference \- Development containers, accessed on September 7, 2025, [https://containers.dev/implementors/json\_reference/](https://containers.dev/implementors/json_reference/)  
14. Centralized configuration (agent.conf) \- Reference, accessed on September 7, 2025, [https://documentation.wazuh.com/current/user-manual/reference/centralized-configuration.html](https://documentation.wazuh.com/current/user-manual/reference/centralized-configuration.html)  
15. Centralized vs Distributed Multi-Agent AI Coordination Strategies \- Galileo AI, accessed on September 7, 2025, [https://galileo.ai/blog/multi-agent-coordination-strategies](https://galileo.ai/blog/multi-agent-coordination-strategies)  
16. Troubleshooting Dev Container issues | GoLand Documentation \- JetBrains, accessed on September 7, 2025, [https://www.jetbrains.com/help/go/troubleshooting-dev-containers.html](https://www.jetbrains.com/help/go/troubleshooting-dev-containers.html)  
17. Dev Container Troubleshooting · Common Knowledge Handbook, accessed on September 7, 2025, [https://handbook.commonknowledge.coop/5-Tech\_Guides/dev-container-troubleshooting.html](https://handbook.commonknowledge.coop/5-Tech_Guides/dev-container-troubleshooting.html)  
18. What are your struggles and challenges when working with Docker containers? \- Reddit, accessed on September 7, 2025, [https://www.reddit.com/r/docker/comments/1bk8i3n/what\_are\_your\_struggles\_and\_challenges\_when/](https://www.reddit.com/r/docker/comments/1bk8i3n/what_are_your_struggles_and_challenges_when/)  
19. Auto Document Your Code: Tools & Best Practices Guide 2025, accessed on September 7, 2025, [https://www.augmentcode.com/guides/auto-document-your-code-tools-and-best-practices](https://www.augmentcode.com/guides/auto-document-your-code-tools-and-best-practices)  
20. The Hidden Dangers of Auto-Generated Code \- Lucenia, accessed on September 7, 2025, [https://lucenia.io/2025/05/06/dangers-autogen-code/](https://lucenia.io/2025/05/06/dangers-autogen-code/)  
21. The Promise and Pitfalls of AI-Assisted Code Generation: Balancing Productivity, Control, and Risk \- Hammad Abbasi, accessed on September 7, 2025, [https://hammadulhaq.medium.com/the-promise-and-pitfalls-of-ai-assisted-code-generation-balancing-productivity-control-and-risk-80869176202f](https://hammadulhaq.medium.com/the-promise-and-pitfalls-of-ai-assisted-code-generation-balancing-productivity-control-and-risk-80869176202f)  
22. AI Code Generation: The Risks and Benefits of AI in Software \- Legit Security, accessed on September 7, 2025, [https://www.legitsecurity.com/aspm-knowledge-base/ai-code-generation-benefits-and-risks](https://www.legitsecurity.com/aspm-knowledge-base/ai-code-generation-benefits-and-risks)  
23. The Hidden Risks of Overrelying on AI in Production Code \- CodeStringers, accessed on September 7, 2025, [https://www.codestringers.com/insights/risk-of-ai-code/](https://www.codestringers.com/insights/risk-of-ai-code/)  
24. What is AI Ethics? | IBM, accessed on September 7, 2025, [https://www.ibm.com/think/topics/ai-ethics](https://www.ibm.com/think/topics/ai-ethics)  
25. Ethical Considerations When Using AI for Documentation \- Blogs Posts Template, accessed on September 7, 2025, [https://www.doc-e.ai/post/ethical-considerations-when-using-ai-for-documentation](https://www.doc-e.ai/post/ethical-considerations-when-using-ai-for-documentation)  
26. Why Ethical AI in Documentation Matters the Most \- Grazitti Interactive, accessed on September 7, 2025, [https://www.grazitti.com/blog/striking-the-right-balance-ethical-ai-and-the-human-voice-in-documentation/](https://www.grazitti.com/blog/striking-the-right-balance-ethical-ai-and-the-human-voice-in-documentation/)  
27. Chapter 3 Ethics of Using AI | AI for Efficient Programming \- Fred Hutch Data Science Lab, accessed on September 7, 2025, [https://hutchdatascience.org/AI\_for\_Efficient\_Programming/ethics-of-using-ai.html](https://hutchdatascience.org/AI_for_Efficient_Programming/ethics-of-using-ai.html)  
28. Ethics of Drafting Documents with Artificial Intelligence \- New Hampshire Bar Association, accessed on September 7, 2025, [https://www.nhbar.org/drafting-documents-with-artificial-intelligence/](https://www.nhbar.org/drafting-documents-with-artificial-intelligence/)  
29. Best Practices for Successful CI/CD | TeamCity CI/CD Guide \- JetBrains, accessed on September 7, 2025, [https://www.jetbrains.com/teamcity/ci-cd-guide/ci-cd-best-practices/](https://www.jetbrains.com/teamcity/ci-cd-guide/ci-cd-best-practices/)  
30. File access error with FileSystemWatcher when multiple files are added to a directory, accessed on September 7, 2025, [https://stackoverflow.com/questions/699538/file-access-error-with-filesystemwatcher-when-multiple-files-are-added-to-a-dire](https://stackoverflow.com/questions/699538/file-access-error-with-filesystemwatcher-when-multiple-files-are-added-to-a-dire)  
31. Solved: FileWatcher Windows Service working inconsistently \- Experts Exchange, accessed on September 7, 2025, [https://www.experts-exchange.com/questions/22022249/FileWatcher-Windows-Service-working-inconsistently.html](https://www.experts-exchange.com/questions/22022249/FileWatcher-Windows-Service-working-inconsistently.html)  
32. FileSystemWatcher : r/dotnet \- Reddit, accessed on September 7, 2025, [https://www.reddit.com/r/dotnet/comments/12xhwco/filesystemwatcher/](https://www.reddit.com/r/dotnet/comments/12xhwco/filesystemwatcher/)  
33. FileSystemWatcher Class (System.IO) \- Microsoft Learn, accessed on September 7, 2025, [https://learn.microsoft.com/en-us/dotnet/api/system.io.filesystemwatcher?view=net-9.0](https://learn.microsoft.com/en-us/dotnet/api/system.io.filesystemwatcher?view=net-9.0)  
34. The Ethics of Employee Monitoring: 5 Real-World Examples of Overreach \- CurrentWare, accessed on September 7, 2025, [https://www.currentware.com/blog/employee-monitoring-ethics/](https://www.currentware.com/blog/employee-monitoring-ethics/)  
35. 7 Best Practices for Ethical Employee Monitoring \- CleverControl, accessed on September 7, 2025, [https://clevercontrol.com/ethics-of-employee-monitoring/](https://clevercontrol.com/ethics-of-employee-monitoring/)  
36. The Ethics of Employee Monitoring \- Hubstaff, accessed on September 7, 2025, [https://hubstaff.com/employee-monitoring/ethics](https://hubstaff.com/employee-monitoring/ethics)  
37. Data Archiving: Pros/Cons, Key Features & Critical Best Practices \- N2W Software, accessed on September 7, 2025, [https://n2ws.com/blog/data-archiving](https://n2ws.com/blog/data-archiving)  
38. Defensible Deletion | Build Data Deletion Policy To Reduce Risk. \- Archive360, accessed on September 7, 2025, [https://www.archive360.com/blog/when-is-it-ok-to-delete-data](https://www.archive360.com/blog/when-is-it-ok-to-delete-data)  
39. Guidance principles on the auto-deletion of email | The National Archives, accessed on September 7, 2025, [https://cdn.nationalarchives.gov.uk/documents/information-management/guidance-principles-on-the-deletion-of-email.pdf](https://cdn.nationalarchives.gov.uk/documents/information-management/guidance-principles-on-the-deletion-of-email.pdf)  
40. Data Retention Policy: 10 Best Practices \- FileCloud, accessed on September 7, 2025, [https://www.filecloud.com/blog/data-retention-policy-best-practices/](https://www.filecloud.com/blog/data-retention-policy-best-practices/)  
41. Creating a Data Retention Policy: Examples, Best Practices & Template \- Secureframe, accessed on September 7, 2025, [https://secureframe.com/blog/data-retention-policy](https://secureframe.com/blog/data-retention-policy)  
42. The Hidden Risks of AI: Why Rigorous Testing is the Key to Success \- Medium, accessed on September 7, 2025, [https://medium.com/@vkulshrestha/the-hidden-risks-of-ai-why-rigorous-testing-is-the-key-to-success-632b3c40ed48](https://medium.com/@vkulshrestha/the-hidden-risks-of-ai-why-rigorous-testing-is-the-key-to-success-632b3c40ed48)  
43. AI in Software Testing: QA & Artificial Intelligence Guide \- TestFort, accessed on September 7, 2025, [https://testfort.com/blog/ai-in-software-testing-a-silver-bullet-or-a-threat-to-the-profession](https://testfort.com/blog/ai-in-software-testing-a-silver-bullet-or-a-threat-to-the-profession)  
44. The 10 Ethical Risks of AI in Testing (And How to Address Them) \- LambdaTest, accessed on September 7, 2025, [https://www.lambdatest.com/blog/solve-ethical-risks-of-ai-testing/](https://www.lambdatest.com/blog/solve-ethical-risks-of-ai-testing/)  
45. Considerations and Best Practices of The Ethics of AI in Software Development \- Refraction, accessed on September 7, 2025, [https://refraction.dev/blog/ethics-ai-software-development-considerations](https://refraction.dev/blog/ethics-ai-software-development-considerations)  
46. Test Automation Challenges: Insights and Solutions \- TestRail, accessed on September 7, 2025, [https://www.testrail.com/blog/test-automation-challenges/](https://www.testrail.com/blog/test-automation-challenges/)  
47. Ethical AI in Software Testing: Key Insights for QA Teams \- Codoid, accessed on September 7, 2025, [https://codoid.com/ai-testing/ethical-ai-in-software-testing-key-insights-for-qa-teams/](https://codoid.com/ai-testing/ethical-ai-in-software-testing-key-insights-for-qa-teams/)  
48. CI/CD Security: 12 Tips for Continuous Security \- Jit, accessed on September 7, 2025, [https://www.jit.io/resources/devsecops/ci-cd-security-tips](https://www.jit.io/resources/devsecops/ci-cd-security-tips)  
49. CI/CD Pipeline Security Best Practices: The Ultimate Guide \- Wiz, accessed on September 7, 2025, [https://www.wiz.io/academy/ci-cd-security-best-practices](https://www.wiz.io/academy/ci-cd-security-best-practices)  
50. How to Efficiently Implement DAST in CI/CD (2025 Guide), accessed on September 7, 2025, [https://escape.tech/blog/implement-dast-in-ci-cd/](https://escape.tech/blog/implement-dast-in-ci-cd/)  
51. Static Application Security Testing (SAST) Scanning \- Snyk, accessed on September 7, 2025, [https://snyk.io/articles/application-security/static-application-security-testing/](https://snyk.io/articles/application-security/static-application-security-testing/)  
52. Integrating SAST Into Your CI/CD Pipeline: A Step-by-Step Guide \- Jit, accessed on September 7, 2025, [https://www.jit.io/resources/app-security/integrating-sast-into-your-cicd-pipeline-a-step-by-step-guide](https://www.jit.io/resources/app-security/integrating-sast-into-your-cicd-pipeline-a-step-by-step-guide)  
53. CI/CD Pipeline Security: Best Practices to Safeguard Your Software Supply Chain \- Apiiro, accessed on September 7, 2025, [https://apiiro.com/blog/ci-cd-pipeline-security-best-practices-for-your-software/](https://apiiro.com/blog/ci-cd-pipeline-security-best-practices-for-your-software/)  
54. Ethical Considerations for Generative AI in DevOps: Building Trust and Ensuring Fairness, accessed on September 7, 2025, [https://dev.to/devops4mecode/ethical-considerations-for-generative-ai-in-devops-building-trust-and-ensuring-fairness-1k5l](https://dev.to/devops4mecode/ethical-considerations-for-generative-ai-in-devops-building-trust-and-ensuring-fairness-1k5l)  
55. DevSecOps & GenAI: Revolutionizing Security in the Digital Age \- Qentelli, accessed on September 7, 2025, [https://qentelli.com/thought-leadership/insights/devsecops-in-the-era-of-genai-opportunities-and-risks](https://qentelli.com/thought-leadership/insights/devsecops-in-the-era-of-genai-opportunities-and-risks)  
56. What is reward hacking in RL? \- Milvus, accessed on September 7, 2025, [https://milvus.io/ai-quick-reference/what-is-reward-hacking-in-rl](https://milvus.io/ai-quick-reference/what-is-reward-hacking-in-rl)  
57. Reward Hacking in Reinforcement Learning | Lil'Log, accessed on September 7, 2025, [https://lilianweng.github.io/posts/2024-11-28-reward-hacking/](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/)  
58. What is Catastrophic Forgetting? \- IBM, accessed on September 7, 2025, [https://www.ibm.com/think/topics/catastrophic-forgetting](https://www.ibm.com/think/topics/catastrophic-forgetting)  
59. Catastrophic interference \- Wikipedia, accessed on September 7, 2025, [https://en.wikipedia.org/wiki/Catastrophic\_interference](https://en.wikipedia.org/wiki/Catastrophic_interference)  
60. en.wikipedia.org, accessed on September 7, 2025, [https://en.wikipedia.org/wiki/Reinforcement\_learning\#:\~:text=real%2Dworld%20applications.-,Stability%20and%20Convergence%20Issues,difficult%20to%20achieve%20consistent%20results.](https://en.wikipedia.org/wiki/Reinforcement_learning#:~:text=real%2Dworld%20applications.-,Stability%20and%20Convergence%20Issues,difficult%20to%20achieve%20consistent%20results.)  
61. Improving Stability in Deep Reinforcement Learning with Weight Averaging, accessed on September 7, 2025, [https://www.gatsby.ucl.ac.uk/\~balaji/udl-camera-ready/UDL-24.pdf](https://www.gatsby.ucl.ac.uk/~balaji/udl-camera-ready/UDL-24.pdf)  
62. AI and Adaptive Learning: Benefits, Challenges, and the Future of Personalized Education, accessed on September 7, 2025, [https://www.quizwhiz.ai/content/blog/ai-and-adaptive-learning-benefits-challenges-and-the-future-of-personalized-education/](https://www.quizwhiz.ai/content/blog/ai-and-adaptive-learning-benefits-challenges-and-the-future-of-personalized-education/)  
63. The risks of Recursive Self-Improvement \- datapro.news, accessed on September 7, 2025, [https://www.datapro.news/p/the-risks-of-recursive-self-improvement](https://www.datapro.news/p/the-risks-of-recursive-self-improvement)  
64. Ethical Considerations in Deploying Autonomous AI Agents \- Auxiliobits, accessed on September 7, 2025, [https://www.auxiliobits.com/blog/ethical-considerations-when-deploying-autonomous-agents/](https://www.auxiliobits.com/blog/ethical-considerations-when-deploying-autonomous-agents/)  
65. Ethical Responsibility in Autonomous Agents \- Terranoha, accessed on September 7, 2025, [https://terranoha.com/solution/ai-virtual-agent-automation/ethics-and-responsibility-in-deploying-autonomous-agents/](https://terranoha.com/solution/ai-virtual-agent-automation/ethics-and-responsibility-in-deploying-autonomous-agents/)  
66. Data Ethics in AI: 6 Key Principles for Responsible Machine Learning \- Alation, accessed on September 7, 2025, [https://www.alation.com/blog/data-ethics-in-ai-6-key-principles-for-responsible-machine-learning/](https://www.alation.com/blog/data-ethics-in-ai-6-key-principles-for-responsible-machine-learning/)  
67. i³ Threat Advisory: The Rise and Risks of AI Agents \- DTEX Systems, accessed on September 7, 2025, [https://www.dtexsystems.com/resources/i3-threat-advisory-mitigating-ai-agent-risks/](https://www.dtexsystems.com/resources/i3-threat-advisory-mitigating-ai-agent-risks/)  
68. 7 Multi-Agent Debugging Challenges Every AI Team Faces | Galileo, accessed on September 7, 2025, [https://galileo.ai/blog/debug-multi-agent-ai-systems](https://galileo.ai/blog/debug-multi-agent-ai-systems)  
69. Agent system design patterns | Databricks on AWS, accessed on September 7, 2025, [https://docs.databricks.com/aws/en/generative-ai/guide/agent-system-design-patterns](https://docs.databricks.com/aws/en/generative-ai/guide/agent-system-design-patterns)  
70. Multi-Agent Systems in AI: Challenges, Safety Measures, and Ethical Considerations, accessed on September 7, 2025, [https://skphd.medium.com/multi-agent-systems-in-ai-challenges-safety-measures-and-ethical-considerations-7a7636b971bd](https://skphd.medium.com/multi-agent-systems-in-ai-challenges-safety-measures-and-ethical-considerations-7a7636b971bd)  
71. 5 Challenges of Scaling Multi-Agent Systems: Key Issues and Solutions for Autonomous AI, accessed on September 7, 2025, [https://zigron.com/2025/08/07/5-challenges-multi-agent-systems/](https://zigron.com/2025/08/07/5-challenges-multi-agent-systems/)  
72. Emergent Behavior \- AI Ethics Lab, accessed on September 7, 2025, [https://aiethicslab.rutgers.edu/e-floating-buttons/emergent-behavior/](https://aiethicslab.rutgers.edu/e-floating-buttons/emergent-behavior/)  
73. Multi-Agent Systems and Ethical Considerations: Navigating AI Responsibility \- SmythOS, accessed on September 7, 2025, [https://smythos.com/developers/agent-development/multi-agent-systems-and-ethical-considerations/](https://smythos.com/developers/agent-development/multi-agent-systems-and-ethical-considerations/)  
74. milvus.io, accessed on September 7, 2025, [https://milvus.io/ai-quick-reference/how-do-multiagent-systems-ensure-fault-tolerance\#:\~:text=Multi%2Dagent%20systems%20(MAS),agents%20fail%20or%20encounter%20errors.](https://milvus.io/ai-quick-reference/how-do-multiagent-systems-ensure-fault-tolerance#:~:text=Multi%2Dagent%20systems%20\(MAS\),agents%20fail%20or%20encounter%20errors.)  
75. How do multi-agent systems ensure fault tolerance? \- Milvus, accessed on September 7, 2025, [https://milvus.io/ai-quick-reference/how-do-multiagent-systems-ensure-fault-tolerance](https://milvus.io/ai-quick-reference/how-do-multiagent-systems-ensure-fault-tolerance)  
76. A Survey on Fault Tolerant Multi Agent System \- ResearchGate, accessed on September 7, 2025, [https://www.researchgate.net/publication/307889041\_A\_Survey\_on\_Fault\_Tolerant\_Multi\_Agent\_System](https://www.researchgate.net/publication/307889041_A_Survey_on_Fault_Tolerant_Multi_Agent_System)