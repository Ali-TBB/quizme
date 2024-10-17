from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os

from src.quiz_generate import QuizGenerate  # Import your QuizGenerate class

app = Flask(__name__)

# Configure the upload folder and allowed file types
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
ALLOWED_TYPES = {'true/false', 'multiple-choice one-answer', 'multiple-choice multiple-answers', 'mixed'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

quizzes_store_ids = []

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

    # Check if a file was uploaded and handle it if present
    file = request.files.get('file')  # Use .get() to avoid KeyError if no file is provided

    attachments = []

    # If a file is provided, process it
    if file and file.filename != '':
        if allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            attachments.append(file_path)  # Add the file path to attachments
        else:
            return jsonify({"error": "Invalid file type."}), 400

    # Fetch the form data (not JSON since it's a multipart form)
    data = request.form
    difficulty = data.get('difficulty')

    # Validate difficulty
    if difficulty not in ['easy', 'medium', 'hard']:
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
        "quiz": generated_quiz.id
    }), 201


@app.route('/quizzes', methods=['GET'])
def get_quizzes():
    return jsonify(quizzes_store_ids), 200

def start():
    app.run(host='127.0.0.1', port=5000, debug=False)
