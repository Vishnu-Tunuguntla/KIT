import os
import psycopg2
import boto3
from datetime import datetime

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

# Uploads video to S3. Temporary method until Rasberry Pi is set up to upload videos to S3.
def upload_video_to_s3(file_path):
    """
    Uploads a video file to S3 and returns the key.
    
    Args:
    - file_path: Local path to the video file.
    
    Returns:
    The S3 key of the uploaded video.
    """
    video_key = f"videos/{datetime.now().strftime('%Y-%m-%d')}/{file_path.split('/')[-1]}"
    s3.upload_file(file_path, bucket_name, video_key)
    return video_key


# Retrieves all unprocessed videos from the database for later frame extraction and analysis.
def query_all_videos():
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

    

# file_path = r"C:\Users\15715\Desktop\KitTools\Videos\foods2.mp4"
# s3_key = upload_video_to_s3(file_path)
# insert_video_metadata(db_conn_params, "DesktopPC", s3_key, datetime.now(), True)
# print(download_video_from_s3(s3_key))
print(query_all_videos())