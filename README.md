# 📥 Advanced YouTube Local Video Downloader

A high-performance, concurrent YouTube download automation system. This tool utilizes a **local Python backend** (powered by `yt-dlp` and a lightweight `Flask` server) bridged with a **Tampermonkey UserScript** to provide fluid, card-based, multi-video download tracking directly inside your web browser (**Google Chrome** or **Brave**).

---

## ✨ Features
* **Contextual Interception:** Just hold `Ctrl` and `Right-Click` any thumbnail or active video on YouTube to trigger a download.
* **Dynamic Quality Extraction:** Automatically polls YouTube API metadata line-by-line to display *only* the true formats natively available for that specific video (up to 4K/8K resolution).
* **Multi-Video Parallel Stacking:** Supports downloading multiple videos at the same time with an elegant stacked card deck interface in the bottom right corner.
* **Live Dashboards:** Displays dynamic horizontal diagnostic rows tracking real-time download speeds, total sizes, remaining megabytes, and crisp progress bars.
* **Instant Abort Kill-Switch:** Click the `✕` close button on any live tracking card to forcefully terminate background network extraction streams instantly.

---

## 🛠️ Step-by-Step Installation Guide

### 🧱 Phase 1: Install Python & System Dependencies

#### **Step 1: Install Python**
1. Download the latest release version of [Python for Windows](https://www.python.org/downloads/).
2. ⚠️ **CRITICAL:** When launching the installer execution window, check the box at the bottom that reads **"Add python.exe to PATH"** before initiating installation parameters. Skipping this will break your system terminalbindings.

#### **Step 2: Install Python Libraries**
1. Open your Windows **Command Prompt** (`cmd`).
2. Run the following installation layout array block to fetch the background infrastructure dependencies:
   ```bash
   pip install yt-dlp Flask flask-cors
### **Step 3: Install FFmpeg (Required for HD/1080p/4K Merging)**
1. YouTube distributes high-definition video and audio metadata packages as entirely separate, distinct split stream paths. Without FFmpeg, yt-dlp will choke out at a      max capping point of 720p.

2. Download a pre-compiled Windows build of FFmpeg **(like the ones from gyan.dev).**

3. Extract the downloaded zip file.

4. Look inside the extracted folder for a folder named **bin**. Inside it, you will see **ffmpeg.exe.**

5. Copy ffmpeg.exe and paste it directly into the exact same folder where you intend to save your python script.

---

### **Phase 2: Save and Run the Python Server (downloader.py)**

1. Create a new folder on your computer **(e.g., C:\YouTubeDownloader).**

2. Make sure your **ffmpeg.exe** file is pasted inside this folder.

3. Save the repository's **downloader.py** file into this exact same directory.

4. Run the backend by double-clicking **downloader.py** or executing it via command prompt:

5. **python downloader.py**

---

### **Phase 3: Setup the Browser Extension (Brave or Chrome)**

1. Install the **Tampermonkey extension** from the official Chrome Web Store.

2. Open the Tampermonkey Dashboard, click the "Create a new script" button (the + icon).

3. Open the Tampermonkey UserScript file provided in this repository, copy its entire contents, paste it into the editor, and click save (Ctrl + S).

4. Reload YouTube inside your browser using **Ctrl + F5.**

---

### **🚀 Phase 4: Run Silently on Windows Startup (Optional)**

1. If you wish to enjoy fluid automated download shortcuts automatically every time your machine boots up without opening a console terminal window manually, use the       built-in startup script:

2. Hit Win + R keys to pop open the Windows Run dialog prompt utility row.

3. Type **shell:startup** and strike Enter to access your personal Windows Startup folder.

4. Copy the **youtube_server.vbs** script file provided in this repository and paste it directly into this startup folder.

**Optional: If your installation directory is not C:\YouTubeDownloader, right-click **youtube_server.vbs**, select Edit, and update the directory location to match your folder pathway.**

---

### **🎯 Phase 5: Verification & Usage Loop**

1. Head over to YouTube inside Chrome or Brave and reload the tab entirely via Ctrl + F5.

2. Find any video thumbnail on the home screen, or open a video player watch page.

3. Hold down the **Ctrl key on your keyboard and Right-Click the video asset.**

What happens:

1. A clean dashboard card appears in the bottom right corner showing "🔍 Fetching Formats...".

2. The Tkinter resolution box opens on your desktop containing the exact, true video resolutions found for that specific video clip (e.g., 2160p (4K), 1440p, 1080p).

3. Pick your format and hit Start Download. The progress bar switches to a red line and tracks data transfers live.

4. Clicking ✕ on the card kills the download process immediately, prints an active cancellation indicator, and safely pulls the overlay away from your screen.
