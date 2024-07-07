import sqlite3
import os

# Ensure the 'uploads' directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('wardrobe.db')
cursor = conn.cursor()

# Create the clothes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS clothes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    color TEXT NOT NULL,
    style TEXT NOT NULL,
    image_path TEXT NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")