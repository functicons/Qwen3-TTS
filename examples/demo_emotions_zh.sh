#!/usr/bin/env bash
# Demo: same Chinese sentence, four different emotional renderings.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
CLI="$SCRIPT_DIR/../scripts/qwen3-tts-cli.sh"
OUT_DIR="$SCRIPT_DIR/out"
mkdir -p "$OUT_DIR"

TEXT="我等了你整整三个小时，你怎么现在才来？"
SPEAKER="Vivian"

declare -a CLIPS=(
  "neutral|"
  "angry|用非常愤怒、几乎要吼出来的语气说"
  "aggrieved|用委屈撒娇的语气说，声音颤抖，像快要哭出来一样"
  "sarcastic|用阴阳怪气、嘲讽的语气说，语速很慢"
)

for entry in "${CLIPS[@]}"; do
  label="${entry%%|*}"
  instruct="${entry#*|}"
  out="$OUT_DIR/zh_${label}.wav"
  echo ">>> [$label] $out"
  "$CLI" -t "$TEXT" -o "$out" -l Chinese -s "$SPEAKER" -i "$instruct"
done

echo
echo "Generated clips in $OUT_DIR:"
ls -la "$OUT_DIR"/zh_*.wav
