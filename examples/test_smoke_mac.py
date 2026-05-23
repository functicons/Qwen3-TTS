# Smoke test for Apple Silicon Macs (no CUDA / no flash-attn).
# Uses the 0.6B CustomVoice model + float32 to avoid MPS fp16 NaN in softmax.
import time
import torch
import soundfile as sf

from qwen_tts import Qwen3TTSModel


def pick_device():
    if torch.cuda.is_available():
        return "cuda:0"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def main():
    device = pick_device()
    dtype = torch.float32
    model_path = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"

    print(f"device={device} dtype={dtype} model={model_path}", flush=True)

    t0 = time.time()
    tts = Qwen3TTSModel.from_pretrained(
        model_path,
        device_map=device,
        dtype=dtype,
        attn_implementation="sdpa",
    )
    print(f"[load] {time.time() - t0:.2f}s", flush=True)

    t0 = time.time()
    wavs, sr = tts.generate_custom_voice(
        text="Hello from Qwen3 TTS, running on Apple Silicon.",
        language="English",
        speaker="Ryan",
        instruct="Cheerful and friendly.",
    )
    print(f"[generate] {time.time() - t0:.2f}s  sr={sr}  samples={len(wavs[0])}", flush=True)

    out = "qwen3_tts_smoke_mac.wav"
    sf.write(out, wavs[0], sr)
    print(f"[wrote] {out}", flush=True)


if __name__ == "__main__":
    main()
