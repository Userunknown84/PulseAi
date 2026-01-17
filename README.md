## 🎯 PulsePoint AI – Viral Reel Generator

PulsePoint AI is a web application that converts long-form videos into 3–5 short, viral reels using AI.
Users can upload a local video or provide a YouTube / Google Drive link, and the app automatically:

->Transcribes audio (if available)

->Detects viral moments using AI

->Cuts the video into short reels

->Allows preview & download of reels

## 🎥 Demo
👉 [Watch Demo Video](https://drive.google.com/file/d/1O7YofQcaeJJz5Wc2lU32hclH_aZEz_xI/view?usp=drive_link)

🚀 Features

-> Upload local video (MP4 / MOV / MKV)
-> Process YouTube or Google Drive links
-> Automatic audio transcription using Whisper
-> Multi-language → English transcription
-> AI-based viral moment detection
-> Generates 3–5 short reels automatically
-> Works even if video has no audio
-> Fast reel generation using FFmpeg
-> Streamlit-based clean UI

## 🧠 How It Works

Video Input:

->Upload a local video OR

->Paste a YouTube / Google Drive link

Transcription:

->If audio exists → transcribed using OpenAI Whisper

->If no audio → video is split intelligently by duration

AI Moment Detection:

->Transcript is analyzed using Gemini (Flash) model

->Identifies 3–5 high-engagement moments

Reel Generation:

->FFmpeg cuts the original video into short reels

->Reels are previewed and downloadable

## 🛠️ Tech Stack

| Component        | Technology            |
| ---------------- | --------------------- |
| Frontend         | Streamlit             |
| Speech-to-Text   | OpenAI Whisper        |
| AI Analysis      | Google Gemini (Flash) |
| Video Processing | FFmpeg                |
| Video Handling   | MoviePy               |
| Link Download    | yt-dlp                |
| Language         | Python                |


## 🔑 Environment Variables

Create a .env file:

GENAI_API_KEY=your_google_gemini_api_key

## How to Run Locally

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py. or /opt/anaconda3/bin/python -m streamlit run app.py

## Dependencies

streamlit
python-dotenv
openai-whisper
moviepy
google-generativeai
yt-dlp
ffmpeg
requests

## Team

Built for ByteSize Sage AI Hackathon
By Aditya Sharma

