#!/usr/bin/env bash
set -euo pipefail

KEEP_BACKUPS=20
TRIGGER="${1:-Manual}"
NOTES="${2:-None}"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_ROOT="backups/project-docs"
BACKUP_DIR="$BACKUP_ROOT/$TIMESTAMP"

mkdir -p "$BACKUP_DIR"

FILES=(
  PROJECT_STATE.md
  NEXT_TASK.md
  ROADMAP.md
  TEAM.md
  BACKLOG.md
  CONTRIBUTING.md
  ENGINEERING_WORKFLOW.md
  SESSION_START.md
  AI_CONTEXT.md
  status.sh
  start_session.sh
)

for file in "${FILES[@]}"; do
  [ -f "$file" ] && cp "$file" "$BACKUP_DIR/"
done

cat > "$BACKUP_DIR/backup_manifest.txt" <<MANIFEST
Timestamp: $TIMESTAMP
Trigger: $TRIGGER
Notes: $NOTES
Branch: $(git rev-parse --abbrev-ref HEAD)
Commit: $(git rev-parse --short HEAD)
Host: $(whoami)@$(hostname)
Remote: $(git remote get-url origin 2>/dev/null || echo "none")
Python: $(python --version 2>/dev/null || echo "python unavailable")
Virtual Env: ${VIRTUAL_ENV:-none}

Git Status:
$(git status --short)
MANIFEST

find "$BACKUP_ROOT" -mindepth 1 -maxdepth 1 -type d \
| sort \
| head -n "-$KEEP_BACKUPS" \
| xargs -r rm -rf

echo "Backed up project docs to: $BACKUP_DIR"
echo "Trigger: $TRIGGER"
echo "Notes: $NOTES"
echo "Keeping latest $KEEP_BACKUPS backups only."
