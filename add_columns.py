"""
Script to manually add the required columns to the users table.
"""

import os
import sys
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'jishu_db')

def add_columns():
    """Manually add the required columns to the users table"""
    try:
        # Connect to MySQL server
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        with connection.cursor() as cursor:
            # Check if users table exists
            cursor.execute("SHOW TABLES LIKE 'users'")
            if not cursor.fetchone():
                print("Error: 'users' table does not exist.")
                return False
            
            # Check if columns exist
            cursor.execute("SHOW COLUMNS FROM users")
            columns = [column[0] for column in cursor.fetchall()]
            
            # Add username column if it doesn't exist
            if 'username' not in columns:
                print("Adding username column to users table...")
                cursor.execute("ALTER TABLE users ADD COLUMN username VARCHAR(50) UNIQUE")
            else:
                print("Column 'username' already exists.")
            
            # Add avatar column if it doesn't exist
            if 'avatar' not in columns:
                print("Adding avatar column to users table...")
                cursor.execute("ALTER TABLE users ADD COLUMN avatar VARCHAR(255)")
            else:
                print("Column 'avatar' already exists.")
            
            # Add is_profile_complete column if it doesn't exist
            if 'is_profile_complete' not in columns:
                print("Adding is_profile_complete column to users table...")
                cursor.execute("ALTER TABLE users ADD COLUMN is_profile_complete BOOLEAN DEFAULT FALSE")
            else:
                print("Column 'is_profile_complete' already exists.")
            
            # Update existing users to have default values
            print("Updating existing users with default values...")
            cursor.execute("SELECT id FROM users")
            users = cursor.fetchall()
            
            for i, (user_id,) in enumerate(users):
                cursor.execute(
                    "UPDATE users SET username = %s, avatar = %s, is_profile_complete = TRUE WHERE id = %s",
                    (f"user_{user_id}", f"https://randomuser.me/api/portraits/men/{i % 10 + 1}.jpg", user_id)
                )
            
            connection.commit()
            print("Columns added and users updated successfully!")
        
        connection.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    add_columns()
