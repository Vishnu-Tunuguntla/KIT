from flask import Flask, request, jsonify
from flask_cors import CORS
import process

app = Flask(__name__)
CORS(app)

@app.route('/api/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file found'}), 400

    video_file = request.files['video']

    try:
        process.execute_insert_video(video_file, "DesktopPC")
        return jsonify({'message': 'Video uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/query-all-videos', methods=['GET'])
def query_all_videos():
    videos = process.query_all_videos()
    if not videos:
        return jsonify([])
    return jsonify(videos)

@app.route('/api/query-unprocessed-videos', methods=['GET'])
def query_unprocessed_videos():
    videos = process.query_unprocessed_videos()
    if not videos:
        return jsonify([])
    return jsonify(videos)

@app.route('/api/query-processed-videos', methods=['GET'])
def query_processed_videos():
    videos = process.query_processed_videos()
    if not videos:
        return jsonify([])
    return jsonify(videos)

@app.route('/api/query-frames', methods=['GET'])
def query_frames():
    frames = process.query_frames()
    if not frames:
        return jsonify([])
    return jsonify(frames)

@app.route('/api/delete-all-videos', methods=['DELETE'])
def delete_all_videos():
    process.delete_all_videos()
    return jsonify({'message': 'All videos deleted successfully'}), 200

@app.route('/api/delete-all-frames', methods=['DELETE'])
def delete_all_frames():
    process.delete_all_frames()
    return jsonify({'message': 'All frames deleted successfully'}), 200

@app.route('/api/delete-all-data', methods=['DELETE'])
def delete_all_data():
    process.delete_all_data()
    return jsonify({'message': 'All data deleted successfully'}), 200

@app.route('/api/execute', methods=['POST'])
def execute_extraction_and_analysis():
    try:
        process.execute_process()
        return jsonify({'message': 'Extraction and analysis executed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()