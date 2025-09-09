# 0. Router — Query-Pattern Matrix
{{#CH0-ROUTER}}

> Documentation synthesis router - Ready for next document batch configuration.

| Intent | Positive Patterns | Negative Patterns | Route | Key Risks |
|---|---|---|---|---|
| Document processing | process, compile, synthesize | delete, remove | DOC-PROCESS | Data: integrity |
| Content analysis | analyze, review, examine | ignore, skip | DOC-ANALYZE | Data: accuracy |
| System management | manage, configure, setup | break, destroy | DOC-MANAGE | Ops: availability |

---

## Router Legend
- **Positive Patterns**: comma-separated keywords/regex the router uses to route queries.
- **Negative Patterns**: keywords/regex that disqualify a route.
- **Route**: stable section ID of the target blueprint.
- **Key Risks**: primary risk categories for this intent.

## Next Steps
1. Add new document sources to merge_pr/updated/
2. Run `make docsyn` to process documents
3. Configure routing patterns based on new document content
