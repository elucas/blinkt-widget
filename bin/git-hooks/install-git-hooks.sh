#!/usr/bin/env bash

GIT_ROOT="$(git rev-parse --show-toplevel)"
GIT_HOOKS_DIR="${GIT_ROOT}/.git/hooks"
PROJECT_HOOKS_DIR="${GIT_ROOT}/bin/git-hooks"

ln -s ${PROJECT_HOOKS_DIR}/pre-commit-runner.sh ${GIT_HOOKS_DIR}/pre-commit && echo "Git hooks created successfully."
