from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
from config import Config
from middleware.auth import token_required

auth_bp = Blueprint('auth', __name__)

def init_auth_routes(mongo):
    from models.user import UserModel
    user_model = UserModel(mongo)
    
    @auth_bp.route('/register', methods=['POST'])
    def register():
        """Register a new user"""
        data = request.get_json()
        
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} is required'}), 400
        
        role = data.get('role', 'student')
        if role not in ['student', 'teacher']:
            return jsonify({'message': 'Role must be student or teacher'}), 400
        
        user = user_model.create_user(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            role=role
        )
        
        if not user:
            return jsonify({'message': 'User already exists'}), 400
        
        # Generate token
        token = jwt.encode({
            'user_id': str(user['_id']),
            'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
        }, Config.JWT_SECRET, algorithm='HS256')
        
        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'reputation': user['reputation']
            }
        }), 201
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        """Login user"""
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email and password required'}), 400
        
        user = user_model.authenticate(data['email'], data['password'])
        
        if not user:
            return jsonify({'message': 'Invalid credentials'}), 401
        
        # Generate token
        token = jwt.encode({
            'user_id': str(user['_id']),
            'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
        }, Config.JWT_SECRET, algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'reputation': user['reputation']
            }
        }), 200
    
    @auth_bp.route('/me', methods=['GET'])
    @token_required
    def get_me():
        """Get current user info"""
        user = {
            'id': str(request.user['_id']),
            'name': request.user['name'],
            'email': request.user['email'],
            'role': request.user['role'],
            'reputation': request.user['reputation'],
            'createdAt': request.user['createdAt']
        }
        return jsonify(user), 200
    
    return auth_bp
