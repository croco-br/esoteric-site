import io
import json
import threading
from pathlib import Path

import numpy as np
from scipy.io.wavfile import write

with (Path(__file__).resolve().parents[1] / "db.json").open("r") as f:
    db = json.load(f)

SAMPLE_RATE = 48000
DURATION = 30  # seconds

# Deterministic output per note name -> cache the encoded WAV bytes so
# repeated requests skip synthesis and encoding entirely.
_audio_cache: dict[str, bytes | None] = {}
_cache_lock = threading.Lock()


def generate_audio(name: str):
    """Return a BytesIO with the cached WAV audio for a note, or None."""
    with _cache_lock:
        if name in _audio_cache:
            cached = _audio_cache[name]
            return io.BytesIO(cached) if cached is not None else None

    audio_bytes = _render_audio(name)

    with _cache_lock:
        _audio_cache[name] = audio_bytes

    return io.BytesIO(audio_bytes) if audio_bytes is not None else None


def _render_audio(name: str) -> bytes | None:
    note_frequencies = db.get(name, {}).get("frequencies", [])
    if not note_frequencies:
        return None

    t = np.linspace(0, DURATION, SAMPLE_RATE * DURATION, endpoint=False)
    audio_data = np.zeros_like(t)

    # Generate sound by combining frequencies.
    for freq in note_frequencies:
        audio_data += 0.25 * np.sin(2 * np.pi * freq * t)

    # Normalize the sound to avoid clipping.
    audio_data /= np.max(np.abs(audio_data))

    # Convert to 16-bit PCM format (half the payload of 32-bit).
    audio_data = (audio_data * 32767).astype(np.int16)

    buffer = io.BytesIO()
    write(buffer, SAMPLE_RATE, audio_data)
    return buffer.getvalue()
