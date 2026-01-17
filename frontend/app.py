import streamlit as st
import os
import whisper
from moviepy.editor import VideoFileClip
import tempfile
import yt_dlp
import subprocess
import requests
import re


st.set_page_config(page_title="PulsePoint AI", layout="centered")
st.title("🎯 PulsePoint AI")
st.write("Turn long videos into viral short reels using AI")


@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

whisper_model = load_whisper()


def cut_clip_ffmpeg(input_path, output_path, start, end):
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ss", str(start),
        "-to", str(end),
        "-c", "copy",
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def create_reels(video_path, moments):
    reels = []
    clip = VideoFileClip(video_path)
    for i, (start, end) in enumerate(moments):
        if start >= clip.duration:
            continue
        end = min(end, clip.duration)
        reel_path = tempfile.mktemp(suffix=f"_reel{i+1}.mp4")
        cut_clip_ffmpeg(video_path, reel_path, start, end)
        reels.append(reel_path)
    return reels


def auto_moments(video_path, transcript):
    clip = VideoFileClip(video_path)
    duration = int(clip.duration)
    if transcript == "No audio available.":
        step = max(duration // 5, 5)
    else:
        step = max(duration // 5, 10)
    moments = [(i, min(i + step, duration)) for i in range(0, duration, step)]
    return moments


def process_video(video_path):
    try:
        clip = VideoFileClip(video_path)
        audio_path = tempfile.mktemp(suffix=".wav")

        
        if clip.audio is None:
            transcript = "No audio available."
            st.warning("No audio found in video.")
        else:
            clip.audio.write_audiofile(audio_path, logger=None)
            result = whisper_model.transcribe(audio_path, task="translate", language="en")
            transcript = result["text"]

        st.subheader("📝 Transcript")
        st.write(transcript)

   
        moments = auto_moments(video_path, transcript)

      
        reels = create_reels(video_path, moments)
        if not reels:
            st.error("No reels could be generated.")
            return

        st.success(f"🎬 {len(reels)} reels generated!")
        for i, reel in enumerate(reels):
            st.video(reel)
            with open(reel, "rb") as f:
                st.download_button(f"Download Reel {i+1}", f, file_name=f"reel_{i+1}.mp4", mime="video/mp4")

    except Exception as e:
        st.error(f"Failed to process video: {e}")


video_file = st.file_uploader("Upload local video", type=["mp4", "mov", "mkv"])
video_link = st.text_input("Or paste YouTube / Google Drive link")


if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(video_file.read())
        path = tmp.name
    if st.button("Transcribe & Generate Reels (Local Video)"):
        process_video(path)


if video_link:
    if st.button("Transcribe & Generate Reels (Link Video)"):
        temp_video = tempfile.mktemp(suffix=".mp4")
        if "youtube" in video_link:
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "outtmpl": temp_video,
                "merge_output_format": "mp4",
                "quiet": True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_link])
        elif "drive.google.com" in video_link:
            file_id = re.search(r"/d/([^/]+)", video_link)
            if not file_id:
                st.error("Invalid Drive link")
                st.stop()
            url = f"https://drive.google.com/uc?export=download&id={file_id.group(1)}"
            r = requests.get(url, stream=True)
            with open(temp_video, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
        else:
            st.error("Only YouTube or Drive supported")
            st.stop()
        process_video(temp_video)
