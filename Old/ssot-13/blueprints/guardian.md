# Guardian

## Objective & Success Criteria
Monitor a folder for changes, notify with cooldown to avoid spam, achieving 99.9% detection with <5% false positives.

## Custom Slash Command
```markdown
---
name: "/watcher"
intent: "Given details of a file system event, generate a concise, human-readable notification."
---
You are a File System Guardian. Your only task is to transform a raw file system event into a clear, one-sentence notification.

**RULES:**
1. Be concise. Do not add conversational filler.
2. State the file name and the action that occurred.
3. If given `ls -l` output, include the file size.

**EXAMPLE INPUT:**
`Mon Sep 8 10:30:01 2025 /Users/dev/project/src/api.js`
`-rw-r--r-- 1 dev staff 4096 Sep 8 10:30 /Users/dev/project/src/api.js`

**EXAMPLE OUTPUT:**
`File modified: src/api.js (4.1 KB)`
```

## Invocation Script
```bash
#!/bin/bash
set -e # Exit on error

# --- Configuration ---
WATCH_PATH="$1"
LOG_FILE="$HOME/.claude_agents/logs/guardian.log"
COOLDOWN_SECONDS=10 # Ignore rapid-fire changes
LAST_EVENT_TIME=0

# --- Pre-flight Checks ---
if [ -z "$WATCH_PATH" ]; then
    echo "Usage: $0 /path/to/watch"
    exit 1
fi
if [ ! -d "$WATCH_PATH" ]; then
    echo "Error: Directory not found at ${WATCH_PATH}"
    exit 1
fi

echo "[$(date)] Guardian Agent started. Watching: ${WATCH_PATH}" | tee -a "${LOG_FILE}"

# --- Main Loop ---
fswatch -o "$WATCH_PATH" | while read -r file_path; do
    CURRENT_TIME=$(date +%s)
    if (( CURRENT_TIME - LAST_EVENT_TIME < COOLDOWN_SECONDS )); then
        continue # Skip if within cooldown period
    fi
    LAST_EVENT_TIME=$CURRENT_TIME

    echo "[$(date)] Event detected for file: ${file_path}" >> "${LOG_FILE}"

    # Explicitly gather context for the agent
    EVENT_DETAILS=$(ls -l "$file_path")

    # Invoke agent to generate the notification message
    NOTIFICATION=$(claude /watcher "${EVENT_DETAILS}")

    # Log and send the notification (macOS example)
    echo "  - Notification: ${NOTIFICATION}" >> "${LOG_FILE}"
    osascript -e "display notification \"${NOTIFICATION}\" with title \"Guardian Alert\""
done
```

## Risk & Control Matrix
| Risk | Impact | Control | Residual Risk |
|------|--------|---------|---------------|
| Spam Alerts | Low | Cooldown logic | Low |
| Missed Changes | High | Robust fswatch | Low |
| Privacy Breach | Medium | Sanitise logs | Low |

## Failure Modes & Recovery
- Watch failure → restart script
- False positives → refine matcher
