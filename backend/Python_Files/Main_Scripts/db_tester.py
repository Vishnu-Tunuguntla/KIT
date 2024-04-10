import psycopg2

db_conn_params = {
    'dbname': 'postgres',
    'user': 'KIT_ADMIN',
    'password': 'hvz0rfb4BGQ_uqg3wfg',
    'host': 'kit-db.c9gssgcyk1lb.us-east-1.rds.amazonaws.com',
    'port': '5432'
}

def get_food_item_ids():
    with psycopg2.connect(**db_conn_params) as conn:
        with conn.cursor() as cur:
            # Query to retrieve all food item IDs
            query = "SELECT ItemID FROM FoodItem"
            cur.execute(query)
            
            # Fetch all the food item IDs
            food_item_ids = cur.fetchall()
            
            # Print the food item IDs
            print("Food Item IDs:")
            for item_id in food_item_ids:
                print(item_id[0])

# Call the function to get and print the food item IDs
get_food_item_ids()