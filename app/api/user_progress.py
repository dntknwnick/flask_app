from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.api import bp
from app.models.user import User
from app.models.exam import Subject, Question
from app.models.user_progress import UserExam, ExamAttempt
from datetime import datetime

@bp.route('/user/exams', methods=['GET'])
@jwt_required()
def get_user_exams():
    """Get all exams purchased by the current user"""
    current_user_id = get_jwt_identity()

    user_exams = UserExam.query.filter_by(user_id=current_user_id).all()
    return jsonify([exam.to_dict() for exam in user_exams])

@bp.route('/user/exams/<int:subject_id>/purchase', methods=['POST'])
@jwt_required()
def purchase_exam(subject_id):
    """Purchase an exam - allows multiple purchases of the same exam"""
    current_user_id = get_jwt_identity()

    # Check if subject exists
    subject = Subject.query.get_or_404(subject_id)

    # Check if user has already purchased this exam
    existing = UserExam.query.filter_by(
        user_id=current_user_id,
        subject_id=subject_id
    ).first()

    if existing:
        # User has already purchased this exam, increment the purchase count
        existing.purchase_count += 1
        existing.last_purchased_at = datetime.utcnow()
        # Reset retakes for new purchase
        existing.retakes_used = 0
        db.session.commit()
        return jsonify(existing.to_dict()), 200
    else:
        # First time purchase
        user_exam = UserExam(
            user_id=current_user_id,
            subject_id=subject_id,
            purchase_count=1,
            purchased_at=datetime.utcnow(),
            last_purchased_at=datetime.utcnow(),
            max_retakes=3,
            retakes_used=0
        )

        db.session.add(user_exam)
        db.session.commit()

        return jsonify(user_exam.to_dict()), 201

@bp.route('/user/exams/<int:user_exam_id>/start', methods=['POST'])
@jwt_required()
def start_exam_attempt(user_exam_id):
    """Start a new exam attempt (limited to max_retakes per purchase)"""
    current_user_id = get_jwt_identity()

    # Check if user exam exists and belongs to the current user
    user_exam = UserExam.query.get_or_404(user_exam_id)

    if user_exam.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized access to this exam'}), 403

    # Check if user has retakes remaining
    if user_exam.retakes_used >= user_exam.max_retakes:
        return jsonify({
            'error': 'Maximum retakes limit reached for this exam',
            'retakes_used': user_exam.retakes_used,
            'max_retakes': user_exam.max_retakes
        }), 400

    # Get subject to determine question count
    subject = Subject.query.get(user_exam.subject_id)

    # Get questions for this subject
    questions = Question.query.filter_by(subject_id=user_exam.subject_id).all()
    total_questions = len(questions)

    if total_questions == 0:
        return jsonify({'error': 'No questions available for this exam'}), 400

    # Calculate attempt number (previous attempts count + 1)
    attempt_number = user_exam.attempts.count() + 1

    # Increment retakes used
    user_exam.retakes_used += 1

    # Create new exam attempt
    attempt = ExamAttempt(
        user_id=current_user_id,
        user_exam_id=user_exam_id,
        attempt_number=attempt_number,
        total_questions=total_questions,
        started_at=datetime.utcnow()
    )

    db.session.add(attempt)
    db.session.commit()

    # Return attempt details and questions
    return jsonify({
        'attempt': attempt.to_dict(),
        'questions': [q.to_dict() for q in questions]
    })

@bp.route('/user/attempts/<int:attempt_id>/submit', methods=['POST'])
@jwt_required()
def submit_exam_attempt(attempt_id):
    """Submit an exam attempt with answers"""
    current_user_id = get_jwt_identity()

    # Check if attempt exists and belongs to the current user
    attempt = ExamAttempt.query.get_or_404(attempt_id)

    if attempt.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized access to this attempt'}), 403

    if attempt.completed_at:
        return jsonify({'error': 'This attempt has already been submitted'}), 400

    data = request.get_json() or {}

    if 'answers' not in data:
        return jsonify({'error': 'Answers are required'}), 400

    answers = data['answers']  # Format: {question_id: option_id}
    time_taken = data.get('time_taken_seconds', 0)

    # Calculate score
    correct_answers = 0
    wrong_answers = 0

    for question_id, option_id in answers.items():
        # Get the question and check if the option is correct
        question = Question.query.get(int(question_id))
        if not question:
            continue

        option = next((o for o in question.options if o.id == int(option_id)), None)
        if not option:
            continue

        if option.is_correct:
            correct_answers += 1
        else:
            wrong_answers += 1

    # Calculate score
    score = (correct_answers * 4) - (wrong_answers * 1)  # +4 for correct, -1 for wrong
    unattempted = attempt.total_questions - (correct_answers + wrong_answers)

    # Update attempt
    attempt.score = score
    attempt.correct_answers = correct_answers
    attempt.wrong_answers = wrong_answers
    attempt.unattempted = unattempted
    attempt.time_taken_seconds = time_taken
    attempt.completed_at = datetime.utcnow()

    db.session.commit()

    return jsonify(attempt.to_dict())

@bp.route('/user/attempts', methods=['GET'])
@jwt_required()
def get_user_attempts():
    """Get all exam attempts by the current user"""
    current_user_id = get_jwt_identity()

    attempts = ExamAttempt.query.filter_by(user_id=current_user_id).all()
    return jsonify([attempt.to_dict() for attempt in attempts])

@bp.route('/user/attempts/<int:attempt_id>', methods=['GET'])
@jwt_required()
def get_attempt_details(attempt_id):
    """Get details of a specific exam attempt"""
    current_user_id = get_jwt_identity()

    attempt = ExamAttempt.query.get_or_404(attempt_id)

    if attempt.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized access to this attempt'}), 403

    return jsonify(attempt.to_dict())
