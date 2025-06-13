from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re

app = Flask(__name__)
CORS(app)

def extract_video_id(url):
    match = re.search(r'(?:v=|youtu\.be/)([\w-]{11})', url)
    return match.group(1) if match else None

@app.route("/transcript", methods=["POST"])
def transcript():
    data = request.get_json()
    url = data.get("url", "")
    video_id = extract_video_id(url)

    if not video_id:
        return jsonify({"error": "Некорректная ссылка на видео."}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry["text"] for entry in transcript])
        return jsonify({"text": full_text})
    except TranscriptsDisabled:
        return jsonify({"error": "У видео отключены расшифровки."}), 400
    except NoTranscriptFound:
        return jsonify({"error": "Нет доступных расшифровок для видео."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
