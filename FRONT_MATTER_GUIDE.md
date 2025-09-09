# DocSyn Front-Matter Guide

This guide explains how to use DocSyn's **data-driven document processing** with YAML front-matter to automatically structure any document set.

## 🎯 Core Concept

Instead of manually creating files for each document type, you add **front-matter** to your documents that tells DocSyn where and how to process them. The system automatically creates the necessary infrastructure.

## 📝 Front-Matter Schema

Add YAML front-matter to the top of your documents:

```yaml
---
# ROUTING (choose exactly one):
part: A                     # → Goes to core/ (global sections)
blueprint: my-blueprint     # → Goes to blueprints/my-blueprint.md

# OPTIONAL METADATA:
slug: stable-identifier     # Stable ID for references
order: 20                   # Sort order within module
chapter: "Foundations"      # Logical grouping
tags: [policy, risk]        # Classification tags
owner: TeamName             # Responsible team
source: "Original Doc"      # Provenance tracking
---

# Your Content Here

Regular markdown content follows the front-matter.
```

## 🔄 Processing Workflows

### Method 1: Direct Document Processing
```bash
# 1. Add documents with front-matter to staging
cp your-docs-with-frontmatter.md merge_pr/updated/

# 2. Process automatically
make docsyn

# 3. System auto-creates blueprint anchors for new blueprint types
# 4. Router suggestions logged to dist/ROUTER_SUGGESTIONS.txt
```

### Method 2: Bulk Source Processing  
```bash
# 1. Add raw documents to sources
cp *.md sources/raw/

# 2. Extract content to blueprints (existing system)
make seed-from-sources

# 3. Process and build
make docsyn
```

## 🎛️ Automatic Blueprint Creation

When you use a **new blueprint name**, DocSyn automatically:

1. **Creates blueprint anchor**: `blueprints/your-blueprint.md`
2. **Logs router suggestion**: `dist/ROUTER_SUGGESTIONS.txt`
3. **Informs you**: Console output shows what was created

### Example: First-Time Blueprint
```yaml
---
blueprint: api-documentation
owner: Backend
tags: [api, docs]
---

# API Documentation

This document will automatically create `blueprints/api-documentation.md`
```

**Result:**
```bash
[INFO] Created blueprint anchor: blueprints/api-documentation.md
[INFO] Router suggestion logged: see dist/ROUTER_SUGGESTIONS.txt
```

## 📋 Router Integration

After DocSyn creates a new blueprint, **manually add** the router mapping:

1. **Check suggestions**: `cat dist/ROUTER_SUGGESTIONS.txt`
2. **Copy suggested line**: `CH4-BP-APIDOC → blueprints/api-documentation.md`  
3. **Add to router table**: Edit `core/00-router.md`

```markdown
| Intent | Positive Patterns | Negative Patterns | Route | Key Risks |
|---|---|---|---|---|
| API documentation | api, docs, endpoints | internal, private | CH4-BP-APIDOC | Data: exposure |
```

## 📂 Routing Rules

### Part A (Global Sections)
```yaml
---
part: A
slug: global-config
---
```
- **Goes to**: `core/global-config.md`
- **Purpose**: System-wide sections that appear once
- **Examples**: Configuration, global policies, architecture

### Blueprint Modules  
```yaml
---
blueprint: user-management
slug: user-mgmt
---
```
- **Goes to**: `blueprints/user-management.md`
- **Purpose**: Modular functionality sections
- **Examples**: Features, processes, tools, workflows

## 🏗️ Document Set Examples

### Academic Papers → Research Synthesis
```yaml
---
blueprint: methodology
chapter: "Research Methods"
tags: [research, analysis]
---

# Methodology

Our research approach combines...
```

### API Documentation → Developer Guide
```yaml
---
blueprint: authentication
chapter: "Security"
tags: [auth, security, api]
---

# Authentication

The API uses OAuth 2.0...
```

### Legal Documents → Compliance Framework
```yaml
---
part: A
slug: legal-framework
chapter: "Foundation"
---

# Legal Framework

This document establishes...
```

## 🔍 Quality Gates

The system automatically validates:

- ✅ **Blueprint anchors exist** for all referenced blueprints
- ✅ **Router contract intact** with required route codes
- ✅ **No contamination** from previous document batches
- ✅ **Unicode integrity** and deterministic builds

## 🚨 Error Handling

### Missing Blueprint
```bash
# If blueprint doesn't exist, system auto-creates it
[INFO] Created blueprint anchor: blueprints/new-module.md
[INFO] Router suggestion logged: see dist/ROUTER_SUGGESTIONS.txt
```

### Invalid Front-Matter
```bash
# System falls back to original filename-based promotion
[WARN] Failed to promote doc.md: invalid front-matter
  - doc.md → blueprints/doc.md (fallback)
```

### Routing Conflicts
```bash
# Manual review required when patterns overlap
[INFO] Check dist/ROUTER_SUGGESTIONS.txt for router mappings to add
```

## 🎯 Best Practices

### 1. Consistent Naming
```yaml
# Good: Clear, descriptive blueprint names
blueprint: user-authentication
blueprint: data-processing
blueprint: error-handling

# Avoid: Generic or ambiguous names
blueprint: utils
blueprint: misc
blueprint: other
```

### 2. Logical Grouping
```yaml
# Use chapters for related content
blueprint: auth-setup
chapter: "Security"

blueprint: auth-tokens  
chapter: "Security"

blueprint: auth-troubleshooting
chapter: "Security"
```

### 3. Metadata Consistency
```yaml
# Consistent owner/tag patterns
owner: Backend
tags: [api, security]

owner: Frontend  
tags: [ui, components]

owner: DevOps
tags: [infrastructure, deployment]
```

## 🔄 Batch Reset Procedure

Between document sets:

```bash
# 1. Archive previous output (optional)
cp dist/DocSyn_Compiled.md archive/batch_$(date +%Y%m%d).md

# 2. Clear staging and sources
rm -rf merge_pr/updated/* sources/raw/*

# 3. Clear blueprint content (keep structure)
find blueprints/ -name "*.md" -exec sh -c 'echo "<!-- Content will be populated from document processing -->" > "$1"' _ {} \;

# 4. Clear suggestions from previous batch
rm -f dist/ROUTER_SUGGESTIONS.txt

# 5. Verify system integrity  
make qa

# 6. Add new documents with front-matter
cp new-batch/*.md merge_pr/updated/

# 7. Process new batch
make docsyn
```

## 📖 Migration Guide

### From Manual File Creation
**Before:**
```bash
# Manual blueprint creation
touch blueprints/new-feature.md
vim blueprints/new-feature.md  # Manual editing
```

**After:**
```yaml
---
blueprint: new-feature
owner: ProductTeam
tags: [feature, enhancement]
---

# New Feature

Content here automatically goes to blueprints/new-feature.md
```

### From Hardcoded Structures
**Before:**
```bash
# Hardcoded for specific document types
if [[ "$file" == *"api"* ]]; then
  cp "$file" blueprints/api.md
fi
```

**After:**
```yaml
---
blueprint: api-documentation
tags: [api, reference]
---

# Content automatically routed based on front-matter
```

---

**The system is now universal and data-driven. Any document set can flow through the same infrastructure by adding appropriate front-matter.**
