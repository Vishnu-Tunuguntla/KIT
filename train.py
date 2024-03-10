from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n-cls.pt')  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data='C:/Users/15715/Desktop/KITProj/KIT/data.yaml', epochs=100, imgsz=832)