from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image
import os



model_name = "openai/clip-vit-base-patch32"
processor = CLIPProcessor.from_pretrained(model_name)
model = CLIPModel.from_pretrained(model_name)

folder_path = "/Users/havishrallabandi/K.I.T/Images"

image_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(".jpeg") or filename.endswith(".jpg")]

print(image_paths)
preprocessed_images = [processor(images=Image.open(image_path), return_tensors="pt") for image_path in image_paths]

label_path = "/Users/havishrallabandi/K.I.T/labels.txt"

label_list = []

with open(label_path,'r') as file:
    for line in file:
        label_list.append(line.strip())

text_inputs = processor(text=label_list, padding=True, return_tensors="pt")

print(label_list)

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

    # Get the top 3 labels and their confidence scores
    top_scores, top_indices = similarities.topk(3, dim=0)
    
    top_labels = [label_list[idx] for idx in top_indices]
    top_confidences = top_scores.tolist()
    
    counter += 1
    print(f"Top 3 classes for Image {counter}: {list(zip(top_labels, top_confidences))}")
