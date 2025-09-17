# 🎬 YouTube Playlist Downloader 2025  

A simple yet powerful GUI application built with **Python** and **PyQt6** to download videos or entire playlists from YouTube with selectable quality and output directory. It automatically merges video and audio into a single MP4 file using FFmpeg.  

---

## 🚀 Features  

- Download entire playlists or individual videos.  
- Choose download quality (Best / 1080 / 720 / 480 / 360).  
- Graphical interface built with PyQt6.  
- Select custom output folder for downloads.  
- Automatically merges audio and video with FFmpeg.  

---

## 📝 Requirements  

Before running the script, make sure you have:

1. **Python 3.9+**  
   [Download Python](https://www.python.org/downloads/)

2. **Install Python dependencies**  
   All dependencies are listed in `requirements.txt`.  
   Run the following inside the project folder:  
   ```bash
   pip install -r requirements.txt
   ```

3. **FFmpeg** (required for merging audio & video):  
   - Download FFmpeg from the official site: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)  
   - Extract it and place it in a path like: `C:\ffmpeg`  
   - Ensure the executable exists at:  
     ```
     C:\ffmpeg\bin\ffmpeg.exe
     ```
   - *(Optional but recommended)*: Add `C:\ffmpeg\bin` to your system PATH for easier access.

---

## ⚙️ How to Run  

Clone or download the repository:  

```bash
git clone https://github.com/USERNAME/YoutubePlaylistDownloader.git
cd YoutubePlaylistDownloader
```

Install dependencies:  

```bash
pip install -r requirements.txt
```

Run the application:  

```bash
python app.py
```

In the GUI:  

- Paste the playlist URL.  
- Choose the download folder.  
- Select quality.  
- Click **Load Playlist Videos** to fetch the video list.  
- Check the videos you want to download.  
- Click **Start Download**.  

---

## 📂 Project Structure  

```
YouTubePlaylistDownloader/
│
├─ app.py           ← Main application script  
├─ requirements.txt ← Required Python packages  
├─ README.md        ← This file  
└─ LICENSE          ← License file (MIT by Kiro Nagy)
```

*(You can add a folder `images/` with screenshots and link them here.)*

---

## ⚠️ Notes  

- This application uses `yt-dlp`, a powerful and actively maintained fork of `youtube-dl`.  
- If FFmpeg is missing, the app will prompt you with a warning.  
- Output file names are automatically generated from the YouTube video title.  
- All downloads are automatically converted to MP4 format.  

---

## ⚖️ License  

This project is licensed under the **MIT License** © 2025 [Kiro Nagy](LICENSE).
