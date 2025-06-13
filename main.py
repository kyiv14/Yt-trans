from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)
CORS(app)

@app.route("/api/transcript", methods=["POST"])
def get_transcript():
    data = request.get_json()
    video_url = data.get("url")

    try:
        video_id = video_url.split("v=")[-1].split("&")[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry["text"] for entry in transcript])
        return jsonify({"text": full_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/", methods=["GET"])
def index():
    return "YouTube Transcript API is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)