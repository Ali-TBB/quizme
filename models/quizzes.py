import json

from utils.collection import Collection


class Quizzes(Collection):

    table = "quizzes"

    def __init__(
        self, id: int, topic: str, difficulty: str, number_of_questions: int = 0, created_at=None, updated_at=None
    ):
        super().__init__(
            {
            "id": id,
            "topic": topic,
            "difficulty": difficulty,
            "number_of_questions": number_of_questions,
            "created_at": created_at,
            "updated_at": updated_at,
            },
        )
    @property
    def topic(self) -> str:
        return self.get("topic")

    @topic.setter
    def topic(self, value):
        self.set("topic", value)

    @property
    def difficulty(self) -> str:
        return self.get("difficulty")

    @difficulty.setter
    def difficulty(self, value: str):
        self.set("difficulty", value)
        
    @property
    def number_of_questions(self) -> int:
        return self.get("number_of_questions")

    @number_of_questions.setter
    def number_of_questions(self, value: int):
        self.set("number_of_questions", value)

    from models.questions import Questions

    @property
    def questions(self) -> list[Questions]:
        from models.questions import Questions

        return Questions.all(where="quiz_id = ?", params=(self.id,))
