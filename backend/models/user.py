from datetime import datetime
from flask_pymongo import PyMongo
from bcrypt import hashpw, gensalt, checkpw

class UserModel:
    def __init__(self, mongo):
        self.collection = mongo.db.users
    
    def create_user(self, name, email, password, role='student'):
        """Create a new user"""
        existing = self.collection.find_one({'email': email})
        if existing:
            return None
        
        hashed = hashpw(password.encode('utf-8'), gensalt())
        
        user = {
            'name': name,
            'email': email,
            'password': hashed,
            'role': role,
            'reputation': 0,
            'createdAt': datetime.utcnow()
        }
        
        result = self.collection.insert_one(user)
        user['_id'] = result.inserted_id
        return user
    
    def authenticate(self, email, password):
        """Authenticate user"""
        user = self.collection.find_one({'email': email})
        if user and checkpw(password.encode('utf-8'), user['password']):
            return user
        return None
    
    def find_by_id(self, user_id):
        """Find user by ID"""
        from bson import ObjectId
        return self.collection.find_one({'_id': ObjectId(user_id)})
    
    def find_by_email(self, email):
        """Find user by email"""
        return self.collection.find_one({'email': email})
    
    def update_reputation(self, user_id, points):
        """Update user reputation"""
        from bson import ObjectId
        self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$inc': {'reputation': points}}
        )
    
    def get_user_stats(self, user_id):
        """Get user statistics (questions asked, answers given)"""
        from bson import ObjectId
        user_id_obj = ObjectId(user_id)
        
        questions_count = self.mongo.db.questions.count_documents({'author': user_id_obj})
        answers_count = self.mongo.db.answers.count_documents({'author': user_id_obj})
        
        return {
            'questionsCount': questions_count,
            'answersCount': answers_count
        }
