import cv2
from ultralytics import YOLO
import numpy as np
import imagehash
from PIL import Image
import os

# Load the custom YOLO model
model = YOLO('best.pt')

# Set the video file path
video_path = "/Users/vishtun/Downloads/test_home.mp4"

# Set the confidence threshold for object detection, higher values mean less false positives
confidence_threshold = 0.85

# Set the blur threshold, higher values mean less blurry images
blur_threshold = 100

# Set the hash size for image comparison
hash_size = 8

# Set the hash threshold for image comparison, lower makes duplication detection more strict
hash_threshold = 20

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
                            if stored_hash - frame_hash <= hash_threshold:  # Adjust the threshold as needed
                                is_duplicate = True
                                break

                        # If the object frame is not a duplicate, save it and add its hash to the dictionary
                        if not is_duplicate:
                            # Generate the image file path
                            image_path = os.path.join(output_folder, f'groceries_frame_{frame_count}.jpg')

                            # Save the extracted object frame as an image
                            cv2.imwrite(image_path, object_frame)

                            # Add the image path to the list of extracted images
                            extracted_images.append(image_path)

                            # Add the object's bounding box coordinates to the list of detected objects
                            detected_objects.append([x1, y1, x2, y2])

                            # Add the hash of the object frame to the dictionary
                            image_hashes[image_path] = frame_hash

    # Print the progress
    print(f'Processed frame {frame_count}/{total_frames}')

# Release the video capture object and close any open windows
cap.release()
cv2.destroyAllWindows()

# Display the extracted images
for image_path in extracted_images:
    # Read the image
    image = cv2.imread(image_path)

    # Display the image
    cv2.imshow('Extracted Image', image)
    cv2.waitKey(0)

# Close all the displayed windows
cv2.destroyAllWindows()