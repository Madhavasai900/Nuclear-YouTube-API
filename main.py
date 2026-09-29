from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import re

app = FastAPI(
    title="Nuclear YouTube API", 
    description="Ghost Mode RDX Edition - Extracts Transcripts and Metadata from YouTube Videos",
    version="Ghost-0.0001%"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_video_id(url: str):
    """Brutal regex to rip the Video ID from any YouTube URL format."""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if match:
        return match.group(1)
    return None

@app.get("/")
def home():
    return {
        "message": "SYSTEM ONLINE. Nuclear YouTube Transcript API is Running.",
        "trap_status": "$30/month Trap is ACTIVE.",
        "elite_level": "0.0001%"
    }

@app.get("/api/v1/extract")
def extract_youtube_data(url: str):
    """
    The Main RDX Payload.
    Takes a YouTube URL, rips the transcript text, and steals the metadata.
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL. Feed me a proper link.")
    
    try:
        # 1. Rip the Transcript (The Gold)
        try:
            api = YouTubeTranscriptApi()
            transcript_list = api.fetch(video_id)
            full_text = " ".join([t.text for t in transcript_list])
        except Exception as e:
            full_text = f"Transcript rip failed (Video might not have subs). Error: {str(e)}"
        
        # 2. Steal Basic Metadata (Title, Author, Thumbnail) via Public oEmbed
        meta_data = {}
        try:
            oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
            meta_resp = requests.get(oembed_url, timeout=5)
            if meta_resp.status_code == 200:
                meta_data = meta_resp.json()
        except:
            pass # Silent fail on metadata if YouTube blocks it, we still want the transcript
            
        return {
            "status": "success",
            "video_id": video_id,
            "metadata": {
                "title": meta_data.get("title", "Unknown"),
                "author": meta_data.get("author_name", "Unknown"),
                "thumbnail_url": meta_data.get("thumbnail_url", f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg")
            },
            "transcript_length": len(full_text),
            "transcript": full_text
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ghost Mode Error: {str(e)}")

# To run locally: uvicorn main:app --reload
