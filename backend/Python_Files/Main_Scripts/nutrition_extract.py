from google.cloud import vision
from google.oauth2 import service_account
from openai import OpenAI
import os

# OpenAI API key
api_key = os.getenv("GPT_API_KEY")
client = OpenAI(api_key=api_key)

def extract_text_from_image(image_path):
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if len(texts) > 0:
        return texts[0].description.strip()
    else:
        return ""
    
def extract_brand_and_food_item(input_string):
    try:
        # Construct the prompt to ask GPT to identify the brand and food item from the input string
        prompt = f"Identify the brand name and food item described in the following input: {input_string}. Response Format: Brand: [brand_name], Food Item: [food_item]. If no brand is mentioned, use 'No brand'. If no food item is mentioned, use 'No food item'."

        # Call the OpenAI API with the constructed prompt
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in analyzing product descriptions and identifying brand names and food items."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="gpt-3.5-turbo",
        )

        # Extract and return the response from GPT
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print(f"Error in extract_brand_and_food_item: {e}")
        raise e

# Example usage
image_path = r"C:\Users\15715\Downloads\extracted_images_groceries_frame_208.jpg"
extracted_text = extract_text_from_image(image_path)
brand_and_food_item = extract_brand_and_food_item(extracted_text)
print(brand_and_food_item)