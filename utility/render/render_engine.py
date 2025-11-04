import time
import os
import tempfile
import zipfile
import platform
import subprocess
from moviepy.editor import (AudioFileClip, CompositeVideoClip, CompositeAudioClip, ImageClip,
                            TextClip, VideoFileClip, ColorClip)
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
import requests

def download_file(url, filename):
    print(f"[RENDER] Downloading video: {url}")
    with open(filename, 'wb') as f:
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        f.write(response.content)
    try:
        size_mb = os.path.getsize(filename) / (1024 * 1024)
        print(f"[RENDER] Downloaded to {filename} ({size_mb:.2f} MB)")
    except Exception:
        pass

def search_program(program_name):
    try: 
        search_cmd = "where" if platform.system() == "Windows" else "which"
        return subprocess.check_output([search_cmd, program_name], stderr=subprocess.DEVNULL).decode().strip()
    except subprocess.CalledProcessError:
        return None

def get_program_path(program_name):
    program_path = search_program(program_name)
    return program_path

def get_output_media(audio_file_path, timed_captions, background_video_data, video_server):
    OUTPUT_FILE_NAME = "rendered_video.mp4"
    magick_path = get_program_path("magick")
    imagemagick_available = False
    if magick_path:
        os.environ['IMAGEMAGICK_BINARY'] = magick_path
        imagemagick_available = True
    
    print("[RENDER] Starting composition pipeline...")
    visual_clips = []
    temp_video_paths = []
    for (t1, t2), video_url in background_video_data:
        if not video_url:
            continue
        try:
            # Download the video file
            # Use .mp4 suffix so ffmpeg/moviepy can infer the correct reader on Windows
            video_filename = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
            download_file(video_url, video_filename)
            temp_video_paths.append(video_filename)
            
            # Create VideoFileClip from the downloaded file
            print(f"[RENDER] Creating clip from {video_filename}")
            video_clip = VideoFileClip(video_filename)
            # Trim the clip to the target interval length and position at t1
            interval_duration = max(0.1, float(t2) - float(t1))
            video_clip = video_clip.subclip(0, min(interval_duration, video_clip.duration))
            video_clip = video_clip.set_start(t1)
            visual_clips.append(video_clip)
        except Exception as e:
            print(f"[RENDER] Skipping video due to error: {e}")
            continue
    
    audio_clips = []
    audio_file_clip = AudioFileClip(audio_file_path)
    audio_clips.append(audio_file_clip)

    if imagemagick_available:
        for (t1, t2), text in timed_captions:
            try:
                text_clip = TextClip(txt=text, fontsize=100, color="white", stroke_width=3, stroke_color="black", method="label")
                text_clip = text_clip.set_start(t1)
                text_clip = text_clip.set_end(t2)
                text_clip = text_clip.set_position(["center", 800])
                visual_clips.append(text_clip)
            except Exception:
                # If TextClip fails, skip subtitle for this segment
                continue

    # If no visual clips could be created, fall back to a solid black background
    if not visual_clips:
        # 1920x1080 black clip as background
        fallback_duration = 1.0
        try:
            audio_probe = AudioFileClip(audio_file_path)
            fallback_duration = max(fallback_duration, float(audio_probe.duration))
            audio_probe.close()
        except Exception:
            pass
        print("[RENDER] No visual clips found. Using black background fallback.")
        visual_clips = [ColorClip(size=(1920, 1080), color=(0, 0, 0)).set_duration(fallback_duration)]

    video = CompositeVideoClip(visual_clips)
    
    if audio_clips:
        audio = CompositeAudioClip(audio_clips)
        video.duration = audio.duration
        video.audio = audio

    print("[RENDER] Starting ffmpeg encoding...")
    video.write_videofile(
        OUTPUT_FILE_NAME,
        codec='libx264',
        audio_codec='aac',
        fps=25,
        preset='veryfast',
        threads=4,
        logger='bar'
    )
    print(f"[RENDER] Encoding complete: {OUTPUT_FILE_NAME}")

    try:
        video.close()
    except Exception:
        pass
    
    # Clean up downloaded files
    for video_filename in temp_video_paths:
        try:
            os.remove(video_filename)
        except Exception:
            pass

    return OUTPUT_FILE_NAME