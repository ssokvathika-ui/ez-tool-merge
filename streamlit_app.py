# streamlit_app.py - ez-tool-merge
import streamlit as st
import subprocess
import os
import tempfile
import shutil
import requests
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# App Title & Description
# -----------------------------
st.title("🎥➕🔊 ez-tool-merge")
st.markdown("""
**Simple Audio + Video Merger**  
Upload files or paste direct links to merge audio and video.

✅ Supports: `.mp4`, `.webm`, `.mkv`, `.m4a`, etc.  
🧹 Temp files are deleted after merge.  
📦 Built for Streamlit Cloud.
""")

# -----------------------------
# Check for ffmpeg
# -----------------------------
@st.cache_resource
def check_ffmpeg():
    return shutil.which("ffmpeg") is not None

if not check_ffmpeg():
    st.error("❌ `ffmpeg` not found! Make sure `packages.txt` with `ffmpeg` is in your repo.")
    st.info("""
    Create a file named `packages.txt` in your repo:
    ```
    ffmpeg
    ```
    """)
    st.stop()

# -----------------------------
# Input Section
# -----------------------------
st.header("📥 Input Sources")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎥 Video Source")
    video_option = st.radio("Choose video input:", ["Upload File", "Direct URL"])
    video_file = st.file_uploader("Upload video", type=["mp4", "webm", "mkv"], key="v1")
    video_url = st.text_input("Or enter video URL") if video_option == "Direct URL" else None

with col2:
    st.subheader("🔊 Audio Source")
    audio_option = st.radio("Choose audio input:", ["Upload File", "Direct URL"])
    audio_file = st.file_uploader("Upload audio", type=["m4a", "wav", "mp3", "webm", "aac"], key="a1")
    audio_url = st.text_input("Or enter audio URL") if audio_option == "Direct URL" else None


# -----------------------------
# Validate Inputs
# -----------------------------
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

# Check if we have valid inputs
has_video = (video_file is not None) or (video_url and is_valid_url(video_url))
has_audio = (audio_file is not None) or (audio_url and is_valid_url(audio_url))

if not has_video or not has_audio:
    st.info("Please provide both audio and video sources to continue.")
    st.stop()

# -----------------------------
# Download Helper
# -----------------------------
def download_file(url: str, dest_path: str, desc: str) -> bool:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.youtube.com/",
        }
        with requests.get(url, stream=True, headers=headers, timeout=120) as r:
            r.raise_for_status()
            total_size = int(r.headers.get("content-length", 0))
            downloaded = 0
            with open(dest_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            pct = min(100.0, (downloaded / total_size) * 100)
                            st.session_state[f'progress_{desc}'] = pct
        return True
    except Exception as e:
        st.session_state[f'error_{desc}'] = str(e)
        return False

# -----------------------------
# Merge Function
# -----------------------------
def merge_streams(video_path: str, audio_path: str, output_path: str) -> tuple[bool, str]:
    try:
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "copy",
            "-f", "webm",
            "-y", output_path
        ]
        logger.info(f"Running FFmpeg: {' '.join(cmd)}")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
        if result.returncode != 0:
            return False, result.stderr.decode('utf-8', errors='ignore')
        return True, "Success"
    except Exception as e:
        return False, str(e)

# -----------------------------
# Processing
# -----------------------------
if st.button("🎬 Merge Audio & Video"):
    temp_dir = tempfile.mkdtemp(prefix="ez_merge_")
    video_temp = None
    audio_temp = None
    output_file = None
    success = False

    try:
        # Progress placeholders
        st.session_state['progress_video'] = 0
        st.session_state['progress_audio'] = 0
        st.session_state['error_video'] = None
        st.session_state['error_audio'] = None

        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text("📥 Downloading or loading files...")

        # --- Handle Video ---
        if video_file:
            video_temp = os.path.join(temp_dir, "input_video" + os.path.splitext(video_file.name)[1])
            with open(video_temp, "wb") as f:
                f.write(video_file.read())
            st.session_state['progress_video'] = 100
        else:
            video_temp = os.path.join(temp_dir, "input_video.webm")
            if not download_file(video_url, video_temp, "video"):
                raise Exception(f"Download failed for video: {st.session_state['error_video']}")

        # --- Handle Audio ---
        if audio_file:
            audio_temp = os.path.join(temp_dir, "input_audio" + os.path.splitext(audio_file.name)[1])
            with open(audio_temp, "wb") as f:
                f.write(audio_file.read())
            st.session_state['progress_audio'] = 100
        else:
            audio_temp = os.path.join(temp_dir, "input_audio.webm")
            if not download_file(audio_url, audio_temp, "audio"):
                raise Exception(f"Download failed for audio: {st.session_state['error_audio']}")

        # --- Merge ---
        status_text.text("🔄 Merging streams...")
        progress_bar.progress(0.5)

        output_file = os.path.join(temp_dir, "merged_output.webm")
        success, msg = merge_streams(video_temp, audio_temp, output_file)

        if not success:
            raise Exception(f"Merge failed: {msg}")

        # --- Success ---
        progress_bar.progress(1.0)
        status_text.text("✅ Merge complete!")

        # Read merged file for download
        with open(output_file, "rb") as f:
            merged_data = f.read()

        st.success("🎉 Merged file is ready!")

        # Download button
        st.download_button(
            label="⬇️ Download Merged Video (.webm)",
            data=merged_data,
            file_name="merged_output.webm",
            mime="video/webm"
        )

    except Exception as e:
        st.error(f"❌ Operation failed: {str(e)}")
        logger.error(f"Merge failed: {e}")
    finally:
        # --- Cleanup ---
        status_text.text("🧹 Cleaning up temporary files...")
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                logger.info("Temporary files deleted.")
            except Exception as e:
                logger.error(f"Cleanup failed: {e}")
        if not success:
            progress_bar.empty()
