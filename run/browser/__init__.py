import json
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os


import utils
from models.attachment import Attachment
from models.answer import Answer
from models.quizzes import Quizzes
from src.correction import Correction
from src.quiz_generate import QuizGenerate
from utils.env import Env  

app = Flask(__name__)

# Configure the upload folder and allowed file types
UPLOAD_FOLDER = 'run/browser/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_TYPES = {'true/false', 'multiple-choice one-answer', 'multiple-choice multiple-answers', 'mixed'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

quizzes_store_ids = []

def get_questions(quiz):
    questions = []
    for question in quiz.questions:
        questionJson = question.__dict__()
        questionJson.pop('correct_option_id')
        questionJson['options'] = [option.__dict__() for option in question.options]
        questions.append(questionJson)
    return questions

@app.route('/')
def index():
    """
    Serve the HTML page.
    """
    return render_template('index.html')

@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    """
    Endpoint to generate a quiz based on the provided form data and an optional file.
    """

    utils.Database.close()

    # Check if a file was uploaded and handle it if present
    file = request.files.get('file')  # Use .get() to avoid KeyError if no file is provided

    attachments = []

    # If a file is provided, process it
    if file and file.filename != '':
        if allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(Env.base_path, UPLOAD_FOLDER, filename)
            file.save(file_path)
            attachments.append(Attachment.create(
                id=None,
                mime_type=file.content_type,
                path=file_path
            ))  # Add the file path to attachments
        else:
            return jsonify({"error": "Invalid file type."}), 400

    # Fetch the form data (not JSON since it's a multipart form)
    data = request.form
    difficulty = data.get('difficulty')

    # Validate difficulty
    if difficulty not in ['easy', 'medium', 'hard', 'mixed']:
        return jsonify({"error": "Invalid difficulty level."}), 400

    number_of_questions = data.get('number_of_questions')

    # Validate number of questions
    if number_of_questions is None or not number_of_questions.isdigit() or int(number_of_questions) <= 0:
        return jsonify({"error": "Invalid number of questions."}), 400

    question_type = data.get('question_type')


    # Validate question type
    if question_type not in ALLOWED_TYPES:
        return jsonify({"error": "Invalid question type."}), 400

    topic_content = data.get('topic_content', None)

    # Create a quiz instance and pass the optional file attachments
    quiz_instance = QuizGenerate(difficulty, number_of_questions, question_type, topic_content, attachments)
    
    # Generate the quiz
    generated_quiz = quiz_instance.start()

    # Store the quiz (for this example, using an in-memory store)
    quizzes_store_ids.append(generated_quiz)

    return jsonify({
        "message": "Quiz generated successfully.",
        "quiz_id": generated_quiz.id,
        "questions": get_questions(generated_quiz)
    }), 201


@app.route('/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """
    Endpoint to retrieve a quiz by its ID.
    """

    utils.Database.close()

    quiz: Quizzes = Quizzes.find(quiz_id)

    if quiz is None:
        return jsonify({"error": "Quiz not found."}), 404

    return jsonify({
        "success": True,
        "message": "Quiz retrieved successfully.",
        "quiz_id": quiz.id,
        "topic_content": quiz.topic,
        "difficulty": quiz.difficulty,
        "number_of_questions": quiz.number_of_questions,
        "question_type": quiz.questions[0].question_type,
        "questions": get_questions(quiz)
    }), 200

@app.route('/quizzes', methods=['GET'])
def get_quizzes():
    return jsonify(quizzes_store_ids), 200

@app.route('/quizzes/<quiz_id>', methods=['POST'])
def check_answers(quiz_id):
    """
    Endpoint to check the user's answers for a quiz.
    """

    utils.Database.close()

    # Fetch the quiz
    quiz: Quizzes = Quizzes.find(quiz_id)

    if quiz is None:
        return jsonify({"error": "Quiz not found."}), 404

    # Fetch the user's answers
    user_answers = request.form.get('answers')

    user_answers = json.loads(user_answers) if user_answers else None

    if user_answers is None:
        return jsonify({"error": "No answers provided."}), 400

    questions = quiz.questions
    
    for question in questions:
        user_answers_ids = user_answers.get(str(question.id))
        user_answers_ids = [int(answer_id) for answer_id in user_answers_ids]

        if user_answers_ids is None:
            return jsonify({"error": "Missing answer for a question."}), 400
        elif not isinstance(user_answers_ids, list):
            return jsonify({"error": "Invalid answer format."}), 400
        
        Answer.create(
            id=None,
            quiz_id=quiz_id,
            question_id=question.id,
            answer_ids=user_answers_ids,
            correct_ids=[]
        )

    correction = Correction(quiz_id)
    results = correction.correct_quiz()
    
    return jsonify({
        "success": True,
        "message": "Answers checked successfully.",
        "results": results,
    }), 200

def start():
    app.run(host='127.0.0.1', port=5000, debug=False)
