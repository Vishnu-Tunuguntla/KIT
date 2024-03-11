import psycopg2
import tkinter as tk
from tkinter import ttk
import os
import shutil
# PostgresSQL Connection Paramaters
db_conn_params = {
    'dbname': 'postgres',
    'user': 'KIT_ADMIN',
    'password': 'hvz0rfb4BGQ_uqg3wfg',
    'host': 'kit-db.c9gssgcyk1lb.us-east-1.rds.amazonaws.com',
    'port': '5432'
}
# Retrieves all unprocessed videos from the database
def query_all_videos():
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
# Deletes all videos from the tables
def delete_all_videos():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_conn_params)

    # Create a cursor object
    cur = conn.cursor()

    # Execute the query
    cur.execute("DELETE FROM videos")

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

# Queries all videos marked as unprocessed
def query_unprocessed_videos():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_conn_params)
    # Create a cursor object
    cur = conn.cursor()
    # Execute the query
    cur.execute("SELECT * FROM videos WHERE processed = false")
    # Fetch all the rows
    rows = cur.fetchall()
    # Print the rows
    for row in rows:
        print(row)
    # Close the cursor and connection
    cur.close()
    conn.close()
    
 #Queries all videos marked as processed
def query_processed_videos():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_conn_params)
    # Create a cursor object
    cur = conn.cursor()
    # Execute the query
    cur.execute("SELECT * FROM videos WHERE processed = true")
    # Fetch all the rows
    rows = cur.fetchall()
    # Print the rows
    for row in rows:
        print(row)
    # Close the cursor and connection
    cur.close()
    conn.close()

    #Queries all frames from the database
def query_all_frames():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_conn_params)
    # Create a cursor object
    cur = conn.cursor()
    # Execute the query
    cur.execute("SELECT * FROM frames")
    # Fetch all the rows
    rows = cur.fetchall()
    # Print the rows
    for row in rows:
        print(row)
    # Close the cursor and connection
    cur.close()
    conn.close()

    #Queries all unprocessed frames from the database   
def query_unprocessed_frames():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_conn_params)
    # Create a cursor object
    cur = conn.cursor()
    # Execute the query
    cur.execute("SELECT * FROM frames WHERE processed = false")
    # Fetch all the rows
    rows = cur.fetchall()
    # Print the rows
    for row in rows:
        print(row)
    # Close the cursor and connection
    cur.close()
    conn.close()

    #Queries all processed frames from the database
def query_processed_frames():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_conn_params)
    # Create a cursor object
    cur = conn.cursor()
    # Execute the query
    cur.execute("SELECT * FROM frames WHERE processed = true")
    # Fetch all the rows
    rows = cur.fetchall()
    # Print the rows
    for row in rows:
        print(row)
    # Close the cursor and connection
    cur.close()
    conn.close()
def delete_all_frames():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_conn_params)

    # Create a cursor object
    cur = conn.cursor()

    # Execute the query
    cur.execute("DELETE FROM frames")

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

def delete_all_data():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_conn_params)

    # Create a cursor object
    cur = conn.cursor()

    # Execute the queries to delete data from all tables
    cur.execute("DELETE FROM NutritionalFacts")
    cur.execute("DELETE FROM ObjectDetails")
    cur.execute("DELETE FROM AnalysisResults")
    cur.execute("DELETE FROM Frames")
    cur.execute("DELETE FROM Videos")

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Delete the contents of the 'extracted_images' and 'json_files' folders
    if os.path.exists("extracted_images"):
        shutil.rmtree("extracted_images")
    if os.path.exists("json_files"):
        shutil.rmtree("json_files")

def create_ui():
    window = tk.Tk()
    window.title("Database Management")

    # Create buttons for query functions
    button_query_all_videos = ttk.Button(window, text="Query All Videos", command=query_all_videos)
    button_query_all_videos.pack(pady=5)

    button_query_unprocessed_videos = ttk.Button(window, text="Query Unprocessed Videos", command=query_unprocessed_videos)
    button_query_unprocessed_videos.pack(pady=5)

    button_query_processed_videos = ttk.Button(window, text="Query Processed Videos", command=query_processed_videos)
    button_query_processed_videos.pack(pady=5)

    button_query_all_frames = ttk.Button(window, text="Query All Frames", command=query_all_frames)
    button_query_all_frames.pack(pady=5)

    button_query_unprocessed_frames = ttk.Button(window, text="Query Unprocessed Frames", command=query_unprocessed_frames)
    button_query_unprocessed_frames.pack(pady=5)

    button_query_processed_frames = ttk.Button(window, text="Query Processed Frames", command=query_processed_frames)
    button_query_processed_frames.pack(pady=5)

    # Create buttons for delete functions
    button_delete_all_videos = ttk.Button(window, text="Delete All Videos", command=delete_all_videos)
    button_delete_all_videos.pack(pady=5)

    button_delete_all_frames = ttk.Button(window, text="Delete All Frames", command=delete_all_frames)
    button_delete_all_frames.pack(pady=5)

    button_delete_all_data = ttk.Button(window, text="Delete All Data", command=delete_all_data)
    button_delete_all_data.pack(pady=5)

    # Create a panel to display the database values
    result_panel = ttk.Label(window, text="")
    result_panel.pack(pady=10)

    def update_result_panel(rows):
        result_text = ""
        for row in rows:
            result_text += str(row) + "\n"
        result_panel.config(text=result_text)

    def query_all_videos_ui():
        conn = psycopg2.connect(**db_conn_params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM videos")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        update_result_panel(rows)

    def query_all_frames_ui():
        conn = psycopg2.connect(**db_conn_params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM frames")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        update_result_panel(rows)

    # Modify the query functions to update the result panel
    button_query_all_videos.config(command=query_all_videos_ui)
    button_query_all_frames.config(command=query_all_frames_ui)

    window.mainloop()

# Create the UI
create_ui()