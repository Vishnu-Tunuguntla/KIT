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
    
    # Pass the video file to your existing Python method for processing and saving to the database
    try:
        process.execute_insert_video(video_file, "DesktopPC")
        #process.execute_process()
        return jsonify({'message': 'Video uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()