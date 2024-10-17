import questionary

from models.answer import Answer
from models.options import Options
from src.quiz_generate import QuizGenerate
from src.correction import Correction
from models.questions import Questions
from utils.env import Env
def main_menu():
    
    """Main menu for the quiz application."""
    choice = questionary.select(
        "What would you like to do?",
        choices=["Generate Quiz", "Exit"]
    ).ask()

    return choice

def generate_quiz():
    """Prompt the user to generate a quiz."""
    difficulty = questionary.select(
        "Select the difficulty level:",
        choices=["easy", "medium", "hard", "mixed"]
    ).ask()
    number_of_questions = questionary.text("Enter the number of questions:").ask()
    topic_content = questionary.text("Enter the topic content (or leave blank):").ask() or None

    # Generate the quiz
    quiz_generator = QuizGenerate(difficulty, int(number_of_questions), "multiple-choice one-answer", topic_content)
    quiz = quiz_generator.start()

    return quiz

def ask_questions(quiz):
    """
    Ask the user the questions generated, display options, and store their selected answer IDs.
    
    Returns:
        list: A list of tuples containing the question, the selected answer's ID, and the quiz ID.
    """
    user_answers = []  # List to store user answers as (question, selected_option_id, quiz_id)
    
    # Fetch all questions for the quiz
    questions = Questions.all(where="quiz_id = ?", params=(quiz.id,))
    
    for question in questions:
        question_text = question.content
        options_ids = question.options_ids
        
        # Fetch all options for the current question
        placeholders = ','.join('?' for _ in options_ids)  # Create SQL placeholders for the IN clause
        options = Options.all(where=f"id IN ({placeholders})", params=(tuple(options_ids)))
        
        # Display the question and options
        # Create a mapping between option text and option ID
        option_map = {option.option_text: option.id for option in options}
        
        # Ask the user to select an answer using the text, but store the ID
        answer_text = questionary.select(
            f"{question_text}",
            choices=list(option_map.keys())  # Display the option texts to the user
        ).ask()
        
        # Get the corresponding option ID based on the selected text
        selected_option_id = option_map[answer_text]
        
        # Collect the user answer with question ID and quiz ID
        user_answers.append((question.id, selected_option_id, quiz.id))
    
    return user_answers


def save_answers(user_answers):
    """Save user answers to the database."""
    for question_id, answer_id , quiz_id in user_answers:
        answer_model = Answer.create(
            id=None,  # Auto-incremented ID
            quiz_id=quiz_id,
            question_id=question_id,
            answer_ids=[answer_id],  # Assuming the answer is stored as a list
            correct_ids=[],  # Set this based on your logic
        )
    print("Answers saved successfully!")

def check_answers(quiz_id):
    """Check the user's answers against the correct answers."""
    correction = Correction(quiz_id)
    results = correction.correct_quiz()

    # Print the results and score
    print(f"Score: {results['score']}/100")
    for result in results['results']:
        print(f"Question ID: {result['question_id']}, User Answer: {result['user_answer']}, "
              f"Correct Answer: {result['correct_answer']}, Is Correct: {result['is_correct']}")

def main():
    """Main loop to run the application."""
    while True:
        choice = main_menu()
        
        if choice == "Generate Quiz":
            quiz = generate_quiz()  # Generate the quiz and get the data
            user_answers = ask_questions(quiz)  # Ask the questions and get user answers
            save_answers(user_answers)  # Save the answers to the database
            check_answers(quiz.id)  # Check answers and display the score
        elif choice == "Exit":
            print("Exiting the application.")
            break
        else:
            print("Invalid choice, please try again.")
