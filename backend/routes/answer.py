from flask import Blueprint, request, jsonify
from bson import ObjectId
from middleware.auth import token_required

answers_bp = Blueprint('answers', __name__)

def init_answers_routes(mongo):
    from models.answer import AnswerModel
    from models.question import QuestionModel
    from models.user import UserModel
    
    answer_model = AnswerModel(mongo)
    question_model = QuestionModel(mongo)
    user_model = UserModel(mongo)
    
    @answers_bp.route('/<question_id>', methods=['POST'])
    @token_required
    def add_answer(question_id):
        """Add an answer to a question"""
        data = request.get_json()
        
        if not data.get('content'):
            return jsonify({'message': 'Content is required'}), 400
        
        # Check if question exists
        question = question_model.find_by_id(question_id)
        if not question:
            return jsonify({'message': 'Question not found'}), 404
        
        # Create answer
        answer = answer_model.create_answer(
            question_id=question_id,
            author_id=request.user_id,
            content=data['content']
        )
        
        # Increase reputation for answering (+5)
        user_model.update_reputation(request.user_id, 5)
        
        answer['_id'] = str(answer['_id'])
        answer['author'] = str(answer['author'])
        answer['author_info']['_id'] = str(answer['author_info']['_id'])
        
        return jsonify(answer), 201
    
    @answers_bp.route('/<answer_id>/vote', methods=['POST'])
    @token_required
    def vote_answer(answer_id):
        """Vote on an answer"""
        data = request.get_json()
        vote_type = data.get('vote_type')
        
        if vote_type not in ['up', 'down']:
            return jsonify({'message': 'vote_type must be "up" or "down"'}), 400
        
        answer = answer_model.vote_answer(answer_id, request.user_id, vote_type)
        
        if not answer:
            return jsonify({'message': 'Answer not found'}), 404
        
        # Update reputation of answer author
        vote_value = 10 if vote_type == 'up' else -5
        user_model.update_reputation(answer['author'], vote_value)
        
        return jsonify({
            'message': 'Vote recorded',
            'votes': answer['votes']
        }), 200
    
    @answers_bp.route('/<answer_id>/accept', methods=['PUT'])
    @token_required
    def accept_answer(answer_id):
        """Accept an answer (question owner only)"""
        answer = answer_model.find_by_id(answer_id)
        
        if not answer:
            return jsonify({'message': 'Answer not found'}), 404
        
        # Check if current user is the question owner
        question = question_model.find_by_id(answer['questionId'])
        
        if str(question['author']) != request.user_id:
            return jsonify({'message': 'Only the question owner can accept an answer'}), 403
        
        # Set accepted answer
        question_model.set_accepted_answer(answer['questionId'], answer_id)
        
        # Award reputation to answer author (+15)
        user_model.update_reputation(answer['author'], 15)
        
        return jsonify({
            'message': 'Answer accepted successfully',
            'acceptedAnswer': answer_id
        }), 200
    
    return answers_bp
