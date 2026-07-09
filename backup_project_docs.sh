#!/usr/bin/env bash
set -euo pipefail

KEEP_BACKUPS=20
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_ROOT="backups/project-docs"
BACKUP_DIR="$BACKUP_ROOT/$TIMESTAMP"

mkdir -p "$BACKUP_DIR"

FILES=(
  PROJECT_STATE.md
  NEXT_TASK.md
  TEAM.md
  BACKLOG.md
  CONTRIBUTING.md
  ENGINEERING_WORKFLOW.md
  SESSION_START.md
  AI_CONTEXT.md
  status.sh
)

for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    cp "$file" "$BACKUP_DIR/"
  fi
done

cat > "$BACKUP_DIR/backup_manifest.txt" <<MANIFEST
Timestamp: $TIMESTAMP
Branch: $(git branch --show-current)
Commit: $(git rev-parse --short HEAD)
Remote: $(git remote get-url origin 2>/dev/null || echo "none")
Python: $(python --version 2>/dev/null || echo "python unavailable")
Virtual Env: ${VIRTUAL_ENV:-none}

Git Status:
$(git status --short)
MANIFEST

# Keep only the newest $KEEP_BACKUPS backups
if [ -d "$BACKUP_ROOT" ]; then
  find "$BACKUP_ROOT" -mindepth 1 -maxdepth 1 -type d \
    | sort \
    | head -n "-$KEEP_BACKUPS" \
    | xargs -r rm -rf
fi

echo "Backed up project docs to: $BACKUP_DIR"
echo "Keeping latest $KEEP_BACKUPS backups only."
