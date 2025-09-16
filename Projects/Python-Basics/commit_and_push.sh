#!/usr/bin/env bash
set -e
BRANCH="feat/python-basics"
echo "Creating branch $BRANCH"
git checkout -b "$BRANCH"
git add Projects/Python-Basics
git commit -m "chore(python): add Python Basics artifacts and example scripts" || { echo "Nothing to commit?"; exit 0; }
git push -u origin "$BRANCH"
echo "Branch pushed: $BRANCH"
echo "Open PR: https://github.com/MthunzeeBaloyi/DevOps-Journey-2025/pull/new/$BRANCH"
