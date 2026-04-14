from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import jwt
import bcrypt
from datetime import datetime, timedelta
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/classroom_doubt')
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'secretkey')
CORS(app)

mongo = PyMongo(app)

# Helper function to convert ObjectId to string
def serialize_doc(doc):
    if doc:
        doc['_id'] = str(doc['_id'])
    return doc

# Register endpoint
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'student')
        
        # Check if user exists
        if mongo.db.users.find_one({'email': email}):
            return jsonify({'message': 'User already exists'}), 400
        
        # Hash password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user
        user = {
            'name': name,
            'email': email,
            'password': hashed,
            'role': role,
            'reputation': 0,
            'createdAt': datetime.utcnow()
        }
        
        result = mongo.db.users.insert_one(user)
        
        # Generate token
        token = jwt.encode({
            'user_id': str(result.inserted_id),
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user': {
                'id': str(result.inserted_id),
                'name': name,
                'email': email,
                'role': role,
                'reputation': 0
            }
        }), 201
        
    except Exception as e:
        print(f"Error in register: {e}")
        return jsonify({'message': str(e)}), 500

# Login endpoint
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = mongo.db.users.find_one({'email': email})
        if not user:
            return jsonify({'message': 'Invalid credentials'}), 401
        
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            token = jwt.encode({
                'user_id': str(user['_id']),
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user': {
                    'id': str(user['_id']),
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role'],
                    'reputation': user.get('reputation', 0)
                }
            }), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        print(f"Error in login: {e}")
        return jsonify({'message': str(e)}), 500

# Get current user
@app.route('/api/auth/me', methods=['GET'])
def get_me():
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'message': 'No token'}), 401
        
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user = mongo.db.users.find_one({'_id': ObjectId(data['user_id'])})
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify({
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'role': user['role'],
            'reputation': user.get('reputation', 0)
        }), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 401

# Get questions endpoint
@app.route('/api/questions', methods=['GET'])
def get_questions():
    questions = list(mongo.db.questions.find().sort('createdAt', -1).limit(20))
    for q in questions:
        q['_id'] = str(q['_id'])
        if 'author' in q:
            author = mongo.db.users.find_one({'_id': q['author']})
            q['author_info'] = {'name': author['name'] if author else 'Unknown'}
            q['author'] = str(q['author'])
    return jsonify(questions), 200

# Create question endpoint
@app.route('/api/questions', methods=['POST'])
def create_question():
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        
        body = request.get_json()
        question = {
            'title': body.get('title'),
            'description': body.get('description'),
            'subject': body.get('subject'),
            'tags': body.get('tags', '').split(',') if body.get('tags') else [],
            'author': ObjectId(data['user_id']),
            'votes': 0,
            'createdAt': datetime.utcnow()
        }
        
        result = mongo.db.questions.insert_one(question)
        return jsonify({'_id': str(result.inserted_id), **body}), 201
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': str(e)}), 500
@app.route('/')
def home():
    return jsonify({
        'message': 'Classroom Doubt System API',
        'endpoints': {
            'register': '/api/auth/register',
            'login': '/api/auth/login',
            'questions': '/api/questions',
            'create_question': '/api/questions (POST)'
        }
    }), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.route('/')
def home():
    return jsonify({
        'message': 'Classroom Doubt System API',
        'endpoints': {
            'register': '/api/auth/register',
            'login': '/api/auth/login',
            'questions': '/api/questions',
            'create_question': '/api/questions (POST)'
        }
    }), 200
