from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.api import bp
from app.models.exam import Subject, Question, Option
from app.models.user import User

@bp.route('/questions', methods=['GET'])
@jwt_required()
def get_questions():
    """Get questions, optionally filtered by subject"""
    subject_id = request.args.get('subject_id', type=int)
    
    if subject_id:
        questions = Question.query.filter_by(subject_id=subject_id).all()
    else:
        questions = Question.query.all()
    
    return jsonify([question.to_dict() for question in questions])

@bp.route('/questions/<int:id>', methods=['GET'])
@jwt_required()
def get_question(id):
    """Get a specific question by ID"""
    question = Question.query.get_or_404(id)
    return jsonify(question.to_dict())

@bp.route('/questions', methods=['POST'])
@jwt_required()
def create_question():
    """Create a new question with options (admin only)"""
    # Check if user is admin
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin():
        return jsonify({'error': 'Admin privileges required'}), 403
    
    data = request.get_json() or {}
    
    required_fields = ['text', 'subject_id', 'options']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if subject exists
    subject = Subject.query.get(data['subject_id'])
    if not subject:
        return jsonify({'error': 'Subject not found'}), 404
    
    # Check if options are provided and at least one is correct
    options = data.get('options', [])
    if not options or len(options) < 2:
        return jsonify({'error': 'At least 2 options are required'}), 400
    
    if not any(option.get('is_correct', False) for option in options):
        return jsonify({'error': 'At least one option must be correct'}), 400
    
    # Create question
    question = Question(
        text=data['text'],
        subject_id=data['subject_id'],
        difficulty=data.get('difficulty', 'medium'),
        marks=data.get('marks', 4),
        negative_marks=data.get('negative_marks', 1)
    )
    
    db.session.add(question)
    db.session.flush()  # Get the question ID without committing
    
    # Create options
    for option_data in options:
        option = Option(
            text=option_data['text'],
            question_id=question.id,
            is_correct=option_data.get('is_correct', False)
        )
        db.session.add(option)
    
    db.session.commit()
    
    return jsonify(question.to_dict()), 201

@bp.route('/questions/<int:id>', methods=['PUT'])
@jwt_required()
def update_question(id):
    """Update a question (admin only)"""
    # Check if user is admin
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin():
        return jsonify({'error': 'Admin privileges required'}), 403
    
    question = Question.query.get_or_404(id)
    data = request.get_json() or {}
    
    if 'text' in data:
        question.text = data['text']
    
    if 'difficulty' in data:
        question.difficulty = data['difficulty']
    
    if 'marks' in data:
        question.marks = data['marks']
    
    if 'negative_marks' in data:
        question.negative_marks = data['negative_marks']
    
    if 'subject_id' in data:
        # Check if subject exists
        subject = Subject.query.get(data['subject_id'])
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        question.subject_id = data['subject_id']
    
    # Update options if provided
    if 'options' in data:
        options = data['options']
        
        # Check if options are valid
        if not options or len(options) < 2:
            return jsonify({'error': 'At least 2 options are required'}), 400
        
        if not any(option.get('is_correct', False) for option in options):
            return jsonify({'error': 'At least one option must be correct'}), 400
        
        # Delete existing options
        Option.query.filter_by(question_id=question.id).delete()
        
        # Create new options
        for option_data in options:
            option = Option(
                text=option_data['text'],
                question_id=question.id,
                is_correct=option_data.get('is_correct', False)
            )
            db.session.add(option)
    
    db.session.commit()
    
    return jsonify(question.to_dict())

@bp.route('/questions/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_question(id):
    """Delete a question (admin only)"""
    # Check if user is admin
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin():
        return jsonify({'error': 'Admin privileges required'}), 403
    
    question = Question.query.get_or_404(id)
    
    # Delete associated options first
    Option.query.filter_by(question_id=question.id).delete()
    
    db.session.delete(question)
    db.session.commit()
    
    return jsonify({'message': 'Question deleted successfully'})
