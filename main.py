import chainlit as cl
import asyncio
import os
from utility.script.script_generator import generate_script
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals
from utility.render.render_engine import get_output_media

def announce(msg):
    return cl.Message(content=msg, author="system")

@cl.on_message
async def main_chat(message: cl.Message):
    # 1. Input: Sanskrit from user
    sanskrit_text = message.content.strip()
    await cl.Message(content="Translating Sanskrit and creating story with a moral...", author="system").send()

    try:
        # 2. Generate story with moral (calls OpenAI sync, so use thread executor)
        loop = asyncio.get_running_loop()
        script = await loop.run_in_executor(None, generate_script, sanskrit_text)
        await cl.Message(content=f"Story generated!\n\n**{script}**", author="system").send()
    except Exception as e:
        await cl.Message(content=f"❌ Error during story generation: {e}", author="system").send()
        return

    # 3. Generate Audio
    audio_file = "audio_tts.wav"
    await cl.Message(content="Generating narration audio for the story...", author="system").send()
    try:
        await generate_audio(script, audio_file)
        await cl.Message(content="Audio generated!", author="system").send()
    except Exception as e:
        await cl.Message(content=f"❌ Error during audio generation: {e}", author="system").send()
        return

    # 4. Generate timed captions
    await cl.Message(content="Generating captions...", author="system").send()
    try:
        loop = asyncio.get_running_loop()
        timed_captions = await loop.run_in_executor(None, generate_timed_captions, audio_file)
        await cl.Message(content="Timed captions complete!", author="system").send()
    except Exception as e:
        await cl.Message(content=f"❌ Error during caption generation: {e}", author="system").send()
        return

    # 5. Video search queries
    await cl.Message(content="Generating relevant video search queries...", author="system").send()
    try:
        loop = asyncio.get_running_loop()
        search_terms = await loop.run_in_executor(None, getVideoSearchQueriesTimed, script, timed_captions)
        await cl.Message(content=f"Search terms created!", author="system").send()
    except Exception as e:
        await cl.Message(content=f"❌ Error during video search query generation: {e}", author="system").send()
        return

    # 6. Get background videos
    await cl.Message(content="Locating background videos...", author="system").send()
    video_server = "pexel"
    try:
        loop = asyncio.get_running_loop()
        background_video_urls = await loop.run_in_executor(None, generate_video_url, search_terms, video_server)
        background_video_urls = await loop.run_in_executor(None, merge_empty_intervals, background_video_urls)
        await cl.Message(content="Background videos found!", author="system").send()
    except Exception as e:
        await cl.Message(content=f"❌ Error during video search: {e}", author="system").send()
        return

    # 7. Render video
    await cl.Message(content="Rendering your moral story video, please wait...", author="system").send()
    video_file = None
    try:
        loop = asyncio.get_running_loop()
        video_file = await loop.run_in_executor(
            None, get_output_media, audio_file, timed_captions, background_video_urls, video_server
        )
    except Exception as e:
        await cl.Message(content=f"❌ Error during video rendering: {e}", author="system").send()
        return

    # 8. Return video
    if os.path.exists(video_file):
        await cl.Message(content="✅ Here is your generated video:").send()
        await cl.Message(elements=[cl.Video(name=os.path.basename(video_file), path=video_file)], content="").send()
    else:
        await cl.Message(content="❌ Video file was not found.", author="system").send()
