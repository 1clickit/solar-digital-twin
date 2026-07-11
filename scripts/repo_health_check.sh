#!/usr/bin/env bash

failures=0

pass() {
    printf 'PASS: %s\n' "$1"
}

fail() {
    printf 'FAIL: %s\n' "$1"
    failures=$((failures + 1))
}

require_file() {
    if [[ -f "$1" ]]; then
        pass "required file exists: $1"
    else
        fail "required file missing: $1"
    fi
}

has_heading() {
    local file=$1
    local heading=$2
    grep -qx "$heading" "$file"
}

heading_value() {
    local file=$1
    local heading=$2
    awk -v heading="$heading" '
        $0 == heading {
            while (getline) {
                if ($0 !~ /^[[:space:]]*$/) {
                    print
                    exit
                }
            }
        }
    ' "$file"
}

echo "Repository health check"
echo "======================="
echo
required_files=(
    START_HERE.md
    AI_PROMPT.md
    TEAM.md
    CONTRIBUTING.md
    PROJECT_STATE.md
    NEXT_TASK.md
    BACKLOG.md
    SESSION_END.md
    PROJECT_INDEX.md
)

for file in "${required_files[@]}"; do
    require_file "$file"
done

echo

current_milestone=$(heading_value PROJECT_STATE.md "Current Milestone:")
next_task=$(heading_value PROJECT_STATE.md "Next Task:")

if [[ -n "$current_milestone" ]]; then
    pass "PROJECT_STATE.md current milestone is set"
else
    fail "PROJECT_STATE.md current milestone is missing"
fi

if [[ -n "$next_task" ]]; then
    pass "PROJECT_STATE.md next task is set"
else
    fail "PROJECT_STATE.md next task is missing"
fi

echo

for heading in "## Objective" "## Scope" "## Success"; do
    if has_heading NEXT_TASK.md "$heading"; then
        pass "NEXT_TASK.md has $heading"
    else
        fail "NEXT_TASK.md missing $heading"
    fi
done

echo
while IFS= read -r doc; do
    if [[ -f "$doc" ]]; then
        pass "indexed doc exists: $doc"
    else
        fail "indexed doc missing: $doc"
    fi
done < <(grep -E '^docs/.*\.md$' PROJECT_INDEX.md | sort -u)

echo

for generated_dir in reports evidence; do
    if git check-ignore -q "$generated_dir/"; then
        pass "generated directory ignored by Git: $generated_dir/"
    else
        fail "generated directory not ignored by Git: $generated_dir/"
    fi
done

echo
staged_credentials=$(
    git diff --cached --name-only |
        grep -Ei '(^|/)(\.env|.*credential.*|.*secret.*|eg4\.env|.*\.local\.yaml)$' || true
)

if [[ -z "$staged_credentials" ]]; then
    pass "no obvious credential filenames are staged"
else
    fail "possible credential filenames staged:"
    printf '%s\n' "$staged_credentials" | sed 's/^/  /'
fi

echo

shell_scripts=()
while IFS= read -r -d '' file; do
    shell_scripts+=("$file")
done < <(git ls-files -z -- '*.sh')

if [[ "${#shell_scripts[@]}" -eq 0 ]]; then
    pass "no tracked shell scripts found"
else
    for file in "${shell_scripts[@]}"; do
        if bash -n "$file"; then
            pass "shell syntax valid: $file"
        else
            fail "shell syntax invalid: $file"
        fi
    done
fi

echo

python_files=()
while IFS= read -r -d '' file; do
    python_files+=("$file")
done < <(git ls-files -z -- '*.py')

if [[ "${#python_files[@]}" -eq 0 ]]; then
    pass "no tracked Python source files found"
else
    if command -v python >/dev/null 2>&1; then
        python_command=python
    elif command -v python3 >/dev/null 2>&1; then
        python_command=python3
    else
        fail "python and python3 commands are unavailable"
        python_command=
    fi

    if [[ -n "$python_command" ]]; then
        python_cache_dir=$(mktemp -d)
        if PYTHONPYCACHEPREFIX="$python_cache_dir" "$python_command" -m compileall -q "${python_files[@]}"; then
            pass "tracked Python source files compile with $python_command"
        else
            fail "tracked Python source files failed to compile"
        fi
        rm -rf "$python_cache_dir"
    fi
fi

echo

if [[ "$failures" -eq 0 ]]; then
    echo "RESULT: PASS"
else
    echo "RESULT: FAIL ($failures issue(s))"
fi

exit "$failures"
