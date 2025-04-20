from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from app.auth import bp
from app.models.user import User
from app.utils.otp import generate_otp, verify_otp, send_otp
import random  # For mock OTP generation

# Store OTPs temporarily (in production, use Redis or another persistent store)
otp_store = {}

@bp.route('/request-otp', methods=['POST'])
def request_otp():
    data = request.get_json() or {}

    if 'mobile_number' not in data:
        return jsonify({'error': 'Mobile number is required'}), 400

    mobile_number = data['mobile_number']

    # In a real app, validate the mobile number format here

    # Hardcoded OTP for development
    # TODO: Replace with actual OTP generation and SMS sending in production
    otp = '123456'

    # Store OTP with expiry (in a real app, use Redis with TTL)
    otp_store[mobile_number] = otp

    # In a real app, send the OTP via SMS
    # For development, just return it in the response
    print(f"OTP for {mobile_number}: {otp}")

    return jsonify({
        'message': 'OTP sent successfully',
        'otp': otp  # Remove this in production!
    })

@bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json() or {}

    if 'mobile_number' not in data or 'otp' not in data:
        return jsonify({'error': 'Mobile number and OTP are required'}), 400

    mobile_number = data['mobile_number']
    otp = data['otp']

    # Verify OTP
    stored_otp = otp_store.get(mobile_number)

    # For development, always accept '123456' as a valid OTP
    # TODO: Remove this in production!
    if otp == '123456':
        pass  # Accept hardcoded OTP
    elif not stored_otp or stored_otp != otp:
        return jsonify({'error': 'Invalid OTP'}), 401

    # OTP is valid, clear it from store
    otp_store.pop(mobile_number, None)

    # Check if user exists, create if not
    user = User.get_by_mobile(mobile_number)
    print(user)
    is_new_user = False

    if not user:
        # For demo purposes, make the first user an admin
        is_first_user = User.query.count() == 0
        role = 'admin' if is_first_user else 'student'

        user = User(
            mobile_number=mobile_number,
            role=role,
            is_profile_complete=False
        )
        db.session.add(user)
        db.session.commit()
        is_new_user = True

    # Generate tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'mobile_number': user.mobile_number,
            'name': user.name,
            'avatar': user.avatar,
            'role': user.role,
            'is_profile_complete': user.is_profile_complete
        },
        'is_new_user': is_new_user
    })

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)

    return jsonify({'access_token': access_token})

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'mobile_number': user.mobile_number,
        'name': user.name,
        'avatar': user.avatar,
        'role': user.role,
        'is_profile_complete': user.is_profile_complete
    })

@bp.route('/update-profile', methods=['POST'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json() or {}

    # Update user profile
    if 'name' in data:
        user.name = data['name']
    if 'avatar' in data:
        user.avatar = data['avatar']

    # Mark profile as complete if name and avatar are set
    if user.name and user.avatar:
        user.is_profile_complete = True

    db.session.commit()

    return jsonify({
        'id': user.id,
        'mobile_number': user.mobile_number,
        'name': user.name,
        'avatar': user.avatar,
        'role': user.role,
        'is_profile_complete': user.is_profile_complete
    })

@bp.route('/complete-profile', methods=['POST'])
def complete_profile():
    """Complete user profile with username and avatar"""
    data = request.get_json() or {}

    # Log the received data for debugging
    print(f"Received profile completion data: {data}")

    # Check if mobile_number is provided
    if 'mobile_number' not in data or not data['mobile_number']:
        return jsonify({'error': 'Mobile number is required'}), 400

    # Find the user by mobile number
    user = User.get_by_mobile(data['mobile_number'])

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Validate required fields
    if 'name' not in data or not data['name']:
        return jsonify({'error': 'Name is required'}), 400
    if 'avatar' not in data or not data['avatar']:
        return jsonify({'error': 'Avatar is required'}), 400

    # Update user profile
    user.name = data['name']

    # Handle avatar path
    avatar = data['avatar']

    # Validate that the avatar is one of the expected filenames
    valid_avatars = ['engg1.jpg', 'engg2.jpg', 'doc.jpg', 'index.png']
    if avatar not in valid_avatars:
        print(f"Warning: Unexpected avatar filename: {avatar}")

    # Store the filename directly - the frontend will handle the path resolution
    user.avatar = avatar

    # Log the avatar being saved
    print(f"Saving avatar: {avatar} for user {user.mobile_number}")
    user.is_profile_complete = True

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Profile completed successfully',
        'user': {
            'id': user.id,
            'mobile_number': user.mobile_number,
            'name': user.name,
            'avatar': user.avatar,
            'role': user.role,
            'is_profile_complete': user.is_profile_complete
        }
    })
