import sys
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import jwt
import bcrypt
from datetime import datetime, timedelta
from bson import ObjectId
import os
from dotenv import load_dotenv

sys.stdout.reconfigure(line_buffering=True)
load_dotenv()

app = Flask(__name__)

# Get MongoDB URI from environment
mongo_uri = os.getenv('MONGO_URI')
print(f"=== DEBUG: MONGO_URI = {mongo_uri[:50] if mongo_uri else 'NOT SET'}...", flush=True)

if not mongo_uri:
    print("=== ERROR: MONGO_URI environment variable is not set! ===", flush=True)
    mongo_uri = 'mongodb://localhost:27017/classroom_doubt'

app.config['MONGO_URI'] = mongo_uri
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'secretkey')
print(f"=== DEBUG: JWT_SECRET = {app.config['SECRET_KEY'][:10]}...", flush=True)

# FIX: Proper CORS configuration - allow all origins for testing
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Connect to MongoDB
try:
    mongo = PyMongo(app)
    mongo.db.command('ping')
    print("=== ✅ MongoDB connected successfully! ===", flush=True)
except Exception as e:
    print(f"=== ❌ MongoDB connection error: {e} ===", flush=True)
    mongo = None

@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({'status': 'OK', 'message': 'Server is running'}), 200

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 200
    
    print("=== Register endpoint called ===", flush=True)
    
    if mongo is None:
        return jsonify({'message': 'Database connection error'}), 500
    
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
        
        print(f"=== User created successfully: {email}", flush=True)
        
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
        print(f"=== Register error: {e} ===", flush=True)
        return jsonify({'message': str(e)}), 500

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    
    if mongo is None:
        return jsonify({'message': 'Database connection error'}), 500
    
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
        print(f"=== Login error: {e} ===", flush=True)
        return jsonify({'message': str(e)}), 500

@app.route('/api/questions', methods=['GET', 'POST', 'OPTIONS'])
def handle_questions():
    if request.method == 'OPTIONS':
        return '', 200
    
    if request.method == 'GET':
        if mongo is None:
            return jsonify([]), 200
        try:
            questions = list(mongo.db.questions.find().sort('createdAt', -1).limit(20))
            for q in questions:
                q['_id'] = str(q['_id'])
            return jsonify(questions), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    
    elif request.method == 'POST':
        print("=== POST /api/questions called ===", flush=True)
        
        # Get token from header
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'message': 'Authentication required'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = data['user_id']
        except Exception as e:
            return jsonify({'message': f'Invalid token: {str(e)}'}), 401
        
        if mongo is None:
            return jsonify({'message': 'Database connection error'}), 500
        
        try:
            body = request.get_json()
            question = {
                'title': body.get('title'),
                'description': body.get('description'),
                'subject': body.get('subject'),
                'tags': body.get('tags', '').split(',') if body.get('tags') else [],
                'author': ObjectId(user_id),
                'votes': 0,
                'createdAt': datetime.utcnow()
            }
            
            result = mongo.db.questions.insert_one(question)
            return jsonify({
                '_id': str(result.inserted_id),
                'message': 'Question created successfully'
            }), 201
        except Exception as e:
            print(f"=== Create question error: {e} ===", flush=True)
            return jsonify({'message': str(e)}), 500

@app.route('/api/users/dashboard', methods=['GET', 'OPTIONS'])
def dashboard():
    if request.method == 'OPTIONS':
        return '', 200
    
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({'message': 'Authentication required'}), 401
    
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user = mongo.db.users.find_one({'_id': ObjectId(data['user_id'])})
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        questions = list(mongo.db.questions.find({'author': ObjectId(data['user_id'])}))
        answers = list(mongo.db.answers.find({'author': ObjectId(data['user_id'])}))
        
        return jsonify({
            'user': {'name': user['name'], 'email': user['email'], 'role': user['role'], 'reputation': user.get('reputation', 0)},
            'stats': {
                'totalQuestions': len(questions),
                'totalAnswers': len(answers),
                'solvedQuestions': sum(1 for q in questions if q.get('acceptedAnswer')),
                'reputation': user.get('reputation', 0)
            }
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/')
def home():
    return jsonify({'message': 'API is running 🚀'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
