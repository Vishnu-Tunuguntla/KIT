import os
import psycopg2
import boto3
from datetime import datetime
import cv2
from ultralytics import YOLO
import numpy as np
import imagehash
from PIL import Image
import os
from gpt_classify import llm_classify
import shutil
import base64

# PostgresSQL Connection Paramaters
db_conn_params = {
    'dbname': 'postgres',
    'user': 'KIT_ADMIN',
    'password': 'hvz0rfb4BGQ_uqg3wfg',
    'host': 'kit-db.c9gssgcyk1lb.us-east-1.rds.amazonaws.com',
    'port': '5432'
}

# S3 Storage Setup. Temporary method until EC2 and Rasberry Pi are setup. 
s3 = boto3.client(
    's3',
    aws_access_key_id='AKIAR7BWENTMUARBZ6T3',
    aws_secret_access_key='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'
)
bucket_name = 'kitbucketaws'

# Downloads a video file from S3 and returns the file path.
def download_video_from_s3(s3_key):
    """
    Downloads a video file from S3 and returns the file path.
    
    Args:
    - s3_key: The S3 key of the video file.
    
    Returns:
    The local file path of the downloaded video.
    """
    sanitized_filename = s3_key.replace("\\", "_").replace("/", "_").replace(":", "_")
    file_path = f"S3Downloads/{sanitized_filename}"

    # Ensure the downloads directory exists
    if not os.path.exists("S3Downloads"):
        os.makedirs("S3Downloads")

    s3.download_file(bucket_name, s3_key, file_path)
    return file_path

# Uploads video to S3. Uses File
def upload_video_to_s3(file):
    """
    Uploads a video file to S3 and returns the key.
    
    Args:
    - file_path: Local path to the video file.
    
    Returns:
    The S3 key of the uploaded video.
    """
    video_key = f"videos/{datetime.now().strftime('%Y-%m-%d')}/{file.filename}"
    s3.upload_fileobj(file, bucket_name, video_key)
    return video_key


# Retrieves all unprocessed videos from the database for later frame extraction and analysis.
def query_all_videos_og():
    """
    Retrieves all unprocessed videos from the database.
    
    Returns:
    A list of dictionaries, where each dictionary contains the video metadata.
    """
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_conn_params)

    # Create a cursor object
    cur = conn.cursor()

    # Execute the query
    cur.execute("SELECT * FROM videos WHERE Processed = FALSE")

    # Fetch all the rows
    rows = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Return the rows
    return rows

# Inserts videos and their addresses from AWS S3 bucket into the database. Temporary method for testing purposes. Will need to be replaced with a method - using the AWS API - that can be called from the Rasberry Pi.
def insert_video_metadata(db_conn_params, device_id, s3_key, timestamp, motion_detected):
    """
    Inserts video metadata into the PostgreSQL database.
    
    Args:
    - db_conn_params: Dictionary containing database connection parameters.
    - device_id: Identifier for the device that captured the video.
    - s3_key: The S3 key where the video is stored.
    - timestamp: The timestamp when the video was captured.
    - motion_detected: Boolean indicating if motion was detected.
    """
    # SQL to insert video metadata
    insert_query = """
    INSERT INTO Videos (DeviceID, Timestamp, Path, MotionDetected, Processed)
    VALUES (%s, %s, %s, %s, FALSE)
    RETURNING VideoID;
    """
    
    with psycopg2.connect(**db_conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute(insert_query, (device_id, timestamp, s3_key, motion_detected))
            video_id = cur.fetchone()[0]
            print(f"Video metadata inserted successfully with VideoID: {video_id}")

# Extracts the S3 keys from a list of video dictionaries.
def extract_s3_keys(video_list):
    """
    Extracts the S3 keys from a list of video dictionaries.

    Args:
    - video_list: A list of dictionaries representing video metadata.

    Returns:
    A list of S3 keys.
    """
    s3_keys = [video[3] for video in video_list]
    return s3_keys

# Updates the videos as processed in the database.
def update_videos_as_processed(videos):
    """
    Updates the videos as processed in the database.
    
    Args:
    - videos: A list of video dictionaries.
    """
    # SQL to update videos as processed
    update_query = "UPDATE Videos SET Processed = TRUE WHERE VideoID = %s"

    with psycopg2.connect(**db_conn_params) as conn:
        with conn.cursor() as cur:
            for video in videos:
                video_id = video[0]
                cur.execute(update_query, (video_id,))

# Extracts frames using a video path and accounts for duplicates using hash comparison and blur using variance of Laplacian.
def extract_frames_from_video(video_path):
    # Load the custom YOLO model
    model = YOLO('backend/Python_Files/Main_Scripts/best.pt')

    # Set the confidence threshold for object detection, higher values mean less false positives
    confidence_threshold = 0.85

    # Set the blur threshold, higher values mean less blurry images
    blur_threshold = 80

    # Set the hash size for image comparison
    hash_size = 8

    # Set the hash threshold for image comparison, higher makes duplication detection more strict
    hash_threshold = 25

    # Set the output folder for extracted images
    output_folder = "extracted_images"

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initialize a list to store the detected objects
    detected_objects = []

    # Initialize a list to store the paths of the extracted images
    extracted_images = []

    # Initialize a dictionary to store the hashes of extracted images
    image_hashes = {}

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get the video frame rate and total number of frames
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Initialize the frame counter
    frame_count = 0

    # Initialize a list to store the extracted frame information
    extracted_frames = []

    # Iterate through the video frames
    while cap.isOpened():
        # Read a frame from the video
        ret, frame = cap.read()

        # Break the loop if no more frames are available
        if not ret:
            break

        # Increment the frame counter
        frame_count += 1

        # Run object detection on the frame
        results = model(frame)

        # Check if there are any detected objects
        if len(results) > 0:
            # Iterate through the detected objects
            for result in results:
                # Check if the object has a valid class label and confidence score
                if len(result.boxes.cls) > 0 and len(result.boxes.conf) > 0:
                    # Get the class label and confidence score
                    class_label = result.boxes.cls[0].item()
                    confidence_score = result.boxes.conf[0].item()

                    # Check if the object is classified as "groceries" and has a confidence score above the threshold
                    if class_label == 0 and confidence_score >= confidence_threshold:
                        # Get the bounding box coordinates
                        x1, y1, x2, y2 = result.boxes.xyxy[0].tolist()

                        # Extract the object frame
                        object_frame = frame[int(y1):int(y2), int(x1):int(x2)]

                        # Calculate the blur metric (variance of Laplacian)
                        gray = cv2.cvtColor(object_frame, cv2.COLOR_BGR2GRAY)
                        blur_metric = cv2.Laplacian(gray, cv2.CV_64F).var()

                        # Check if the object frame is not blurry
                        if blur_metric >= blur_threshold:
                            # Convert the object frame to PIL Image
                            pil_image = Image.fromarray(cv2.cvtColor(object_frame, cv2.COLOR_BGR2RGB))

                            # Calculate the hash of the object frame
                            frame_hash = imagehash.dhash(pil_image, hash_size=hash_size)

                            # Check if the hash already exists in the dictionary
                            is_duplicate = False
                            for stored_hash in image_hashes.values():
                                if stored_hash - frame_hash <= hash_threshold:
                                    is_duplicate = True
                                    break

                            # If the object frame is not a duplicate, save it and add its information to the list
                            if not is_duplicate:
                                # Generate the image file path
                                image_path = os.path.join(output_folder, f'groceries_frame_{frame_count}.jpg')

                                # Save the extracted object frame as an image
                                cv2.imwrite(image_path, object_frame)

                                # Calculate the timestamp based on frame count and FPS
                                timestamp = frame_count / fps

                                # Add the frame information to the list of extracted frames
                                frame_info = {
                                    'video_path': video_path,
                                    'frame_path': image_path,
                                    'timestamp': timestamp,
                                    'detected_objects': [x1, y1, x2, y2]
                                }
                                extracted_frames.append(frame_info)

                                # Add the hash of the object frame to the dictionary
                                image_hashes[image_path] = frame_hash

        # Print the progress
        print(f'Processed frame {frame_count}/{total_frames}')

    # Release the video capture object and close any open windows
    cap.release()
    cv2.destroyAllWindows()

    return extracted_frames

def insert_frames_into_database(video_id, frames):
    """
    Inserts the extracted frames into the database.
    
    Args:
    - video_id: The ID of the video.
    - frames: A list of dictionaries containing the frame information.
    """
    # SQL to insert frames
    insert_query = """
    INSERT INTO Frames (VideoID, Timestamp, Path, Processed)
    VALUES (%s, to_timestamp(%s), %s, FALSE)
    """

    with psycopg2.connect(**db_conn_params) as conn:
        with conn.cursor() as cur:
            for frame in frames:
                timestamp = frame['timestamp']
                frame_path = frame['frame_path']
                s3_key = f"frames/{frame_path.split('/')[-1]}"
                cur.execute(insert_query, (video_id, timestamp, s3_key))

def upload_frames_to_s3(frames):
    """
    Uploads the extracted frames to S3.
    
    Args:
    - frames: A list of dictionaries containing the frame information.
    """
    for frame in frames:
        frame_path = frame['frame_path']
        s3_key = f"frames/{frame_path.split('/')[-1]}"
        s3.upload_file(frame_path, bucket_name, s3_key)

def query_unprocessed_frames():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_conn_params)

    # Create a cursor object
    cur = conn.cursor()

    # Execute the query to retrieve unprocessed frames
    cur.execute("SELECT * FROM frames WHERE processed = false")

    # Fetch all the rows
    rows = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    return rows

def update_frame_as_processed(frame_id):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_conn_params)

    # Create a cursor object
    cur = conn.cursor()

    # Execute the query to update the frame as processed
    cur.execute("UPDATE frames SET processed = true WHERE frameid = %s", (frame_id,))

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

def download_frame_from_s3(s3_key):
    """
    Downloads a frame from S3 and returns the local file path.
    
    Args:
    - s3_key: The S3 key of the frame.
    
    Returns:
    The local file path of the downloaded frame.
    """
    sanitized_filename = s3_key.replace("\\", "_").replace("/", "_").replace(":", "_")
    local_frame_path = f"S3Downloads/{sanitized_filename}"

    # Ensure the downloads directory exists
    if not os.path.exists("S3Downloads"):
        os.makedirs("S3Downloads")

    s3.download_file(bucket_name, s3_key, local_frame_path)
    return local_frame_path

# Extracts frames from a video file using the YOLOv8 object detection model.
def process_unprocessed_videos():
    """
    Processes unprocessed videos, extracts frames, and inserts them into the database.
    """
    # Query all unprocessed videos from the database
    unprocessed_videos = query_all_videos_og()

    # Update the videos as processed in the database
    update_videos_as_processed(unprocessed_videos)

    # Process each unprocessed video
    for video in unprocessed_videos:
        video_id = video[0]
        s3_key = video[3]

        # Download the video from S3
        video_path = download_video_from_s3(s3_key)

        # Extract frames from the video using the logic from frame_extract_advanced.py
        extracted_frames = extract_frames_from_video(video_path)

        # Insert the extracted frames into the database
        insert_frames_into_database(video_id, extracted_frames)

        # Upload the extracted frames to S3
        upload_frames_to_s3(extracted_frames)

def process_unprocessed_frames():
    # Query all unprocessed frames from the database
    unprocessed_frames = query_unprocessed_frames()

    # Process each unprocessed frame
    for frame in unprocessed_frames:
        frame_id = frame[0]
        frame_path = frame[3]

        try:
            # Download the frame from S3
            local_frame_path = download_frame_from_s3(frame_path)

            # Classify the frame using the llm_classify function
            llm_classify(local_frame_path)

            # Update the frame as processed in the database
            update_frame_as_processed(frame_id)

        except Exception as e:
            print(f"Error occurred while processing frame {frame_id}: {e}")
def query_all_videos():
    conn = psycopg2.connect(**db_conn_params)
    cur = conn.cursor()
    cur.execute("SELECT * FROM videos")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [f"https://{bucket_name}.s3.amazonaws.com/{row[3]}" for row in rows]

def query_unprocessed_videos():
    conn = psycopg2.connect(**db_conn_params)
    cur = conn.cursor()
    cur.execute("SELECT * FROM videos WHERE processed = false")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [f"https://{bucket_name}.s3.amazonaws.com/{row[3]}" for row in rows]

def query_processed_videos():
    conn = psycopg2.connect(**db_conn_params)
    cur = conn.cursor()
    cur.execute("SELECT * FROM videos WHERE processed = true")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [f"https://{bucket_name}.s3.amazonaws.com/{row[3]}" for row in rows]

def query_frames():
    conn = psycopg2.connect(**db_conn_params)
    cur = conn.cursor()
    cur.execute("SELECT * FROM frames")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    frame_data = []
    for row in rows:
        s3_key = row[3]
        local_frame_path = download_frame_from_s3(s3_key)
        with open(local_frame_path, 'rb') as file:
            image_data = file.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            frame_data.append(f"data:image/jpeg;base64,{base64_data}")

    return frame_data
def delete_all_videos():
    conn = psycopg2.connect(**db_conn_params)
    cur = conn.cursor()
    cur.execute("DELETE FROM videos")
    conn.commit()
    cur.close()
    conn.close()

def delete_all_frames():
    conn = psycopg2.connect(**db_conn_params)
    cur = conn.cursor()
    cur.execute("DELETE FROM frames")
    conn.commit()
    cur.close()
    conn.close()

def delete_all_data():
    conn = psycopg2.connect(**db_conn_params)
    cur = conn.cursor()
    cur.execute("DELETE FROM NutritionalFacts")
    cur.execute("DELETE FROM ObjectDetails")
    cur.execute("DELETE FROM AnalysisResults")
    cur.execute("DELETE FROM Frames")
    cur.execute("DELETE FROM Videos")
    conn.commit()
    cur.close()
    conn.close()
    if os.path.exists("extracted_images"):
        shutil.rmtree("extracted_images")
    if os.path.exists("json_files"):
        shutil.rmtree("json_files")
    if os.path.exists("S3Downloads"):
        shutil.rmtree("S3Downloads")
            
def execute_insert_video(file, location):
    s3_key = upload_video_to_s3(file)
    insert_video_metadata(db_conn_params, location, s3_key, datetime.now(), True)

def execute_process():
    process_unprocessed_videos()
    process_unprocessed_frames()


