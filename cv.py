from ultralytics import YOLO
import cv2  # Import OpenCV

#Before running follow steps for Virtual Envrionment
#python3 -m venv myenv
#source myenv/bin/activate
#pip install -r requirements.txt
#deactivate when done

# Load the YOLOv8n model
model = YOLO('yolov8n.pt')

camera_device_number = 0

# Open the USB camera
cap = cv2.VideoCapture(camera_device_number)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()