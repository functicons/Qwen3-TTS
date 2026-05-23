"""Single-shot CLI runner for Qwen3-TTS CustomVoice models.

Loads the model, synthesizes one clip, writes a WAV. Designed to be invoked
through scripts/qwen3-tts-cli.sh which handles venv activation. Status lines
go to stderr; the resulting output path is echoed to stdout so callers can
capture it.
"""
import argparse
import sys
import time

import soundfile as sf
import torch

from qwen_tts import Qwen3TTSModel


def pick_device(flag: str) -> str:
    if flag != "auto":
        return flag
    if torch.cuda.is_available():
        return "cuda:0"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def main() -> None:
    p = argparse.ArgumentParser(
        prog="qwen3-tts-cli",
        description="Synthesize one WAV with Qwen3-TTS CustomVoice.",
    )
    p.add_argument("-t", "--text", required=True, help="text to synthesize")
    p.add_argument("-o", "--out", required=True, help="output .wav path")
    p.add_argument("-l", "--lang", default="English",
                   help="language name (English, Chinese, Japanese, Korean, German, French, Russian, Portuguese, Spanish, Italian)")
    p.add_argument("-s", "--speaker", default="Ryan",
                   help="speaker name (e.g. Ryan, Vivian) — see model card")
    p.add_argument("-i", "--instruct", default="",
                   help='natural-language style/emotion instruction (e.g. "Very happy.", "用悲伤的语气说")')
    p.add_argument("-m", "--model", default="Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
                   help="HF model id (0.6B/1.7B CustomVoice)")
    p.add_argument("--device", default="auto",
                   choices=["auto", "cpu", "mps", "cuda:0"])
    args = p.parse_args()

    device = pick_device(args.device)
    dtype = torch.float32  # safe across CPU/MPS; CUDA users can edit if needed.
    print(f"[device] {device} [model] {args.model}", file=sys.stderr, flush=True)

    t0 = time.time()
    tts = Qwen3TTSModel.from_pretrained(
        args.model,
        device_map=device,
        dtype=dtype,
        attn_implementation="sdpa",
    )
    print(f"[load] {time.time() - t0:.2f}s", file=sys.stderr, flush=True)

    t0 = time.time()
    wavs, sr = tts.generate_custom_voice(
        text=args.text,
        language=args.lang,
        speaker=args.speaker,
        instruct=args.instruct,
    )
    dur = len(wavs[0]) / sr
    print(f"[generate] {time.time() - t0:.2f}s dur={dur:.2f}s sr={sr}",
          file=sys.stderr, flush=True)

    sf.write(args.out, wavs[0], sr)
    print(args.out)


if __name__ == "__main__":
    main()
