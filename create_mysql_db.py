"""
Script to create the MySQL database for the Jishu application.
"""

import os
import pymysql
import getpass
from dotenv import load_dotenv

def create_database():
    """Create the database using credentials from .env or user input"""
    # Try to load from .env first
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
        
        host = os.environ.get('DB_HOST')
        user = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')
        database = os.environ.get('DB_NAME')
        
        if host and user and database:
            print(f"Using database configuration from .env file:")
            print(f"Host: {host}")
            print(f"User: {user}")
            print(f"Database: {database}")
            
            use_env = input("\nUse these credentials? (Y/n): ").lower() != 'n'
            
            if not use_env:
                host, user, password, database = get_user_credentials()
        else:
            host, user, password, database = get_user_credentials()
    else:
        host, user, password, database = get_user_credentials()
    
    try:
        # Connect to MySQL server
        print(f"\nConnecting to MySQL server at {host}...")
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password
        )
        
        with connection.cursor() as cursor:
            # Check if database exists
            cursor.execute(f"SHOW DATABASES LIKE '{database}'")
            result = cursor.fetchone()
            
            if not result:
                print(f"Creating database '{database}'...")
                cursor.execute(f"CREATE DATABASE {database}")
                print(f"Database '{database}' created successfully!")
            else:
                print(f"Database '{database}' already exists.")
        
        connection.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_user_credentials():
    """Get database credentials from user input"""
    print("\nEnter MySQL credentials:")
    host = input("Host (default: localhost): ") or "localhost"
    user = input("Username (default: root): ") or "root"
    password = getpass.getpass("Password (leave empty for no password): ")
    database = input("Database name (default: jishu_db): ") or "jishu_db"
    
    return host, user, password, database

def main():
    """Main function to create the database"""
    print("MySQL Database Creator for Jishu")
    print("===============================")
    
    if create_database():
        print("\nDatabase setup completed successfully!")
        print("\nNext steps:")
        print("1. Run 'python init_db.py' to initialize the database tables and sample data")
        print("2. Run 'python run.py' to start the Flask application")
    else:
        print("\nDatabase setup failed.")
        print("Please check your MySQL credentials and try again.")

if __name__ == "__main__":
    main()
