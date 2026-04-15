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

# Force print to flush immediately
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

# Configure CORS - Allow Netlify frontend
CORS(app, origins=[
    'https://classroom-dought-system.netlify.app',
    'https://classroom-doubt-system.netlify.app',
    'http://localhost:3000'
], supports_credentials=True)
# Connect to MongoDB
try:
    mongo = PyMongo(app)
    # Test connection
    mongo.db.command('ping')
    print("=== ✅ MongoDB connected successfully! ===", flush=True)
except Exception as e:
    print(f"=== ❌ MongoDB connection error: {e} ===", flush=True)
    mongo = None

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK', 'message': 'Server is running'}), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    print("=== Register endpoint called ===", flush=True)
    
    if mongo is None:
        print("=== ERROR: mongo is None! ===", flush=True)
        return jsonify({'message': 'Database connection error'}), 500
    
    try:
        data = request.get_json()
        print(f"=== Register data: {data}", flush=True)
        
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

@app.route('/api/auth/login', methods=['POST'])
def login():
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

@app.route('/api/questions', methods=['GET'])
def get_questions():
    if mongo is None:
        return jsonify([]), 200
    
    try:
        questions = list(mongo.db.questions.find().sort('createdAt', -1).limit(20))
        for q in questions:
            q['_id'] = str(q['_id'])
        return jsonify(questions), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/')
def home():
    return jsonify({'message': 'API is running 🚀'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
