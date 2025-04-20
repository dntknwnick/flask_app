from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.api import bp
from app.models.exam import ExamCategory, Subject
from app.models.user import User

@bp.route('/subjects', methods=['GET'])
def get_subjects():
    """Get all subjects, optionally filtered by category"""
    category_id = request.args.get('category_id', type=int)
    
    if category_id:
        subjects = Subject.query.filter_by(category_id=category_id).all()
    else:
        subjects = Subject.query.all()
    
    return jsonify([subject.to_dict() for subject in subjects])

@bp.route('/subjects/<int:id>', methods=['GET'])
def get_subject(id):
    """Get a specific subject by ID"""
    subject = Subject.query.get_or_404(id)
    return jsonify(subject.to_dict())

@bp.route('/subjects', methods=['POST'])
@jwt_required()
def create_subject():
    """Create a new subject (admin only)"""
    # Check if user is admin
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin():
        return jsonify({'error': 'Admin privileges required'}), 403
    
    data = request.get_json() or {}
    
    required_fields = ['name', 'category_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if category exists
    category = ExamCategory.query.get(data['category_id'])
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    # Check if subject already exists in this category
    if Subject.query.filter_by(name=data['name'], category_id=data['category_id']).first():
        return jsonify({'error': 'Subject already exists in this category'}), 400
    
    subject = Subject(
        name=data['name'],
        description=data.get('description', ''),
        icon=data.get('icon', ''),
        is_full_mock=data.get('is_full_mock', False),
        duration_minutes=data.get('duration_minutes', 60),
        category_id=data['category_id']
    )
    
    db.session.add(subject)
    db.session.commit()
    
    return jsonify(subject.to_dict()), 201

@bp.route('/subjects/<int:id>', methods=['PUT'])
@jwt_required()
def update_subject(id):
    """Update a subject (admin only)"""
    # Check if user is admin
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin():
        return jsonify({'error': 'Admin privileges required'}), 403
    
    subject = Subject.query.get_or_404(id)
    data = request.get_json() or {}
    
    if 'name' in data and 'category_id' in data:
        # Check if name is being changed and if it already exists in the category
        if (data['name'] != subject.name or data['category_id'] != subject.category_id) and \
           Subject.query.filter_by(name=data['name'], category_id=data['category_id']).first():
            return jsonify({'error': 'Subject already exists in this category'}), 400
    
    if 'name' in data:
        subject.name = data['name']
    
    if 'description' in data:
        subject.description = data['description']
    
    if 'icon' in data:
        subject.icon = data['icon']
    
    if 'is_full_mock' in data:
        subject.is_full_mock = data['is_full_mock']
    
    if 'duration_minutes' in data:
        subject.duration_minutes = data['duration_minutes']
    
    if 'category_id' in data:
        # Check if category exists
        category = ExamCategory.query.get(data['category_id'])
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        subject.category_id = data['category_id']
    
    db.session.commit()
    
    return jsonify(subject.to_dict())

@bp.route('/subjects/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_subject(id):
    """Delete a subject (admin only)"""
    # Check if user is admin
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin():
        return jsonify({'error': 'Admin privileges required'}), 403
    
    subject = Subject.query.get_or_404(id)
    
    # Check if subject has questions
    if subject.questions.count() > 0:
        return jsonify({'error': 'Cannot delete subject with questions'}), 400
    
    db.session.delete(subject)
    db.session.commit()
    
    return jsonify({'message': 'Subject deleted successfully'})
