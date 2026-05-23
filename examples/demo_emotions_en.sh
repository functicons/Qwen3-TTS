#!/usr/bin/env bash
# Demo: same English sentence, four different emotional renderings.
# Each invocation reloads the model (~4s), so total runtime is ~60-80s.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
CLI="$SCRIPT_DIR/../scripts/qwen3-tts-cli.sh"
OUT_DIR="$SCRIPT_DIR/out"
mkdir -p "$OUT_DIR"

TEXT="I cannot believe you actually did that. Why on earth would you do something like that?"
SPEAKER="Ryan"

declare -a CLIPS=(
  "neutral|"
  "angry|Furious and shouting."
  "sad|Sad and disappointed, almost sighing."
  "whisper|A quiet, conspiratorial whisper."
)

for entry in "${CLIPS[@]}"; do
  label="${entry%%|*}"
  instruct="${entry#*|}"
  out="$OUT_DIR/en_${label}.wav"
  echo ">>> [$label] $out"
  "$CLI" -t "$TEXT" -o "$out" -l English -s "$SPEAKER" -i "$instruct"
done

echo
echo "Generated clips in $OUT_DIR:"
ls -la "$OUT_DIR"/en_*.wav
