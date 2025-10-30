# utility/audio/audio_generator.py
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)
# voice: one of ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
# response_format: "mp3", "wav", "opus", "flac", "aac"
async def generate_audio(text: str, outputFilename: str,
                         model: str = "tts-1",
                         voice: str = "echo",
                         response_format: str = None,
                         speed: float = 1.0) -> None:
    # Infer format from filename extension if not set
    ext = Path(outputFilename).suffix.lower().lstrip(".")
    fmt = response_format or (ext if ext in {"mp3", "wav", "opus", "flac", "aac"} else "mp3")

    # OpenAI TTS is synchronous; call and stream to file
    resp = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        response_format=fmt,
        speed=speed
    )
    resp.stream_to_file(outputFilename)
