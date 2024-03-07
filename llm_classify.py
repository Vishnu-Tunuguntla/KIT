import anthropic
import base64

# Set up your Anthropic API key
api_key = "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"
client = anthropic.Client(api_key=api_key)
# Set the path to the image file on your computer
image_path = "/Users/vishtun/Desktop/pProjects/KIT/KIT/extracted_images/groceries_frame_347.jpg"

# Read the image file and encode it in base64
with open(image_path, "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

# Set the media type based on the image file extension
image_media_type = "image/jpeg"  # Assuming the image is in JPEG format

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_media_type,
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Describe this image."
                }
            ],
        }
    ],
)

print(message)