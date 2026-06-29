import yt_dlp
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import tkinter as tk
from tkinter import ttk
import os

app = Flask(__name__)
CORS(app)

DEFAULT_DOWNLOAD_PATH = os.path.join(os.path.expanduser('~'), 'Downloads')
download_tasks = {}

def get_real_video_qualities(video_url):
    ydl_opts = {'quiet': True, 'skip_download': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])
            
            heights = set()
            for f in formats:
                height = f.get('height')
                if f.get('vcodec') != 'none' and height and height >= 144:
                    heights.add(height)
            
            sorted_heights = sorted(list(heights), reverse=True)
            return [f"{h}p" for h in sorted_heights]
    except Exception as e:
        print(f"Metadata scan timeout fallback: {e}")
        return ["1080p", "720p", "480p", "360p"]

def make_progress_hook(video_id):
    def hook(d):
        if download_tasks.get(video_id, {}).get('cancel_requested'):
            raise Exception("USER_CANCELLED")

        info_dict = d.get('info_dict', {})
        real_title = info_dict.get('title')
        if real_title:
            download_tasks[video_id]["title"] = real_title

        if d['status'] == 'downloading':
            speed_bytes = d.get('speed')
            speed = f"{speed_bytes / (1024 * 1024):.1f} MB/s" if speed_bytes else "0.0 MB/s"
            
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            
            if total_bytes > 0:
                percent = int((downloaded / total_bytes) * 100)
                total_size = f"{total_bytes / (1024 * 1024):.1f} MB"
                remaining = f"{(total_bytes - downloaded) / (1024 * 1024):.1f} MB"
            else:
                percent = 0
                total_size = "Unknown"
                remaining = "Unknown"

            download_tasks[video_id].update({
                "status": "downloading",
                "percent": f"{percent}%",
                "speed": speed,
                "remaining": remaining,
                "total": total_size
            })
        elif d['status'] == 'finished':
            download_tasks[video_id].update({
                "status": "merging",
                "percent": "100%",
                "speed": "0.0 MB/s",
                "remaining": "0.0 MB"
            })
    return hook

def run_download_thread(video_url, video_id, quality):
    format_selection = f'bestvideo[height<={quality.replace("p","")}]+bestaudio/best'
    out_template = os.path.join(DEFAULT_DOWNLOAD_PATH, '%(title)s.%(ext)s')

    ydl_opts = {
        'format': format_selection,
        'outtmpl': out_template,
        'progress_hooks': [make_progress_hook(video_id)],
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        if download_tasks[video_id].get('cancel_requested'):
            download_tasks[video_id]["status"] = "cancelled"
        else:
            download_tasks[video_id]["status"] = "completed"
    except Exception as e:
        if "USER_CANCELLED" in str(e) or download_tasks[video_id].get('cancel_requested'):
            download_tasks[video_id]["status"] = "cancelled"
        else:
            download_tasks[video_id]["status"] = "failed"
    finally:
        threading.Timer(10.0, lambda: download_tasks.pop(video_id, None)).start()

def show_dynamic_quality_popup(video_url, video_id):
    download_tasks[video_id]["status"] = "fetching formats..."
    extracted_qualities = get_real_video_qualities(video_url)
    
    if download_tasks.get(video_id, {}).get('cancel_requested'):
        return

    download_tasks[video_id]["status"] = "selecting quality..."

    root = tk.Tk()
    root.title("Select Video Quality")
    root.attributes("-topmost", True)
    
    window_width, window_height = 320, 150
    center_x = int(root.winfo_screenwidth()/2 - window_width/2)
    center_y = int(root.winfo_screenheight()/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    ttk.Label(root, text="Choose an available resolution:", font=("Arial", 11)).pack(pady=12)

    quality_var = tk.StringVar()
    dropdown = ttk.Combobox(root, textvariable=quality_var, values=extracted_qualities, state="readonly", width=20)
    
    if extracted_qualities:
        dropdown.current(0)
    dropdown.pack(pady=5)

    user_choice = {"selected": None}
    def on_submit():
        user_choice["selected"] = quality_var.get()
        root.destroy()

    ttk.Button(root, text="Start Download", command=on_submit).pack(pady=15)
    root.mainloop()

    if user_choice["selected"]:
        choice = user_choice["selected"]
        download_tasks[video_id]["quality"] = choice
        download_tasks[video_id]["status"] = "downloading"
        threading.Thread(target=run_download_thread, args=(video_url, video_id, choice)).start()
    else:
        if video_id in download_tasks:
            download_tasks[video_id]["status"] = "cancelled"
            threading.Timer(5.0, lambda: download_tasks.pop(video_id, None)).start()

@app.route('/download', methods=['POST'])
def trigger_download():
    data = request.json or {}
    url = data.get('url')
    initial_title = data.get('title', 'Fetching Title...')
    
    if not url or 'v=' not in url:
        return jsonify({"status": "Invalid URL"}), 400

    video_id = url.split('v=')[1].split('&')[0]
    download_tasks[video_id] = {
        "title": initial_title,
        "status": "connecting...",
        "percent": "0%",
        "speed": "0.0 MB/s",
        "remaining": "Waiting...",
        "total": "Waiting...",
        "quality": "Pending",
        "cancel_requested": False
    }
    
    threading.Thread(target=show_dynamic_quality_popup, args=(url, video_id)).start()
    return jsonify({"status": "Scan started", "video_id": video_id}), 200

@app.route('/cancel', methods=['POST'])
def cancel_download():
    data = request.json or {}
    video_id = data.get('video_id')
    if video_id in download_tasks:
        download_tasks[video_id]['cancel_requested'] = True
        download_tasks[video_id]['status'] = 'cancelled'
        return jsonify({"status": "Aborted"}), 200
    return jsonify({"status": "Not found"}), 404

@app.route('/progress', methods=['GET'])
def get_progress():
    return jsonify(download_tasks), 200

if __name__ == '__main__':
    if not os.path.exists(DEFAULT_DOWNLOAD_PATH):
        os.makedirs(DEFAULT_DOWNLOAD_PATH)
    app.run(port=5678, threaded=True)
