from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image
import os



model_name = "openai/clip-vit-base-patch32"
processor = CLIPProcessor.from_pretrained(model_name)
model = CLIPModel.from_pretrained(model_name)

folder_path = "/Users/havishrallabandi/K.I.T/Images"

image_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(".jpeg") or filename.endswith(".jpg")]
print (image_paths)

preprocessed_images = [processor(images=Image.open(image_path), return_tensors="pt") for image_path in image_paths]

texts = ["apple","banana","orange","grape","peach","blueberry","bread","ramen","cereal box"] 
text_inputs = processor(text=texts, padding=True, return_tensors="pt")

counter = 0
for preprocessed_image in preprocessed_images:
    # Get the image tensor
    image_inputs = preprocessed_image["pixel_values"]
    
    # Use the model to generate embeddings
    with torch.no_grad():
        image_features = model.get_image_features(**preprocessed_image)
        text_features = model.get_text_features(**text_inputs)

    # Calculate similarities
    similarities = (text_features @ image_features.T).softmax(dim=0)

    # Find the best class for each image
    best_class = texts[similarities.argmax()]
    counter += 1
    print(f"Best class for Image {counter}: {best_class}")

