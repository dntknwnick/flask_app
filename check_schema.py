"""
Script to check the database schema and make sure all required tables and columns exist.
"""

import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from sqlalchemy import inspect

def check_schema():
    """Check if all required tables and columns exist"""
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Check if tables exist
        tables = inspector.get_table_names()
        required_tables = ['users', 'exam_categories', 'subjects', 'questions', 'options', 'user_exams', 'exam_attempts']
        
        print("Checking tables...")
        for table in required_tables:
            if table in tables:
                print(f"✓ Table '{table}' exists")
            else:
                print(f"✗ Table '{table}' does not exist")
        
        # Check if User model columns exist
        if 'users' in tables:
            print("\nChecking User model columns...")
            user_columns = [c['name'] for c in inspector.get_columns('users')]
            required_user_columns = ['id', 'mobile_number', 'name', 'username', 'avatar', 'role', 'created_at', 'last_login', 'is_profile_complete']
            
            for column in required_user_columns:
                if column in user_columns:
                    print(f"✓ Column 'users.{column}' exists")
                else:
                    print(f"✗ Column 'users.{column}' does not exist")
            
            # Check if there are any users in the database
            print("\nChecking for users...")
            result = db.session.execute("SELECT COUNT(*) FROM users").scalar()
            print(f"Found {result} users in the database")
            
            if result > 0:
                print("\nSample user data:")
                user_data = db.session.execute("SELECT * FROM users LIMIT 1").fetchone()
                for i, column in enumerate(inspector.get_columns('users')):
                    print(f"{column['name']}: {user_data[i]}")
        else:
            print("\nCannot check User model columns because 'users' table does not exist.")

if __name__ == "__main__":
    check_schema()
