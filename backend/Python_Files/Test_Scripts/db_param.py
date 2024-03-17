import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="KIT_ADMIN",
    password="hvz0rfb4BGQ_uqg3wfg",
    host="kit-db.c9gssgcyk1lb.us-east-1.rds.amazonaws.com",
    port="5432"
)
cur = conn.cursor()

# SQL to delete existing tables
drop_tables = """
DROP TABLE IF EXISTS NutritionalFacts;
DROP TABLE IF EXISTS ObjectDetails;
DROP TABLE IF EXISTS AnalysisResults;
DROP TABLE IF EXISTS FoodItem;
DROP TABLE IF EXISTS Frames;
DROP TABLE IF EXISTS Videos;
"""

# Execute the SQL to delete existing tables
cur.execute(drop_tables)

# SQL for creating tables
create_videos_table = """
CREATE TABLE IF NOT EXISTS Videos (
    VideoID SERIAL PRIMARY KEY,
    DeviceID VARCHAR(255),
    Timestamp TIMESTAMP NOT NULL,
    Path TEXT NOT NULL,
    MotionDetected BOOLEAN,
    Processed BOOLEAN DEFAULT FALSE
);
"""

create_frames_table = """
CREATE TABLE IF NOT EXISTS Frames (
    FrameID SERIAL PRIMARY KEY,
    VideoID INT,
    Timestamp TIMESTAMP NOT NULL,
    Path TEXT NOT NULL,
    Processed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (VideoID) REFERENCES Videos (VideoID)
);
"""

create_food_item_table = """
CREATE TABLE IF NOT EXISTS FoodItem (
    ItemID SERIAL PRIMARY KEY,
    FrameID INT,
    Details JSONB,
    FOREIGN KEY (FrameID) REFERENCES Frames (FrameID)
);
"""

# Execute the SQL statements
cur.execute(create_videos_table)
cur.execute(create_frames_table)
cur.execute(create_food_item_table)

# Commit the transactions
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print("Tables created successfully.")