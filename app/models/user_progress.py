from app import db
from datetime import datetime

class UserExam(db.Model):
    __tablename__ = 'user_exams'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    purchased_at = db.Column(db.DateTime, default=datetime.utcnow)
    purchase_count = db.Column(db.Integer, default=1)  # Track how many times user purchased this exam
    last_purchased_at = db.Column(db.DateTime, default=datetime.utcnow)
    max_retakes = db.Column(db.Integer, default=3)  # Maximum number of retakes allowed per purchase
    retakes_used = db.Column(db.Integer, default=0)  # Number of retakes used so far

    # Relationships
    user = db.relationship('User', back_populates='exams')
    subject = db.relationship('Subject')
    attempts = db.relationship('ExamAttempt', back_populates='user_exam', lazy='dynamic')

    def __repr__(self):
        return f'<UserExam {self.id} User:{self.user_id} Subject:{self.subject_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'subject_id': self.subject_id,
            'subject_name': self.subject.name if self.subject else None,
            'category_name': self.subject.category.name if self.subject and self.subject.category else None,
            'purchased_at': self.purchased_at.isoformat() if self.purchased_at else None,
            'purchase_count': self.purchase_count,
            'last_purchased_at': self.last_purchased_at.isoformat() if self.last_purchased_at else None,
            'max_retakes': self.max_retakes,
            'retakes_used': self.retakes_used,
            'retakes_remaining': self.max_retakes - self.retakes_used,
            'attempts': [attempt.to_dict() for attempt in self.attempts],
            'attempt_count': self.attempts.count()
        }

class ExamAttempt(db.Model):
    __tablename__ = 'exam_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_exam_id = db.Column(db.Integer, db.ForeignKey('user_exams.id'), nullable=False)
    attempt_number = db.Column(db.Integer, default=1)  # Which attempt number this is for the user
    score = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    wrong_answers = db.Column(db.Integer, default=0)
    unattempted = db.Column(db.Integer, default=0)
    time_taken_seconds = db.Column(db.Integer)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    # Relationships
    user = db.relationship('User', back_populates='attempts')
    user_exam = db.relationship('UserExam', back_populates='attempts')

    def __repr__(self):
        return f'<ExamAttempt {self.id} User:{self.user_id} Score:{self.score}/{self.total_questions}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_exam_id': self.user_exam_id,
            'attempt_number': self.attempt_number,
            'score': self.score,
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers,
            'wrong_answers': self.wrong_answers,
            'unattempted': self.unattempted,
            'time_taken_seconds': self.time_taken_seconds,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
