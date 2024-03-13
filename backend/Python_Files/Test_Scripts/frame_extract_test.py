import cv2
from ultralytics import YOLO

# Load the custom YOLO model
model = YOLO('best.pt')

# Set the video file path
video_path = "/Users/vishtun/Downloads/test_home.mp4"

# Set the confidence threshold for object detection
confidence_threshold = 0.85

# Set the overlap threshold for object comparison
overlap_threshold = 0.8

# Initialize a list to store the detected objects
detected_objects = []

# Initialize a list to store the paths of the extracted images
extracted_images = []

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

                # Check if the object is classified as "groceries" and has a semi-high confidence score
                if class_label == 0 and confidence_score >= confidence_threshold:
                    # Get the bounding box coordinates
                    x1, y1, x2, y2 = result.boxes.xyxy[0].tolist()

                    # Check if the object overlaps with any previously detected objects
                    is_duplicate = False
                    for prev_object in detected_objects:
                        prev_x1, prev_y1, prev_x2, prev_y2 = prev_object

                        # Calculate the overlap area
                        overlap_x1 = max(x1, prev_x1)
                        overlap_y1 = max(y1, prev_y1)
                        overlap_x2 = min(x2, prev_x2)
                        overlap_y2 = min(y2, prev_y2)

                        overlap_area = max(0, overlap_x2 - overlap_x1) * max(0, overlap_y2 - overlap_y1)
                        object_area = (x2 - x1) * (y2 - y1)

                        # Check if the overlap ratio exceeds the threshold
                        if overlap_area / object_area >= overlap_threshold:
                            is_duplicate = True
                            break

                    # If the object is not a duplicate, save the frame and add it to the list of detected objects
                    if not is_duplicate:
                        # Extract the object from the frame
                        object_frame = frame[int(y1):int(y2), int(x1):int(x2)]

                        # Generate the image file path
                        image_path = f'groceries_frame_{frame_count}.jpg'

                        # Save the extracted object frame as an image
                        cv2.imwrite(image_path, object_frame)

                        # Add the image path to the list of extracted images
                        extracted_images.append(image_path)

                        # Add the object's bounding box coordinates to the list of detected objects
                        detected_objects.append([x1, y1, x2, y2])

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