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

echo "Repository Health:"
if [[ -x scripts/repo_health_check.sh ]]; then
    ./scripts/repo_health_check.sh
else
    echo "MISSING: scripts/repo_health_check.sh"
fi
echo
duplicate_headings=0
while IFS= read -r file; do
    duplicates=$(grep -E '^#{1,6} ' "$file" | sort | uniq -d)
    if [[ -n "$duplicates" ]]; then
        echo "DUPLICATE HEADINGS: $file"
        printf '%s\n' "$duplicates" | sed 's/^/  /'
        duplicate_headings=1
    fi
done < <(find . -maxdepth 3 -type f -name '*.md' -not -path './.git/*' -print | sort)

if [[ "$duplicate_headings" -eq 0 ]]; then
    echo "Duplicate headings: OK"
fi
echo
project_next=$(awk '/^Next Task:/{getline; print; exit}' PROJECT_STATE.md)
task_objective=$(awk '/^## Objective$/{getline; while ($0 ~ /^[[:space:]]*$/) getline; print; exit}' NEXT_TASK.md)

normalize_text() {
    tr '[:upper:]' '[:lower:]' |
        sed -E 's/`//g; s/[[:punct:]]+$//; s/[[:space:]]+/ /g; s/^ //; s/ $//'
}

normalized_project_next=$(printf '%s' "$project_next" | normalize_text)
normalized_task_objective=$(printf '%s' "$task_objective" | normalize_text)

if [[ "$normalized_project_next" == "$normalized_task_objective" ]]; then
    echo "Documentation drift: OK"
else
    echo "DOCUMENTATION DRIFT:"
    echo "  PROJECT_STATE.md: $project_next"
    echo "  NEXT_TASK.md: $task_objective"
fi
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
