import psycopg2
# PostgresSQL Connection Paramaters
db_conn_params = {
    'dbname': 'postgres',
    'user': 'KIT_ADMIN',
    'password': 'hvz0rfb4BGQ_uqg3wfg',
    'host': 'kit-db.c9gssgcyk1lb.us-east-1.rds.amazonaws.com',
    'port': '5432'
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_conn_params)

# Create a cursor object
cur = conn.cursor()

# Execute the query
cur.execute("SELECT * FROM videos")

# Fetch all the rows
rows = cur.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the cursor and connection
cur.close()
conn.close()