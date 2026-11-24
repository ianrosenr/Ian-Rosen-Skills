"""Narration helper for Manim scenes: Kokoro text-to-speech, cached per sentence."""
import hashlib
from pathlib import Path

import numpy as np
import soundfile as sf
from manim import Scene

VOICE = "af_heart"
_CACHE = Path(__file__).parent / "media" / "voice"
_pipeline = None


def _tts(text: str) -> tuple[Path, float]:
    global _pipeline
    _CACHE.mkdir(parents=True, exist_ok=True)
    path = _CACHE / (hashlib.sha1(f"{VOICE}:{text}".encode()).hexdigest()[:16] + ".wav")
    if not path.exists():
        if _pipeline is None:
            from kokoro import KPipeline
            _pipeline = KPipeline(lang_code="a")
        audio = np.concatenate([a for _, _, a in _pipeline(text, voice=VOICE)])
        sf.write(path, audio, 24000)
    return path, sf.info(path).duration


class Narrated(Scene):
    def say(self, text: str) -> float:
        """Start narration; returns its length in seconds so animations can match it."""
        path, seconds = _tts(text)
        self.add_sound(str(path))
        return seconds
