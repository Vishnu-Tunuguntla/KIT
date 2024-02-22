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
    success, frame = cap.read()  
    if not success:
        print("Could not read frame from camera")  
        break

    results = model(frame, stream=True)  

    for result in results:
        boxes = result.boxes
        probs = result.probs

        # Draw bounding boxes and labels on the frame
        for box, prob in zip(boxes.xyxy, probs): 
            x1, y1, x2, y2 = map(int, box)
            label = f'{result.names[int(box.cls)]}: {prob:.2f}'  # Class label and probability
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('YOLOv8 Live Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release() 
cv2.destroyAllWindows() 