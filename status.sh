#!/usr/bin/env bash

echo "========================================"
echo "Solar Digital Twin Session Status"
echo "========================================"
echo

echo "Branch:"
git branch --show-current
echo

echo "Git Status:"
git status --short
echo

echo "Latest Commit:"
git log -1 --oneline
echo

echo "GitHub Sync:"
git fetch --quiet
git status -sb
echo

if [ -f PROJECT_STATE.md ]; then
    echo "========== PROJECT_STATE.md =========="
    cat PROJECT_STATE.md
    echo
fi

if [ -f NEXT_TASK.md ]; then
    echo "========== NEXT_TASK.md =============="
    cat NEXT_TASK.md
    echo
fi
