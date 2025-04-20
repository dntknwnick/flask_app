"""
Migration script to add username, avatar, and is_profile_complete fields to the users table.
Run this script from the backend directory.
"""

import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.user import User

def upgrade():
    """Add new columns to the users table"""
    app = create_app()
    with app.app_context():
        # Check if columns already exist
        columns = [c.name for c in User.__table__.columns]
        
        # Add username column if it doesn't exist
        if 'username' not in columns:
            print("Adding username column to users table...")
            db.engine.execute('ALTER TABLE users ADD COLUMN username VARCHAR(50) UNIQUE')
        else:
            print("Column 'username' already exists.")
        
        # Add avatar column if it doesn't exist
        if 'avatar' not in columns:
            print("Adding avatar column to users table...")
            db.engine.execute('ALTER TABLE users ADD COLUMN avatar VARCHAR(255)')
        else:
            print("Column 'avatar' already exists.")
        
        # Add is_profile_complete column if it doesn't exist
        if 'is_profile_complete' not in columns:
            print("Adding is_profile_complete column to users table...")
            db.engine.execute('ALTER TABLE users ADD COLUMN is_profile_complete BOOLEAN DEFAULT FALSE')
        else:
            print("Column 'is_profile_complete' already exists.")
        
        # Update existing users to have default values
        print("Updating existing users with default values...")
        users = User.query.all()
        for i, user in enumerate(users):
            if not user.username:
                user.username = f"user_{user.id}"
            if not user.avatar:
                user.avatar = f"https://randomuser.me/api/portraits/men/{i % 10 + 1}.jpg"
            user.is_profile_complete = True
        
        db.session.commit()
        print("Migration completed successfully!")

if __name__ == "__main__":
    upgrade()
