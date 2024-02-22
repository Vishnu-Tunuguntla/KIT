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

# Inference loop
while True:
    success, frame = cap.read()  # Read a frame from the camera
    if not success:
        print("Could not read frame from camera")  # Error handling
        break

    results = model(frame, stream=True)  # Run inference on the frame

    for result in results:
        boxes = result.boxes
        probs = result.probs

    # You can now visualize or process 'boxes' and 'probs'
    # ... add your visualization/processing code here

cap.release()  # Release the camera resource 