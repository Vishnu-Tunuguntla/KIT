import base64
import requests
import json
import os

# OpenAI API key
api_key = os.getenv("GPT_API_KEY")

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Cleans String for JSON Format
def extract_json(input_string):
    # Find the positions of the first "{" and the last "}"
    first_brace_index = input_string.find("{")
    last_brace_index = input_string.rfind("}")

    if first_brace_index != -1 and last_brace_index != -1:
        # Extract the JSON data between the first "{" and the last "}"
        json_string = input_string[first_brace_index:last_brace_index + 1]

        return json_string
    else:
        print("No valid JSON data found in the input string.")
        return None

def llm_classify(image_path):
    # Encoded Image
    image_data = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Examine the image to determine if it features a grocery item. Output should be in JSON format. If the item is not a grocery item, the JSON should state: {\"food_type\": \"not a grocery item\"}. If the item is a produce, the JSON should include: {\"food_type\": \"produce\", \"name\": \"<item name>\", \"nutrition_info\": {<nutrition details>}, \"approximate_expiration_time\": \"<approximated expiration time after purchase>\"}. If the item is packaged, the JSON should include: {\"food_type\": \"packaged\", \"product_name\": \"<extracted text>\", \"details\": {<extracted product details>}}."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        response_text = response.json()["choices"][0]["message"]["content"]

        # Remove extra characters from the response text
        response_text = response_text.strip("```json\n")

        # Parse the response text as JSON
        item_data = json.loads(extract_json(response_text))

        # Create the "json_files" folder if it doesn't exist
        os.makedirs("json_files", exist_ok=True)

        # Generate a unique filename based on the image path
        filename = os.path.splitext(os.path.basename(image_path))[0] + ".json"

        # Save the item data to a JSON file
        with open(os.path.join("json_files", filename), "w") as json_file:
            json.dump(item_data, json_file, indent=4)

        print(f"JSON file generated and saved to json_files/{filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making the API request: {e}")
    except (KeyError, IndexError) as e:
        print(f"Error occurred while parsing the API response: {e}")
    except json.JSONDecodeError as e:
        print(f"Error occurred while parsing the response as JSON: {e}")
        print(f"Response text: {response_text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
llm_classify("AppleImage.jpeg")

