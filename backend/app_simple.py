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

# Configuration
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/classroom_doubt')
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'secretkey')

# CORS - Allow all for testing
CORS(app, resources={r"/api/*": {"origins": "*"}})

# MongoDB Connection
try:
    mongo = PyMongo(app)
    mongo.db.command('ping')
    print("✅ MongoDB connected!")
except Exception as e:
    print(f"❌ MongoDB error: {e}")
    mongo = None

# Helper function to convert ObjectId to string
def serialize_doc(doc):
    if doc is None:
        return None
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    if 'author' in doc and isinstance(doc['author'], ObjectId):
        doc['author'] = str(doc['author'])
    if 'questionId' in doc and isinstance(doc['questionId'], ObjectId):
        doc['questionId'] = str(doc['questionId'])
    return doc

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK', 'message': 'Server is running'}), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    if not mongo:
        return jsonify({'message': 'Database error'}), 500
    try:
        data = request.json
        if mongo.db.users.find_one({'email': data['email']}):
            return jsonify({'message': 'User exists'}), 400
        
        hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        user = {
            'name': data['name'],
            'email': data['email'],
            'password': hashed,
            'role': data.get('role', 'student'),
            'reputation': 0,
            'createdAt': datetime.utcnow()
        }
        result = mongo.db.users.insert_one(user)
        token = jwt.encode({'user_id': str(result.inserted_id), 'exp': datetime.utcnow() + timedelta(days=7)}, app.config['SECRET_KEY'])
        return jsonify({'token': token, 'user': {'id': str(result.inserted_id), 'name': user['name'], 'email': user['email'], 'role': user['role']}}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    if not mongo:
        return jsonify({'message': 'Database error'}), 500
    try:
        data = request.json
        user = mongo.db.users.find_one({'email': data['email']})
        if not user or not bcrypt.checkpw(data['password'].encode(), user['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        token = jwt.encode({'user_id': str(user['_id']), 'exp': datetime.utcnow() + timedelta(days=7)}, app.config['SECRET_KEY'])
        return jsonify({'token': token, 'user': {'id': str(user['_id']), 'name': user['name'], 'email': user['email'], 'role': user['role']}}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/questions', methods=['GET'])
def get_questions():
    if not mongo:
        return jsonify([]), 200
    try:
        questions = list(mongo.db.questions.find().sort('createdAt', -1).limit(20))
        # Serialize each question
        for q in questions:
            q['_id'] = str(q['_id'])
            if 'author' in q and isinstance(q['author'], ObjectId):
                q['author'] = str(q['author'])
        return jsonify(questions), 200
    except Exception as e:
        print(f"Error in get_questions: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/questions', methods=['POST'])
def create_question():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({'message': 'Auth required'}), 401
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        body = request.json
        question = {
            'title': body['title'],
            'description': body['description'],
            'subject': body['subject'],
            'tags': body.get('tags', '').split(',') if body.get('tags') else [],
            'author': ObjectId(data['user_id']),
            'votes': 0,
            'createdAt': datetime.utcnow()
        }
        result = mongo.db.questions.insert_one(question)
        return jsonify({'_id': str(result.inserted_id), 'message': 'Question created'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 401

@app.route('/api/questions/<question_id>', methods=['GET'])
def get_question(question_id):
    if not mongo:
        return jsonify({'message': 'Database error'}), 500
    try:
        question = mongo.db.questions.find_one({'_id': ObjectId(question_id)})
        if not question:
            return jsonify({'message': 'Question not found'}), 404
        question = serialize_doc(question)
        return jsonify(question), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/')
def home():
    return jsonify({'message': 'API is running 🚀'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
