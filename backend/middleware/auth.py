from functools import wraps
from flask import request, jsonify
import jwt
from config import Config
from bson import ObjectId

def token_required(f):
    """Decorator to protect routes that require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Decode token
            data = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
            from app import mongo
            user = mongo.db.users.find_one({'_id': ObjectId(data['user_id'])})
            
            if not user:
                return jsonify({'message': 'User not found!'}), 401
            
            request.user = user
            request.user_id = str(user['_id'])
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def role_required(allowed_roles):
    """Decorator to check user role"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(request, 'user'):
                return jsonify({'message': 'Authentication required!'}), 401
            
            if request.user['role'] not in allowed_roles:
                return jsonify({'message': f'Access denied. {allowed_roles} only!'}), 403
            
            return f(*args, **kwargs)
        return decorated
    return decorator
