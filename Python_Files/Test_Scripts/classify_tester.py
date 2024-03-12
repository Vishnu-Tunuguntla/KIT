from ultralytics import YOLO
import cv2

# Load the YOLOv8n model
model = YOLO('best.pt')
path = r"C:\Users\15715\Desktop\KITProj\KIT\KitTools\images\human.jpg"



def draw_image(img_path):
    img = cv2.imread(img_path)
    # Run YOLOv8 inference on the frame
    results = model(img)

    # Visualize the results on the frame
    annotated_frame = results[0].plot()

    # Display the annotated frame
    cv2.imshow("YOLOv8 Inference", annotated_frame)
    cv2.waitKey(0)
    # Release the video capture object and close the display window
    cv2.destroyAllWindows()


def draw_video(v_path):
    cap = cv2.VideoCapture(v_path)

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


if path.endswith('.jpg') or path.endswith('.png') or path.endswith('.jpeg'):
    draw_image(path)
elif path.endswith('.mp4') or path.endswith('.avi'):
    draw_video(path)
