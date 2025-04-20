"""
Script to update MySQL configuration in .env file.
"""

import os
import getpass

def update_env_file(host, user, password, database):
    """Update the .env file with the new MySQL configuration"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    # Create a backup of the .env file
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            original_content = f.read()
        
        with open(f"{env_path}.bak", 'w') as f:
            f.write(original_content)
        
        print(f"Backup created at {env_path}.bak")
    
    # Read the current .env file
    env_content = []
    db_section = True
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip().startswith('# JWT Configuration'):
                    db_section = False
                
                if not db_section or not (line.strip().startswith('DB_') or line.strip() == ''):
                    env_content.append(line.rstrip())
    
    # Update the .env file
    with open(env_path, 'w') as f:
        f.write("# Database Configuration\n")
        f.write(f"DB_HOST={host}\n")
        f.write(f"DB_USER={user}\n")
        f.write(f"DB_PASSWORD={password}\n")
        f.write(f"DB_NAME={database}\n")
        f.write("\n")
        
        # Write the rest of the content
        for line in env_content:
            f.write(f"{line}\n")
    
    print(f"Updated .env file with new MySQL configuration.")

def main():
    """Main function to update MySQL configuration"""
    print("MySQL Configuration Updater")
    print("==========================")
    
    # Get connection details
    host = input("Enter host (default: localhost): ") or "localhost"
    user = input("Enter username (default: root): ") or "root"
    password = getpass.getpass("Enter password (leave empty for no password): ")
    database = input("Enter database name (default: jishu_db): ") or "jishu_db"
    
    # Update the .env file
    update_env_file(host, user, password, database)
    
    print("\nConfiguration updated successfully!")
    print("\nNext steps:")
    print("1. Run 'python init_db.py' to initialize the database")
    print("2. Run 'python run.py' to start the Flask application")

if __name__ == "__main__":
    main()
