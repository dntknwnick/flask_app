"""
Script to test MySQL connection with different credentials.
"""

import pymysql
import getpass

def test_connection(host, user, password, database=None):
    """Test MySQL connection with the given credentials"""
    try:
        # Connect to MySQL server
        if database:
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        else:
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password
            )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"Connection successful! MySQL version: {version[0]}")
        
        connection.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

def main():
    """Main function to test MySQL connection"""
    print("MySQL Connection Tester")
    print("======================")
    
    # Get connection details
    host = input("Enter host (default: localhost): ") or "localhost"
    user = input("Enter username (default: root): ") or "root"
    password = getpass.getpass("Enter password (leave empty for no password): ")
    
    # Test connection without database
    print("\nTesting connection to MySQL server...")
    if test_connection(host, user, password):
        # If connection is successful, test with database
        database = input("\nEnter database name to test (leave empty to skip): ")
        if database:
            print(f"\nTesting connection to database '{database}'...")
            test_connection(host, user, password, database)
        
        # Show connection string for .env file
        print("\n======================")
        print("Use these credentials in your .env file:")
        print("======================")
        print(f"DB_HOST={host}")
        print(f"DB_USER={user}")
        print(f"DB_PASSWORD={password}")
        if database:
            print(f"DB_NAME={database}")
        else:
            print("DB_NAME=jishu_db")
    
    print("\nTest completed.")

if __name__ == "__main__":
    main()
