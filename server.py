
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/api/search', methods=['GET'])
def search_tracks():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch5',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            results = []
            for entry in info.get('entries', []):
                results.append({
                    'id': entry.get('id'),
                    'title': entry.get('title'),
                    'artist': entry.get('uploader', 'Unknown Artist'),
                    'duration': entry.get('duration'),
                    'thumbnail': entry.get('thumbnail')
                })
            return jsonify({'tracks': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stream', methods=['GET'])
def stream_track():
    track_id = request.args.get('id')
    if not track_id:
        return jsonify({'error': 'No track ID provided'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={track_id}", download=False)
            return jsonify({
                'stream_url': info.get('url'),
                'title': info.get('title'),
                'artist': info.get('uploader')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__mai
