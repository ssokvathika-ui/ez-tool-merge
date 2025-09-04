# ez-tool-merge

# 🎥➕🔊 ez-tool-merge

A simple, no-nonsense tool to **merge audio and video streams** — whether from **direct URLs** or **local files**.

Perfect for combining:
- Audio from YouTube (`.m4a`, `.webm`)
- Video without sound (`.mp4`, `.webm`)
- Podcasts, lectures, meditative content, and more!

Built with Streamlit and `ffmpeg`, hosted on Streamlit Cloud — **temp files are cleaned up automatically**.

🎯 **One job. Done right.**

---

## 🌐 Try It Live

👉 **[Try ez-tool-merge on Streamlit](https://your-username.streamlit.app/ez-tool-merge)**  
*(Replace with your actual deployment link)*

---

## 🚀 Features

✅ Merge audio + video from:
- 🔗 **Direct download links** (e.g., from `silent-echo`)
- 📁 **Uploaded local files**

🛠️ Supports common formats:
- Video: `.mp4`, `.webm`, `.mkv`
- Audio: `.m4a`, `.webm`, `.mp3`, `.wav`, `.aac`

🧹 **Automatic cleanup**: All temporary files are deleted after merge.

📦 **Cloud-ready**: Designed to run on **Streamlit Cloud** with zero config.

---

## 🖼️ Screenshot

![ez-tool-merge interface](https://via.placeholder.com/800x500?text=ez-tool-merge+Interface)

*(Replace with actual screenshot later)*

---

## 💡 How to Use

1. **Enter or upload your video source** (with video, no audio)
2. **Enter or upload your audio source** (with audio, no video)
3. Click **"Merge Audio & Video"**
4. Wait for the process to complete
5. Download the merged `.webm` file

> 🌐 Tip: Use this with direct links from tools like [Silent Echo Studio](https://github.com/your-username/silent-echo)!

---

## ⚙️ Local Setup (Developers)

### Prerequisites
- Python 3.8+
- `ffmpeg` installed on your system

### Installation
```bash
git clone https://github.com/your-username/ez-tool-merge.git
cd ez-tool-merge

# Install Python dependencies
pip install -r requirements.txt
