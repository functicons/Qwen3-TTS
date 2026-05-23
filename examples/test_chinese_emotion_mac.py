# Chinese emotion-control demo: same text, neutral vs. aggrieved/teary tone.
import time
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

device = "mps" if torch.backends.mps.is_available() else "cpu"
dtype = torch.float32
model_path = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"

print(f"loading {model_path} on {device}...", flush=True)
t0 = time.time()
tts = Qwen3TTSModel.from_pretrained(
    model_path,
    device_map=device,
    dtype=dtype,
    attn_implementation="sdpa",
)
print(f"[load] {time.time() - t0:.2f}s", flush=True)

text = "我等了你整整三个小时，你怎么现在才来？"
speaker = "Vivian"

clips = [
    ("qwen3_tts_zh_neutral.wav",   "",                                              "neutral"),
    ("qwen3_tts_zh_aggrieved.wav", "用委屈撒娇的语气说，声音颤抖，像快要哭出来一样", "aggrieved/teary"),
]

for out, instruct, label in clips:
    t0 = time.time()
    wavs, sr = tts.generate_custom_voice(
        text=text,
        language="Chinese",
        speaker=speaker,
        instruct=instruct,
    )
    dur = len(wavs[0]) / sr
    print(f"[{label}] gen={time.time()-t0:.2f}s  dur={dur:.2f}s  -> {out}", flush=True)
    sf.write(out, wavs[0], sr)
