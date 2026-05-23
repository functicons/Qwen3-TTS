#!/usr/bin/env bash
# Easy-to-use CLI for Qwen3-TTS. Wraps scripts/qwen3_tts_cli.py with the repo's
# venv already activated, so callers don't have to think about Python paths.
#
# Usage:
#   scripts/qwen3-tts-cli.sh --text "Hello world" --out hello.wav
#   scripts/qwen3-tts-cli.sh -t "你好世界" -o ni-hao.wav -l Chinese -s Vivian \
#       -i "用欢快的语气说"
#
# Run with --help to see all flags.
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$REPO_ROOT/.venv/bin/python"
RUNNER="$REPO_ROOT/scripts/qwen3_tts_cli.py"

if [[ ! -x "$PY" ]]; then
  echo "error: venv not found at $REPO_ROOT/.venv" >&2
  echo "  setup: cd \"$REPO_ROOT\" && python3.13 -m venv .venv && .venv/bin/pip install -e ." >&2
  exit 1
fi

exec "$PY" "$RUNNER" "$@"
