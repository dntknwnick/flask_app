from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.api import bp
from app.models.exam import ExamCategory, Subject
from app.models.user import User

@bp.route('/exam-categories', methods=['GET'])
def get_exam_categories():
    """Get all exam categories"""
    categories = ExamCategory.query.all()
    return jsonify([category.to_dict() for category in categories])

@bp.route('/exam-categories/<int:id>', methods=['GET'])
def get_exam_category(id):
    """Get a specific exam category by ID"""
    category = ExamCategory.query.get_or_404(id)
    return jsonify(category.to_dict())

@bp.route('/exam-categories', methods=['POST'])
@jwt_required()
def create_exam_category():
    """Create a new exam category (admin only)"""
    # Check if user is admin
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin():
        return jsonify({'error': 'Admin privileges required'}), 403
    
    data = request.get_json() or {}
    
    if 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    # Check if category already exists
    if ExamCategory.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Exam category already exists'}), 400
    
    category = ExamCategory(
        name=data['name'],
        description=data.get('description', ''),
        icon=data.get('icon', '')
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify(category.to_dict()), 201

@bp.route('/exam-categories/<int:id>', methods=['PUT'])
@jwt_required()
def update_exam_category(id):
    """Update an exam category (admin only)"""
    # Check if user is admin
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin():
        return jsonify({'error': 'Admin privileges required'}), 403
    
    category = ExamCategory.query.get_or_404(id)
    data = request.get_json() or {}
    
    if 'name' in data:
        # Check if name is being changed and if it already exists
        if data['name'] != category.name and ExamCategory.query.filter_by(name=data['name']).first():
            return jsonify({'error': 'Exam category already exists'}), 400
        category.name = data['name']
    
    if 'description' in data:
        category.description = data['description']
    
    if 'icon' in data:
        category.icon = data['icon']
    
    db.session.commit()
    
    return jsonify(category.to_dict())

@bp.route('/exam-categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_exam_category(id):
    """Delete an exam category (admin only)"""
    # Check if user is admin
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin():
        return jsonify({'error': 'Admin privileges required'}), 403
    
    category = ExamCategory.query.get_or_404(id)
    
    # Check if category has subjects
    if category.subjects.count() > 0:
        return jsonify({'error': 'Cannot delete category with subjects'}), 400
    
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({'message': 'Exam category deleted successfully'})
