from flask import Blueprint, request, jsonify
from bson import ObjectId
from middleware.auth import token_required, role_required

questions_bp = Blueprint('questions', __name__)

def init_questions_routes(mongo):
    from models.question import QuestionModel
    question_model = QuestionModel(mongo)
    
    @questions_bp.route('/', methods=['GET'])
    def get_questions():
        """Get all questions with filters"""
        search = request.args.get('search')
        subject = request.args.get('subject')
        tags = request.args.get('tags')
        sort = request.args.get('sort', 'newest')
        
        questions = question_model.get_all_questions(
            search=search,
            subject=subject,
            tags=tags,
            sort=sort
        )
        
        # Convert ObjectId to string for JSON serialization
        for q in questions:
            q['_id'] = str(q['_id'])
            q['author'] = str(q['author'])
            q['author_info']['_id'] = str(q['author_info']['_id'])
        
        return jsonify(questions), 200
    
    @questions_bp.route('/<question_id>', methods=['GET'])
    def get_question(question_id):
        """Get single question with its answers"""
        try:
            question = question_model.find_by_id(question_id)
            if not question:
                return jsonify({'message': 'Question not found'}), 404
            
            # Get answers for this question
            from models.answer import AnswerModel
            answer_model = AnswerModel(mongo)
            answers = answer_model.get_answers_by_question(question_id)
            
            # Convert ObjectId to string
            question['_id'] = str(question['_id'])
            question['author'] = str(question['author'])
            question['author_info']['_id'] = str(question['author_info']['_id'])
            
            for answer in answers:
                answer['_id'] = str(answer['_id'])
                answer['author'] = str(answer['author'])
                answer['author_info']['_id'] = str(answer['author_info']['_id'])
            
            return jsonify({
                'question': question,
                'answers': answers
            }), 200
            
        except Exception as e:
            return jsonify({'message': str(e)}), 400
    
    @questions_bp.route('/', methods=['POST'])
    @token_required
    @role_required(['student'])
    def create_question():
        """Create a new question (students only)"""
        data = request.get_json()
        
        required_fields = ['title', 'description', 'subject']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} is required'}), 400
        
        tags = data.get('tags', '')
        
        question = question_model.create_question(
            title=data['title'],
            description=data['description'],
            tags=tags,
            subject=data['subject'],
            author_id=request.user_id
        )
        
        question['_id'] = str(question['_id'])
        question['author'] = str(question['author'])
        
        return jsonify(question), 201
    
    @questions_bp.route('/<question_id>', methods=['PUT'])
    @token_required
    def update_question(question_id):
        """Update question (owner only)"""
        question = question_model.find_by_id(question_id)
        
        if not question:
            return jsonify({'message': 'Question not found'}), 404
        
        if str(question['author']) != request.user_id:
            return jsonify({'message': 'Not authorized'}), 403
        
        data = request.get_json()
        update_data = {}
        
        allowed_fields = ['title', 'description', 'tags', 'subject']
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        if update_data:
            question_model.update_question(question_id, update_data)
        
        return jsonify({'message': 'Question updated successfully'}), 200
    
    @questions_bp.route('/<question_id>', methods=['DELETE'])
    @token_required
    def delete_question(question_id):
        """Delete question (owner only)"""
        question = question_model.find_by_id(question_id)
        
        if not question:
            return jsonify({'message': 'Question not found'}), 404
        
        if str(question['author']) != request.user_id:
            return jsonify({'message': 'Not authorized'}), 403
        
        # Delete all answers for this question
        from models.answer import AnswerModel
        answer_model = AnswerModel(mongo)
        answer_model.delete_answers_by_question(question_id)
        
        # Delete the question
        question_model.delete_question(question_id)
        
        return jsonify({'message': 'Question deleted successfully'}), 200
    
    return questions_bp
