"""
Script to check the database schema and make sure all required tables and columns exist.
"""

from app import create_app, db
from app.models.user import User
from app.models.exam import ExamCategory, Subject, Question, Option
from app.models.user_progress import UserExam, ExamAttempt

def check_schema():
    """Check if all required tables and columns exist"""
    app = create_app()
    with app.app_context():
        # Check if tables exist
        tables = db.engine.table_names()
        required_tables = ['users', 'exam_categories', 'subjects', 'questions', 'options', 'user_exams', 'exam_attempts']
        
        print("Checking tables...")
        for table in required_tables:
            if table in tables:
                print(f"✓ Table '{table}' exists")
            else:
                print(f"✗ Table '{table}' does not exist")
        
        # Check if User model columns exist
        print("\nChecking User model columns...")
        user_columns = [c.name for c in User.__table__.columns]
        required_user_columns = ['id', 'mobile_number', 'name', 'username', 'avatar', 'role', 'created_at', 'last_login', 'is_profile_complete']
        
        for column in required_user_columns:
            if column in user_columns:
                print(f"✓ Column 'users.{column}' exists")
            else:
                print(f"✗ Column 'users.{column}' does not exist")
        
        # Check if there are any users in the database
        print("\nChecking for users...")
        user_count = User.query.count()
        print(f"Found {user_count} users in the database")
        
        if user_count > 0:
            print("\nSample user data:")
            user = User.query.first()
            print(f"ID: {user.id}")
            print(f"Mobile: {user.mobile_number}")
            print(f"Name: {user.name}")
            print(f"Username: {user.username}")
            print(f"Avatar: {user.avatar}")
            print(f"Role: {user.role}")
            print(f"Is Profile Complete: {user.is_profile_complete}")

if __name__ == "__main__":
    check_schema()
