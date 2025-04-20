from app import create_app, db
from app.models import User, ExamCategory, Subject, Question, Option, UserExam, ExamAttempt
from datetime import datetime, timedelta

def init_db():
    """Initialize the database with sample data"""
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()

        # Check if data already exists
        if User.query.count() > 0:
            print("Database already contains data. Skipping initialization.")
            return

        # Create admin user
        admin = User(
            mobile_number='9876543210',
            role='admin',
            name='Admin User',
            avatar='https://randomuser.me/api/portraits/men/1.jpg',
            is_profile_complete=True
        )
        db.session.add(admin)

        # Create student user
        student = User(
            mobile_number='9876543211',
            role='student',
            name='Student User',
            avatar='https://randomuser.me/api/portraits/women/1.jpg',
            is_profile_complete=True
        )
        db.session.add(student)

        # Create exam categories
        neet = ExamCategory(name='NEET', description='Medical Entrance Exam - Physics, Chemistry, Biology', icon='medical-bag')
        jee_advance = ExamCategory(name='JEE_Advance', description='Engineering Entrance - Advanced Level', icon='atom')
        jee_mains = ExamCategory(name='JEE_Mains', description='Engineering Entrance - Main Level', icon='calculator-variant')
        cet = ExamCategory(name='CET', description='Common Entrance Test for State Colleges', icon='school')

        db.session.add_all([neet, jee_advance, jee_mains, cet])
        db.session.flush()  # Get IDs without committing

        # Create subjects for NEET
        physics_neet = Subject(name='Physics', description='NEET Physics', icon='atom', category_id=neet.id, is_full_mock=False, duration_minutes=60)
        chemistry_neet = Subject(name='Chemistry', description='NEET Chemistry', icon='flask-empty-outline', category_id=neet.id, is_full_mock=False, duration_minutes=60)
        botany = Subject(name='Botany', description='NEET Botany', icon='virus-outline', category_id=neet.id, is_full_mock=False, duration_minutes=60)
        zoology = Subject(name='Zoology', description='NEET Zoology', icon='dna', category_id=neet.id, is_full_mock=False, duration_minutes=60)
        neet_full = Subject(name='Full Mock Exam', description='NEET Full Mock Test', icon='stethoscope', category_id=neet.id, is_full_mock=True, duration_minutes=180)

        # Create subjects for JEE Advanced
        physics_jee_adv = Subject(name='Physics', description='JEE Advanced Physics', icon='atom', category_id=jee_advance.id, is_full_mock=False, duration_minutes=60)
        chemistry_jee_adv = Subject(name='Chemistry', description='JEE Advanced Chemistry', icon='flask-empty-outline', category_id=jee_advance.id, is_full_mock=False, duration_minutes=60)
        math_jee_adv = Subject(name='Mathematics', description='JEE Advanced Mathematics', icon='calculator-variant-outline', category_id=jee_advance.id, is_full_mock=False, duration_minutes=60)
        jee_adv_full = Subject(name='Full Mock Exam', description='JEE Advanced Full Mock Test', icon='stethoscope', category_id=jee_advance.id, is_full_mock=True, duration_minutes=180)

        # Create subjects for JEE Mains
        physics_jee_main = Subject(name='Physics', description='JEE Mains Physics', icon='atom', category_id=jee_mains.id, is_full_mock=False, duration_minutes=60)
        chemistry_jee_main = Subject(name='Chemistry', description='JEE Mains Chemistry', icon='flask-empty-outline', category_id=jee_mains.id, is_full_mock=False, duration_minutes=60)
        math_jee_main = Subject(name='Mathematics', description='JEE Mains Mathematics', icon='calculator-variant-outline', category_id=jee_mains.id, is_full_mock=False, duration_minutes=60)
        jee_main_full = Subject(name='Full Mock Exam', description='JEE Mains Full Mock Test', icon='stethoscope', category_id=jee_mains.id, is_full_mock=True, duration_minutes=180)

        # Create subjects for CET
        physics_cet = Subject(name='Physics', description='CET Physics', icon='atom', category_id=cet.id, is_full_mock=False, duration_minutes=60)
        chemistry_cet = Subject(name='Chemistry', description='CET Chemistry', icon='flask-empty-outline', category_id=cet.id, is_full_mock=False, duration_minutes=60)
        math_cet = Subject(name='Mathematics', description='CET Mathematics', icon='calculator-variant-outline', category_id=cet.id, is_full_mock=False, duration_minutes=60)
        cet_full = Subject(name='Full Mock Exam', description='CET Full Mock Test', icon='stethoscope', category_id=cet.id, is_full_mock=True, duration_minutes=150)

        subjects = [
            physics_neet, chemistry_neet, botany, zoology, neet_full,
            physics_jee_adv, chemistry_jee_adv, math_jee_adv, jee_adv_full,
            physics_jee_main, chemistry_jee_main, math_jee_main, jee_main_full,
            physics_cet, chemistry_cet, math_cet, cet_full
        ]

        db.session.add_all(subjects)
        db.session.flush()

        # Create sample questions for Physics NEET
        q1 = Question(text="A particle moves in a straight line with constant acceleration. If the velocity of the particle is v₁ and v₂ at times t₁ and t₂ respectively, the velocity at time (t₁ + t₂)/2 is:", subject_id=physics_neet.id)
        db.session.add(q1)
        db.session.flush()

        options_q1 = [
            Option(text="(v₁ + v₂)/2", question_id=q1.id, is_correct=True),
            Option(text="√(v₁v₂)", question_id=q1.id, is_correct=False),
            Option(text="2v₁v₂/(v₁ + v₂)", question_id=q1.id, is_correct=False),
            Option(text="(v₁² + v₂²)/(v₁ + v₂)", question_id=q1.id, is_correct=False)
        ]
        db.session.add_all(options_q1)

        q2 = Question(text="The dimensional formula for the coefficient of viscosity is:", subject_id=physics_neet.id)
        db.session.add(q2)
        db.session.flush()

        options_q2 = [
            Option(text="[ML⁻¹T⁻¹]", question_id=q2.id, is_correct=True),
            Option(text="[ML⁻²T⁻¹]", question_id=q2.id, is_correct=False),
            Option(text="[MLT⁻¹]", question_id=q2.id, is_correct=False),
            Option(text="[ML⁻¹T⁻²]", question_id=q2.id, is_correct=False)
        ]
        db.session.add_all(options_q2)

        # Create sample questions for Chemistry NEET
        q3 = Question(text="Which of the following is the correct order of increasing acid strength?", subject_id=chemistry_neet.id)
        db.session.add(q3)
        db.session.flush()

        options_q3 = [
            Option(text="HF < HCl < HBr < HI", question_id=q3.id, is_correct=True),
            Option(text="HI < HBr < HCl < HF", question_id=q3.id, is_correct=False),
            Option(text="HF < HI < HBr < HCl", question_id=q3.id, is_correct=False),
            Option(text="HCl < HBr < HI < HF", question_id=q3.id, is_correct=False)
        ]
        db.session.add_all(options_q3)

        # Create sample user exam purchases and attempts
        # Student purchases Physics NEET multiple times
        now = datetime.utcnow()

        # First purchase (3 days ago)
        user_exam = UserExam(
            user_id=student.id,
            subject_id=physics_neet.id,
            purchase_count=1,  # Purchased once
            purchased_at=now - timedelta(days=3),
            last_purchased_at=now - timedelta(days=3),
            max_retakes=3,
            retakes_used=2  # Used 2 out of 3 retakes
        )
        db.session.add(user_exam)
        db.session.flush()

        # Add some exam attempts
        attempt1 = ExamAttempt(
            user_id=student.id,
            user_exam_id=user_exam.id,
            attempt_number=1,
            score=32,  # 8 correct answers (4 points each)
            total_questions=50,
            correct_answers=8,
            wrong_answers=12,
            unattempted=30,
            time_taken_seconds=2400,  # 40 minutes
            started_at=now - timedelta(days=2, hours=5),
            completed_at=now - timedelta(days=2, hours=4, minutes=20)
        )

        attempt2 = ExamAttempt(
            user_id=student.id,
            user_exam_id=user_exam.id,
            attempt_number=2,
            score=40,  # 10 correct answers (4 points each)
            total_questions=50,
            correct_answers=10,
            wrong_answers=10,
            unattempted=30,
            time_taken_seconds=2700,  # 45 minutes
            started_at=now - timedelta(days=1, hours=3),
            completed_at=now - timedelta(days=1, hours=2, minutes=15)
        )

        db.session.add_all([attempt1, attempt2])

        # Commit all changes
        db.session.commit()

        print("Database initialized with sample data.")

if __name__ == '__main__':
    init_db()
