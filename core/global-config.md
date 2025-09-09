---
part: A
slug: global-config
order: 5
chapter: "Configuration"
tags: [config, global]
owner: Platform
---

# Global Configuration

This document contains global configuration settings that apply across all modules.

## Environment Variables

- `DOCSYN_ENV`: Runtime environment (development, staging, production)
- `DOCSYN_LOG_LEVEL`: Logging verbosity (debug, info, warn, error)

## Default Settings

```yaml
defaults:
  timeout: 30s
  retries: 3
  encoding: utf-8
```

This should be promoted to the core/ directory as a Part A global section.
