import os
import json
import psycopg2
from openai import OpenAI

# PostgreSQL connection parameters
db_conn_params = {
    'dbname': 'postgres',
    'user': 'KIT_ADMIN',
    'password': 'hvz0rfb4BGQ_uqg3wfg',
    'host': 'kit-db.c9gssgcyk1lb.us-east-1.rds.amazonaws.com',
    'port': '5432'
}

# OpenAI API key
api_key = os.getenv("GPT_API_KEY")
client = OpenAI(api_key=api_key)

# Function to retrieve all food item names and brands from the database
def get_food_item_names_and_brands():
    try:
        conn = psycopg2.connect(**db_conn_params)
        cur = conn.cursor()

        # Construct the SQL query to retrieve food item names and brands
        query = "SELECT Details->>'name', Details->>'brand' FROM FoodItem"
        cur.execute(query)

        # Fetch all the food item names and brands
        food_items = cur.fetchall()

        cur.close()
        conn.close()

        return food_items
    except (psycopg2.Error, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return []

# Function to answer the user request based on food item names and brands
def answer_request(food_items, request):
    try:
        food_item_names_and_brands = [f"{item[0]} ({item[1]})" for item in food_items]
        food_item_names_and_brands_str = ', '.join(food_item_names_and_brands)

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant that answers requests based on the provided food item names and brands."
                },
                {
                    "role": "user",
                    "content": f"Food items: {food_item_names_and_brands_str}\nRequest: {request}"
                }
            ],
            model="gpt-3.5-turbo",
        )

        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print(f"Error in answer_request: {e}")
        raise e

if __name__ == "__main__":
    try:
        # Retrieve food item names and brands from the database
        food_items = get_food_item_names_and_brands()

        if food_items:
            # Get the user request
            request = input("Enter your request: ")

            # Answer the request based on the food item names and brands
            answer = answer_request(food_items, request)
            print(answer)
        else:
            print("No food items found in the database.")
    except Exception as e:
        print(f"Error in main script: {e}")