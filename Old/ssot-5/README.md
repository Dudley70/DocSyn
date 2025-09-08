# SSOT-5: Claude Code Knowledge Base for Gemini Gem

## What This Project Is

SSOT-5 is a **knowledge compilation system** that transforms modular documentation about Claude Code into a single, authoritative source of truth document (`SSOT.md`). This compiled knowledge base powers a Gemini Gem that provides expert-level advice on Claude Code usage and agent development patterns.

## Project Purpose & Flow

```
Modular Source Files → Build System → SSOT.md → Gemini Gem → Claude Code Expertise
     (/core/ + /blueprints/)                              (Knowledge Base)    (User Gets Advice)
```

- **Input**: Small, maintainable `.md` files in `/core/` and `/blueprints/`
- **Process**: Automated compilation via `scripts/assemble_ssot.py`
- **Output**: Single `SSOT.md` file optimized for Gemini Gem consumption
- **Consumer**: Gemini Gem configured to use the compiled knowledge base
- **End Result**: Users get authoritative, up-to-date advice on Claude Code and agent blueprints

## Key Components

### 📚 **Knowledge Architecture**
- **`/core/`** - Foundational concepts (Router, Risk Model, DevContainer setup)
- **`/blueprints/`** - Agent patterns (Documenter, Guardian, Janitor, Tester, etc.)
- **`/dashboards/`** - Grafana monitoring configurations
- **`/scripts/`** - Build automation and validation tools

### 🤖 **The Gemini Gem Integration**
This project enables a Gemini Gem to become a Claude Code expert by:
- Understanding user intent via the Router system
- Providing blueprint-based recommendations
- Applying risk management frameworks
- Suggesting concrete implementation patterns

### 🛡️ **Governance & Safety**
- Four-pillar risk model (Governance, Environment, Data, Operations)
- Human-in-the-loop approval patterns
- Comprehensive telemetry and monitoring guidance
- Security-first devcontainer architecture

---

## Quickstart Guide: Setting Up and Using the Agentic SSOT

### **Introduction: What is This?**

This guide will get you set up with the Agentic SSOT in under 5 minutes. The SSOT is a self-governing knowledge base that powers our expert Gemini Gem on Claude Code. This repository contains the source files, and a build process compiles them into a single, comprehensive manual (`SSOT.md`) for the Gem to use.

### **Part 1: The 5-Minute Setup**

1. **Prerequisites:** Ensure you have `make`, `python3`, and `docker` installed on your system.

2. **Clone the Repository:** Clone this repository to your local machine:
   ```bash
   git clone <repository-url>
   cd ssot-5
   ```

3. **Validate the Setup:** Run the master check from the repository root. This will build the SSOT, run the router smoke test, and check for long code blocks:
   ```bash
   make ci
   ```
   If this command succeeds, your environment is correctly configured.

4. **Point Your Gem:** In your Gemini settings, create or configure your Gem to use the newly compiled **`SSOT.md`** file as its primary knowledge source.

### **Part 2: Your Daily Workflow**

Your daily interaction with the SSOT follows a simple "Docs-as-Code" pattern:

1. **Ask the Gem:** Use your Gemini Gem for any questions about Claude Code. It will use the `SSOT.md` to give you expert, reliable answers.

2. **Edit the Source:** To update or add information, edit the small, modular `.md` files in the **`/core/`** and **`/blueprints/`** directories. **Do not edit `SSOT.md` directly**.

3. **Rebuild Locally:** After making your changes, re-compile the main manual by running:
   ```bash
   make ssot
   ```

4. **Create a Pull Request:** Commit your changes to the modular source files and open a pull request. The CI system will automatically run all validation checks on your PR.

### **Part 3: Key Concepts in 60 Seconds**

- **Dual-Surface, Single-Source (DSSS):** We manage content in small, easy-to-edit files (the *source*), which are then compiled into a single manual (the *surface*) for the Gem.

- **The Router (`core/00-router.md`):** This is the brain of the Gem's retrieval system. It maps user intents to the correct section of the manual to ensure you get accurate answers.

- **Blueprints (`/blueprints/`):** These are detailed, templated guides for building specific types of agents. They are the practical core of the manual.

- **The Risk Model (`core/01-risks.md`):** This is our central safety and governance framework. It defines the rules and controls that all agents must operate under.

### **Part 4: Where to Find More**

This quickstart is your entry point. For deep dives into specific topics, full code examples, and advanced patterns, please refer to the complete, compiled **`SSOT.md`** manual.

---

## Available Make Commands

```bash
make ssot          # Compile source files into SSOT.md
make check         # Validate source files and check for issues
make router-test   # Run router smoke tests
make code-lift     # Fix code block formatting issues
make ci            # Full CI validation (lint, build, test)
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines, authoring conventions, and versioning practices.

## Project Structure

```
ssot-5/
├── core/                    # Foundational components
│   ├── 00-router.md        # Intent routing logic
│   ├── 01-risks.md         # Risk management framework
│   └── 02-devcontainer.md  # Standard development environment
├── blueprints/             # Agent implementation patterns
│   ├── documenter.md       # Automated documentation agent
│   ├── guardian.md         # File watching and linting agent
│   ├── janitor.md          # Repository cleanup agent
│   ├── tester.md           # Automated testing agent
│   ├── cicd-analyst.md     # CI/CD security analysis agent
│   ├── adaptive-learning.md # Self-improving agent
│   └── orchestrator.md     # Multi-agent coordination
├── dashboards/             # Monitoring configurations
├── scripts/                # Build and validation tools
├── .github/workflows/      # CI/CD automation
├── build.manifest.json     # Build configuration
├── SSOT.md                 # Compiled output (auto-generated)
└── README.md              # This file
```

## License

[Add your license information here]

## Support

For questions about this knowledge compilation system, please open an issue. For questions about Claude Code itself, ask your configured Gemini Gem!