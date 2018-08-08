#!/usr/bin/env bash

# Note rev-parse works inside the .git dir which is why we can use it in this
# file, so it can be run manually or by the git hook process.
GIT_ROOT="$(git rev-parse --show-toplevel)"
GIT_HOOKS_DIR="${GIT_ROOT}/.git/hooks"
PROJECT_HOOKS_DIR="${GIT_ROOT}/bin/git-hooks/pre-commit"

for f in ${PROJECT_HOOKS_DIR}/*; do
    # $f is a file:
    if [[ -f $f ]]; then
        echo "Running pre-commit hook: $f"
        $f || exit 1
    fi
done

exit 0
