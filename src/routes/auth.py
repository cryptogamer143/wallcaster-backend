from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from src.models.user import db, User

auth_bp = Blueprint('auth', __name__)

# Initialize JWT in your app (in app.py):
# app.config["JWT_SECRET_KEY"] = "super-secret-key"  # change in production
# jwt = JWTManager(app)


# ---------------- LOGIN ---------------- #
@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if user.status != 'active':
                return jsonify({'error': 'Account is suspended or banned'}), 403
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Create JWT token (valid for 1 day)
            access_token = create_access_token(
                identity={'id': user.id, 'role': user.role},
                expires_delta=timedelta(days=1)
            )
            
            return jsonify({
                'message': 'Login successful',
                'token': access_token,
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ---------------- REGISTER ---------------- #
@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        
        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 409
        
        # Assign first registered user as admin
        role = "admin" if User.query.count() == 0 else "user"
        
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ---------------- GET CURRENT USER ---------------- #
@auth_bp.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        identity = get_jwt_identity()  # {'id': user_id, 'role': user_role}
        user = User.query.get(identity['id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ---------------- CHANGE PASSWORD ---------------- #
@auth_bp.route('/api/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        identity = get_jwt_identity()
        user = User.query.get(identity['id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Current and new passwords are required'}), 400
        
        if not user.check_password(current_password):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
