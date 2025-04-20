from app import db

from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    mobile_number = db.Column(db.String(15), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100))
    avatar = db.Column(db.String(255))  # URL or identifier for avatar
    role = db.Column(db.String(20), default='student')  # 'admin' or 'student'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_profile_complete = db.Column(db.Boolean, default=False)  # Flag to check if username and avatar are set

    # Relationships
    exams = db.relationship('UserExam', back_populates='user', lazy='dynamic')
    attempts = db.relationship('ExamAttempt', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.mobile_number}>'

    @staticmethod
    def get_by_mobile(mobile_number):
        return User.query.filter_by(mobile_number=mobile_number).first()

    def is_admin(self):
        return self.role == 'admin'
