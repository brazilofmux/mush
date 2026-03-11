#!/usr/bin/env bash
set -euo pipefail

if ! command -v ragel >/dev/null 2>&1; then
    echo "ragel not found in PATH; cannot regenerate mdfix.c from mdfix.rl" >&2
    exit 1
fi

ragel -G2 -o mdfix.c mdfix.rl
echo "Regenerated mdfix.c from mdfix.rl using Ragel -G2."
