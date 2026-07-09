#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="backups/project-docs/$(date +%Y%m%d_%H%M%S)"

mkdir -p "$BACKUP_DIR"

for file in \
  PROJECT_STATE.md \
  NEXT_TASK.md \
  TEAM.md \
  BACKLOG.md \
  CONTRIBUTING.md \
  ENGINEERING_WORKFLOW.md
do
  if [ -f "$file" ]; then
    cp "$file" "$BACKUP_DIR/"
  fi
done

echo "Backed up project docs to: $BACKUP_DIR"
