from flask import Flask, request, jsonify
from flask_cors import CORS
import process
import os

app = Flask(__name__)
frontend_host = os.environ.get('FRONTEND_HOST') 
CORS(app, resources={r"/api/*": {"origins": [frontend_host]}}) # Allow all origins to access the API, change to frontend_host when deploying

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

@app.route('/api/food-items', methods=['GET'])
def get_food_items():
    try:
        food_items = process.get_food_items()
        return jsonify(food_items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/food-items/<int:item_id>', methods=['PUT'])
def update_food_item(item_id):
    try:
        data = request.get_json()
        process.update_food_item(item_id, data)
        return jsonify({'message': 'Food item updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gpt-request', methods=['POST'])
def handle_gpt_request():
    try:
        user_request = request.json['request']
        
        # Retrieve food item names and brands from the database
        food_items = process.get_food_item_names_and_brands()
        
        # Answer the request based on the food item names and brands
        answer = process.answer_request(food_items, user_request)
        
        return jsonify({'answer': answer})
    except Exception as e:
        print(f"Error in handle_gpt_request: {e}")
        return jsonify({'error': str(e)}), 500
@app.route('/api/recipe-request', methods=['POST'])
def handle_recipe_request():
    print("Recipe request received")  # Debug print
    try:
        ingredients = request.json['items']
        print("Ingredients:", ingredients)  # Debug print
        recipe = process.get_recipe_from_ingredients(ingredients)
        return jsonify({'recipe': recipe})
    except Exception as e:
        print(f"Error in handle_recipe_request: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
