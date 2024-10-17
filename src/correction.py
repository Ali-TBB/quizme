import json
from models.answer import Answer
from models.options import Options
from models.questions import Questions


class Correction:
    def __init__(self, quiz_id: int):
        """
        Initializes a new Correction object.

        Args:
            quiz_id (int): The ID of the quiz being corrected.
        """
        self.quiz_id = quiz_id

    def correct_quiz(self) -> dict:
        """
        Checks all user answers against the correct answers for the specified quiz
        and calculates the score.

        Returns:
            dict: A dictionary containing the results and the calculated score.
        """
        results = []
        total_score = 0
        total_possible_score = 0

        # Fetch all questions for the quiz
        questions = Questions.all(where="quiz_id = ?", params=(self.quiz_id,))

        # Fetch all answers for this quiz
        answers = Answer.all(where="quiz_id = ?", params=(self.quiz_id,))

        # Create a mapping of question_id to correct_answer_id (no need for answer text)
        for question in questions:
            correct_answer_id = question.correct_option_id

            # Find the user's answer for this question
            user_answer = next((answer for answer in answers if answer.question_id == question.id), None)

            # If user_answer.answer_ids is stored as a string, convert it to a list
            if user_answer is not None and isinstance(user_answer.answer_ids, str):
                user_answer.answer_ids = json.loads(user_answer.answer_ids)  # Convert string to list

            # Calculate score based on difficulty
            difficulty_score = self.get_difficulty_score(question.difficulty)
            total_possible_score += difficulty_score  # Add to total possible score

            # Check if the user's answer is correct by comparing the answer IDs
            is_correct = user_answer is not None and correct_answer_id in user_answer.answer_ids

            if is_correct:
                total_score += difficulty_score  # Increment the score for a correct answer

            results.append({
                "question_id": question.id,
                "user_answer": user_answer.answer_ids if user_answer else None,
                "correct_answer": correct_answer_id,
                "is_correct": is_correct
            })


        # Calculate percentage score out of 100
        score_percentage = (total_score / total_possible_score) * 100 if total_possible_score > 0 else 0

        return {
            "results": results,
            "score": round(score_percentage)  # Return the score as an integer
        }

    def get_difficulty_score(self, difficulty: str) -> int:
        """
        Returns the score value based on the difficulty of the question.

        Args:
            difficulty (str): The type of the question (difficulty level).

        Returns:
            int: The score associated with the difficulty level.
        """
        if difficulty == "easy":
            return 1
        elif difficulty == "medium":
            return 2
        elif difficulty == "hard":
            return 3
        return 0  # Default score if difficulty is not recognized

    def get_correct_answer_text(self, correct_option_id: int) -> str:
        """
        Fetches the correct answer text from the Options table based on the correct option ID.

        Args:
            correct_option_id (int): The ID of the correct option.

        Returns:
            str: The text of the correct answer.
        """
        option = Options.find(correct_option_id)
        return option.option_text if option else ""
