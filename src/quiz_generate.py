import json


from src.data_types.quiz_generate import QuizGenerateDataType
from src.base_model import BaseModel
from models.quizzes import Quizzes
from models.questions import Questions
from models.options import Options
from models.dataset import Dataset


class QuizGenerate(BaseModel):
    """
    Class to handle generating and saving quizzes to the database.
    """
    backup_name = "quiz_train"
    data_type = QuizGenerateDataType

    def __init__(self, difficulty: str, number_of_questions: int, question_type: str, topic_content: str = None, attachments: list = None):
        """
        Initializes a new instance for generating quizzes.

        Args:
            difficulty (str): The difficulty level of the quiz (e.g., 'easy', 'medium', 'hard').
            number_of_questions (int): The total number of questions to generate.
            question_type (str): The type of questions to include in the quiz (e.g., 'multiple-choice', 'true/false').
            topic_content (str, optional): The subject matter or topic for the quiz content. Defaults to None.
            attachments (list, optional): A list of attachments related to the topic. Defaults to None.
        """
        super().__init__(dataset=Dataset.find(1))
        self.difficulty = difficulty
        self.number_of_questions = number_of_questions
        self.question_type = question_type
        self.topic_content = topic_content
        self.attachments = attachments if attachments is not None else []

        # Constructing the input_data based on provided content and attachments
        if self.topic_content:
            topic_info = f"Topic: {self.topic_content}"
        else:
            topic_info = "Topic: Depend on the file"

        if self.attachments:
            attachment_info = f"\nAttachments: {', '.join([self.attachments[i].path for i in range(len(self.attachments))])}"
        else:
            attachment_info = ""

        self.input_data = (
            f"Please generate a quiz based on the following criteria:\n"
            f"- {topic_info}\n"
            f"- Difficulty Level: {self.difficulty}\n"
            f"- Number of Questions: {self.number_of_questions}\n"
            f"- Question Type: {self.question_type}{attachment_info}\n"
            f"The quiz should include a variety of questions that align with the specified difficulty level."
        )

    def save_quiz_to_db(self, quiz_data: str):
        """
        Saves the generated quiz questions and options into the database.

        Args:
            quiz_json (str): The JSON string containing the quiz details.
            quiz_id (int): The ID of the quiz to associate the questions with.
        """
        quiz_id = Quizzes.nextId()
        quiz_data = json.loads(quiz_data)
        question_count = quiz_data.get("question_count", 0)
        questions = quiz_data.get("questions", [])

        for question_data in questions:
            # Extract question details
            content = question_data.get("question", "")
            difficulty = question_data.get("difficulty", "easy")
            options_list = question_data.get("options", [])
            correct_answers = question_data.get("corrected_answer", [])

            # Insert the question into the database
            question = Questions.create(
                id=None,  # ID will be auto-generated
                quiz_id=quiz_id,
                question_type="multiple-answer" if len(correct_answers) > 1 else "one-answer",
                difficulty=difficulty,
                content=content,
                options_ids="",  # Will be populated later
                correct_option_id=None,  # Will be set after creating options
            )
            question_id = question.id # get its ID

            # Insert options and map them to the question
            option_ids = []
            correct_option_id = None
            for option_text in options_list:
                is_correct = option_text in correct_answers

                option = Options.create(
                    id=None,  # ID will be auto-generated
                    question_id=question_id,
                    option_text=option_text,
                )
                option_id = option.id  # get its ID
                option_ids.append(option_id)

                if is_correct:
                    correct_option_id = option_id  # Save the correct option ID

            # Update the question with correct option ID and options IDs
            question.options_ids = option_ids
            question.correct_option_id = correct_option_id
            question.update()  # Update the question with the option IDs and correct option
        quiz = Quizzes.create(
            id = quiz_id,
            topic=self.topic_content,
            difficulty=self.difficulty,
            number_of_questions = self.number_of_questions
        )
        print(f"Successfully saved {question_count} questions and their options to the database.")
        return quiz

    def start(self):
        """
        Starts the quiz generation process by sending the initial message.
        """
        output = self.send_message(self.input_data, self.attachments)
        self.update_history(self.input_data, output, self.attachments)
        return self.save_quiz_to_db(output)
