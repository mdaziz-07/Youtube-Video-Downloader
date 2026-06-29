*Phase 1: Install Python & System Dependencies*
*Step 1*: Install Python
Download the latest version of Python for Windows from the official website.

CRITICAL: When running the installer, make sure to check the box at the bottom that says "Add python.exe to PATH" before clicking install. If you skip this, your terminal won't recognize python commands.

*Step 2*: Install the Required Libraries
Open your Windows Command Prompt (cmd).

Run the following command to install the background server infrastructure and download engine:

pip install yt-dlp Flask flask-cors

*Step 3*: Install FFmpeg (Required for 1080p / 4K Merging)
YouTube serves high-definition video and audio as two separate tracks. Without a tool called FFmpeg, yt-dlp can only download low-quality videos (usually 720p or lower).

Download a pre-compiled Windows build of FFmpeg (like the ones from gyan.dev).

Extract the downloaded zip file.

Look inside the extracted folder for a folder named bin. Inside it, you will see ffmpeg.exe.

Copy ffmpeg.exe and paste it directly into the exact same folder where you intend to save your python script.

*Phase 2*: Save and Run the Python Server (downloader.py)
Create a new folder on your computer (e.g., C:\YouTubeDownloader).

Make sure your ffmpeg.exe file is pasted inside this folder.

Open Notepad, paste the downloader.py code entirely, and save it as downloader.py inside that folder (make sure to select "All Files (.)" in Notepad so it doesn't save as a .txt file):
python downloader.py
Keep this terminal window running in the background.

*Phase 3*: Browser Setup (Brave & Google Chrome)
The browser code handles everything via safe dynamic nodes to fully protect against Brave and Chrome's strict Trusted Types / CSP sandboxing frameworks.

*Step 1*: Install Tampermonkey
For Google Chrome: Install Tampermonkey from the Chrome Web Store.

For Brave Browser: Install the exact same extension from the Chrome Web Store link.

*Step 2*: Install the Universal UserScript
Click the Tampermonkey extension icon in your browser toolbar and select Create a new script.

Erase any placeholder code inside the editor box completely.

Paste the TamperMonkeyScript.txt

Press Ctrl + S inside the Tampermonkey editor to install the script.

*Phase 4*:If You want the downloader.py script to run automatically on startup in background, do this step:

Press Win + R on your keyboard to open the Windows Run dialog box.

Type shell:startup and hit Enter. This opens your personal Windows Startup folder.

Right-click an empty space inside this folder, select New -> Text Document, and name it exactly:
youtube_server.vbs
(Make sure the file extension actually changes from .txt to .vbs).

Right-click your new youtube_server.vbs file, select Edit (or open with Notepad), paste the script below, and save it:

*Phase 5*: Verification & Usage Loop
Head to YouTube inside Chrome or Brave and reload the tab entirely via Ctrl + F5.

Find any video thumbnail on the home screen, or open a video player watch page.

Hold down the Ctrl key on your keyboard and Right-Click the video asset.

What happens:

A clean dashboard card appears in the bottom right corner showing "🔍 Fetching Formats...".

The Tkinter resolution box opens on your screen containing the exact, true video resolutions found for that specific video clip (e.g., 2160p (4K), 1440p, 1080p).

Pick your format and hit Start Download. The progress bar switches to red and tracks data transfers live.

Clicking ✕ on the card kills the download process immediately, prints an active cancellation indicator, and safely pulls the overlay away from your screen.
