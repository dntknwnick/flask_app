from app import db
from datetime import datetime

class ExamCategory(db.Model):
    __tablename__ = 'exam_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255))
    icon = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    subjects = db.relationship('Subject', back_populates='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<ExamCategory {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'subjects': [subject.to_dict() for subject in self.subjects]
        }

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    icon = db.Column(db.String(50))
    is_full_mock = db.Column(db.Boolean, default=False)
    duration_minutes = db.Column(db.Integer, default=60)
    category_id = db.Column(db.Integer, db.ForeignKey('exam_categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    category = db.relationship('ExamCategory', back_populates='subjects')
    questions = db.relationship('Question', back_populates='subject', lazy='dynamic')
    
    def __repr__(self):
        return f'<Subject {self.name} ({self.category.name})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'is_full_mock': self.is_full_mock,
            'duration_minutes': self.duration_minutes,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None
        }

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    marks = db.Column(db.Integer, default=4)  # Default marks for correct answer
    negative_marks = db.Column(db.Integer, default=1)  # Default negative marks for wrong answer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    subject = db.relationship('Subject', back_populates='questions')
    options = db.relationship('Option', back_populates='question', lazy='dynamic')
    
    def __repr__(self):
        return f'<Question {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'subject_id': self.subject_id,
            'difficulty': self.difficulty,
            'marks': self.marks,
            'negative_marks': self.negative_marks,
            'options': [option.to_dict() for option in self.options]
        }

class Option(db.Model):
    __tablename__ = 'options'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    question = db.relationship('Question', back_populates='options')
    
    def __repr__(self):
        return f'<Option {self.id} for Question {self.question_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'is_correct': self.is_correct
        }
