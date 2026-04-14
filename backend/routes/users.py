from flask import Blueprint, request, jsonify
from bson import ObjectId
from middleware.auth import token_required

users_bp = Blueprint('users', __name__)

def init_users_routes(mongo):
    from models.user import UserModel
    from models.question import QuestionModel
    from models.answer import AnswerModel
    
    user_model = UserModel(mongo)
    question_model = QuestionModel(mongo)
    answer_model = AnswerModel(mongo)
    
    @users_bp.route('/profile/<user_id>', methods=['GET'])
    def get_user_profile(user_id):
        """Get user profile with their questions and answers"""
        try:
            user = user_model.find_by_id(user_id)
            if not user:
                return jsonify({'message': 'User not found'}), 404
            
            # Get user's questions
            questions = list(mongo.db.questions.find({'author': ObjectId(user_id)}))
            for q in questions:
                q['_id'] = str(q['_id'])
            
            # Get user's answers
            answers = list(mongo.db.answers.find({'author': ObjectId(user_id)}))
            for a in answers:
                a['_id'] = str(a['_id'])
            
            return jsonify({
                'user': {
                    'id': str(user['_id']),
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role'],
                    'reputation': user['reputation'],
                    'createdAt': user['createdAt']
                },
                'questions': questions,
                'answers': answers
            }), 200
            
        except Exception as e:
            return jsonify({'message': str(e)}), 400
    
    @users_bp.route('/dashboard', methods=['GET'])
    @token_required
    def get_dashboard():
        """Get dashboard data for current user"""
        user_id = request.user_id
        
        # Get user's questions
        questions = list(mongo.db.questions.find({'author': ObjectId(user_id)}))
        
        # Count solved questions (those with acceptedAnswer)
        solved_count = sum(1 for q in questions if q.get('acceptedAnswer'))
        
        # Get user's answers
        answers = list(mongo.db.answers.find({'author': ObjectId(user_id)}))
        
        dashboard_data = {
            'user': {
                'id': str(request.user['_id']),
                'name': request.user['name'],
                'role': request.user['role'],
                'reputation': request.user['reputation']
            },
            'stats': {
                'totalQuestions': len(questions),
                'totalAnswers': len(answers),
                'solvedQuestions': solved_count,
                'reputation': request.user['reputation']
            },
            'recentQuestions': [
                {
                    '_id': str(q['_id']),
                    'title': q['title'],
                    'createdAt': q['createdAt'],
                    'hasAcceptedAnswer': bool(q.get('acceptedAnswer'))
                }
                for q in sorted(questions, key=lambda x: x['createdAt'], reverse=True)[:5]
            ],
            'recentAnswers': [
                {
                    '_id': str(a['_id']),
                    'content': a['content'][:100],
                    'createdAt': a['createdAt']
                }
                for a in sorted(answers, key=lambda x: x['createdAt'], reverse=True)[:5]
            ]
        }
        
        return jsonify(dashboard_data), 200
    
    return users_bp
