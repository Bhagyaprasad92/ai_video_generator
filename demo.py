import os
import time
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    video_name = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        
        api_key = "YOUR_TEXT_TO_VIDEO_API_KEY_HERE"
        api_url = "https://api.your-video-service.com/v1/generate"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=data)
            result = response.json()
            
            task_id = result.get("task_id")
            status_url = f"https://api.your-video-service.com/v1/status/{task_id}"
            
            video_url = None
            while True:
                status_resp = requests.get(status_url, headers=headers).json()
                status = status_resp.get("status")
                if status == "completed":
                    video_url = status_resp.get("video_url")
                    break
                if status == "failed":
                    break
                time.sleep(5)
                
            if video_url:
                vid_resp = requests.get(video_url)
                os.makedirs("static", exist_ok=True)
                video_name = f"video_{task_id}.mp4"
                with open(os.path.join("static", video_name), "wb") as f:
                    f.write(vid_resp.content)
        except Exception:
            pass

    return render_template("index.html", video=video_name)

if __name__ == "__main__":
    app.run(debug=True)