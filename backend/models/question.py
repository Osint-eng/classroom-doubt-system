from datetime import datetime
from bson import ObjectId

class QuestionModel:
    def __init__(self, mongo):
        self.collection = mongo.db.questions
        self.mongo = mongo
    
    def create_question(self, title, description, tags, subject, author_id):
        """Create a new question"""
        question = {
            'title': title,
            'description': description,
            'tags': [tag.strip() for tag in tags.split(',')],
            'subject': subject,
            'author': ObjectId(author_id),
            'votes': 0,
            'acceptedAnswer': None,
            'createdAt': datetime.utcnow()
        }
        
        result = self.collection.insert_one(question)
        return self.find_by_id(result.inserted_id)
    
    def find_by_id(self, question_id):
        """Find question by ID"""
        question = self.collection.aggregate([
            {'$match': {'_id': ObjectId(question_id)}},
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
        
        result = list(question)
        return result[0] if result else None
    
    def get_all_questions(self, search=None, subject=None, tags=None, sort='newest'):
        """Get all questions with filters"""
        match_stage = {}
        
        # Search functionality
        if search:
            match_stage['$or'] = [
                {'title': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}}
            ]
        
        # Filter by subject
        if subject:
            match_stage['subject'] = subject
        
        # Filter by tags
        if tags:
            tag_list = tags.split(',')
            match_stage['tags'] = {'$in': tag_list}
        
        # Filter unanswered
        if sort == 'unanswered':
            match_stage['acceptedAnswer'] = None
        
        pipeline = []
        if match_stage:
            pipeline.append({'$match': match_stage})
        
        pipeline.extend([
            {'$lookup': {
                'from': 'users',
                'localField': 'author',
                'foreignField': '_id',
                'as': 'author_info'
            }},
            {'$unwind': '$author_info'},
            {'$lookup': {
                'from': 'answers',
                'localField': '_id',
                'foreignField': 'questionId',
                'as': 'answers'
            }},
            {'$project': {
                'password': 0,
                'author_info.password': 0
            }}
        ])
        
        # Sorting
        if sort == 'newest':
            pipeline.append({'$sort': {'createdAt': -1}})
        elif sort == 'mostVotes':
            pipeline.append({'$sort': {'votes': -1}})
        elif sort == 'unanswered':
            pipeline.append({'$sort': {'createdAt': -1}})
        
        return list(self.collection.aggregate(pipeline))
    
    def update_question(self, question_id, update_data):
        """Update question"""
        self.collection.update_one(
            {'_id': ObjectId(question_id)},
            {'$set': update_data}
        )
    
    def delete_question(self, question_id):
        """Delete question"""
        self.collection.delete_one({'_id': ObjectId(question_id)})
    
    def increment_votes(self, question_id, increment=1):
        """Increment question votes"""
        self.collection.update_one(
            {'_id': ObjectId(question_id)},
            {'$inc': {'votes': increment}}
        )
    
    def set_accepted_answer(self, question_id, answer_id):
        """Set accepted answer for question"""
        self.collection.update_one(
            {'_id': ObjectId(question_id)},
            {'$set': {'acceptedAnswer': ObjectId(answer_id)}}
        )
