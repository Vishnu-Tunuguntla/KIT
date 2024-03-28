import json
import requests
from PIL import Image
from pyzbar.pyzbar import decode

# Nutritionix API credentials
NUTRITIONIX_APP_ID = '6fb84a4e'
NUTRITIONIX_API_KEY = '11093b460290065d73e39e543480dd4d'

# Function to detect barcode in an image and decode it
def detect_barcode(image_path):
    image = Image.open(image_path)
    barcodes = decode(image)
    if barcodes:
        # For debugging: print the detected barcode
        print(f"Detected Barcode: {barcodes[0].data.decode('utf-8')}")
        return barcodes[0].data.decode('utf-8')
    else:
        # If no barcodes are found, log this for debugging purposes
        print("No barcode detected.")
        return None

# Function to search Nutritionix by barcode
def search_by_barcode(barcode):
    url = f"https://trackapi.nutritionix.com/v2/search/item?upc={barcode}"
    headers = {
        'x-app-id': NUTRITIONIX_APP_ID,
        'x-app-key': NUTRITIONIX_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        # Log the failed API call for debugging
        print(f"Failed to fetch nutritional information for barcode {barcode}. Status Code: {response.status_code}")
        return None

# Function to extract and save required nutritional information
def save_nutritional_info(output_file, info):
    # Check if the response contains the expected data before attempting to save
    if info and 'foods' in info and len(info['foods']) > 0:
        food_info = info['foods'][0]
        data_to_save = {
            'brand_name': food_info.get('brand_name', 'N/A'),
            'type_of_food': food_info.get('food_name', 'N/A'),
            'nutritional_facts': {
                'calories': food_info.get('nf_calories', 'N/A'),
                'total_fat': food_info.get('nf_total_fat', 'N/A'),
                'ingredients': food_info.get('nf_ingredient_statement','N/A')
                # Include any additional nutritional facts here
            }
        }
        with open(output_file, 'w') as file:
            json.dump(data_to_save, file, indent=4)
        print(f"Nutritional information saved to {output_file}")
    else:
        print("No nutritional information found to save.")

# Main script execution
print("ran")
image_path = '/Users/havishrallabandi/K.I.T/Images/RiceKrispy.jpeg'
json_output_file = 'nutritional_info.json'

barcode = detect_barcode(image_path)
if barcode:
    nutritional_info = search_by_barcode(barcode)
    if nutritional_info:
        save_nutritional_info(json_output_file, nutritional_info)
    else:
        print("Nutritional information could not be retrieved.")
else:
    print("Barcode detection failed or no barcode found.")