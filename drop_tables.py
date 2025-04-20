from app import create_app, db

def drop_and_create_tables():
    """Drop all tables and recreate them"""
    app = create_app()
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        print("Database tables reset successfully.")

if __name__ == '__main__':
    drop_and_create_tables() 