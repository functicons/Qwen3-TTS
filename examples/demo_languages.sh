#!/usr/bin/env bash
# Demo: the same greeting in four different languages.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
CLI="$SCRIPT_DIR/../scripts/qwen3-tts-cli.sh"
OUT_DIR="$SCRIPT_DIR/out"
mkdir -p "$OUT_DIR"

# Each entry: label|lang|speaker|text
declare -a CLIPS=(
  "en|English|Ryan|Welcome to the Qwen Text to Speech demo. I hope you enjoy it."
  "zh|Chinese|Vivian|欢迎来到通义千问语音合成的演示，希望你喜欢。"
  "ja|Japanese|Vivian|Qwen音声合成のデモへようこそ。お楽しみください。"
  "fr|French|Ryan|Bienvenue dans la démo de synthèse vocale Qwen. J'espère que cela vous plaira."
)

INSTRUCT="Cheerful and welcoming."

for entry in "${CLIPS[@]}"; do
  IFS='|' read -r label lang speaker text <<<"$entry"
  out="$OUT_DIR/lang_${label}.wav"
  echo ">>> [$label / $lang / $speaker] $out"
  "$CLI" -t "$text" -o "$out" -l "$lang" -s "$speaker" -i "$INSTRUCT"
done

echo
echo "Generated clips in $OUT_DIR:"
ls -la "$OUT_DIR"/lang_*.wav
