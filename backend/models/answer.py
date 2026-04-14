from datetime import datetime
from bson import ObjectId

class AnswerModel:
    def __init__(self, mongo):
        self.collection = mongo.db.answers
        self.mongo = mongo
    
    def create_answer(self, question_id, author_id, content):
        """Create a new answer"""
        answer = {
            'questionId': ObjectId(question_id),
            'author': ObjectId(author_id),
            'content': content,
            'votes': 0,
            'voters': [],  # List of {user_id, vote_type}
            'createdAt': datetime.utcnow()
        }
        
        result = self.collection.insert_one(answer)
        return self.find_by_id(result.inserted_id)
    
    def find_by_id(self, answer_id):
        """Find answer by ID"""
        answer = self.collection.aggregate([
            {'$match': {'_id': ObjectId(answer_id)}},
            {'$lookup': {
                'from': 'users',
                'localField': 'author',
                'foreignField': '_id',
                'as': 'author_info'
            }},
            {'$unwind': '$author_info'},
            {'$project': {
                'password': 0,
                'author_info.password': 0
            }}
        ])
        
        result = list(answer)
        return result[0] if result else None
    
    def get_answers_by_question(self, question_id):
        """Get all answers for a question"""
        answers = self.collection.aggregate([
            {'$match': {'questionId': ObjectId(question_id)}},
            {'$lookup': {
                'from': 'users',
                'localField': 'author',
                'foreignField': '_id',
                'as': 'author_info'
            }},
            {'$unwind': '$author_info'},
            {'$project': {
                'password': 0,
                'author_info.password': 0
            }},
            {'$sort': {'votes': -1, 'createdAt': 1}}
        ])
        
        return list(answers)
    
    def vote_answer(self, answer_id, user_id, vote_type):
        """Vote on an answer (upvote/downvote)"""
        answer = self.collection.find_one({'_id': ObjectId(answer_id)})
        
        if not answer:
            return None
        
        # Check if user already voted
        existing_vote = None
        for voter in answer.get('voters', []):
            if voter['user_id'] == str(user_id):
                existing_vote = voter
                break
        
        vote_value = 1 if vote_type == 'up' else -1
        
        if existing_vote:
            # Remove old vote effect
            old_value = 1 if existing_vote['vote_type'] == 'up' else -1
            self.collection.update_one(
                {'_id': ObjectId(answer_id)},
                {'$inc': {'votes': -old_value}}
            )
            # Remove from voters list
            self.collection.update_one(
                {'_id': ObjectId(answer_id)},
                {'$pull': {'voters': {'user_id': str(user_id)}}}
            )
        
        # Add new vote
        self.collection.update_one(
            {'_id': ObjectId(answer_id)},
            {
                '$inc': {'votes': vote_value},
                '$push': {'voters': {'user_id': str(user_id), 'vote_type': vote_type}}
            }
        )
        
        return self.find_by_id(answer_id)
    
    def delete_answers_by_question(self, question_id):
        """Delete all answers for a question"""
        self.collection.delete_many({'questionId': ObjectId(question_id)})
