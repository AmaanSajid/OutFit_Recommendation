import sqlite3
import os
from datetime import datetime

def insert_clothing_item(item_type, color, style, uploaded_file):
    conn = sqlite3.connect('wardrobe.db')
    cursor = conn.cursor()
    
    # Generate a unique filename
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name}"
    uploads_dir = os.path.abspath(os.path.join(os.getcwd(), 'uploads'))
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    file_path = os.path.join(uploads_dir, filename)
    
    # Save the image file
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getvalue())
    
    cursor.execute('''
    INSERT INTO clothes (type, color, style, image_path)
    VALUES (?, ?, ?, ?)
    ''', (item_type, color, style, file_path))
    
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    
    return item_id

def get_all_clothing_items():
    conn = sqlite3.connect('wardrobe.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM clothes')
    items = cursor.fetchall()
    
    conn.close()
    
    return items

def get_clothing_item_by_id(item_id):
    conn = sqlite3.connect('wardrobe.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM clothes WHERE id = ?', (item_id,))
    item = cursor.fetchone()
    
    conn.close()
    
    return item