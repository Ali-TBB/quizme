import json
from utils.collection import Collection


class Answer(Collection):
    table = "answers"

    def __init__(
        self,
        id: int,
        question_id: int,
        quiz_id: int,
        answer_ids: str,
        correct_ids: str,
        created_at=None,
        updated_at=None
    ):
        """
        Initializes a new Answer object.

        Args:
            id (int): The ID of the answer.
            question_id (int): The ID of the associated question.
            answer_ids (str): The ids of the answer.
            correct_ids (str): The ids of the corrected answer.
            created_at (datetime, optional): When the answer was created.
            updated_at (datetime, optional): When the answer was last updated.
        """
        super().__init__(
            {
                "id": id,
                "question_id": question_id,
                "quiz_id": quiz_id,
                "answer_ids": json.dumps(answer_ids),
                "correct_ids": json.dumps(correct_ids),
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

    @property
    def answer_id(self):
        return self.get("id")

    @answer_id.setter
    def answer_id(self, value: int):
        self.set("id", value)

    @property
    def question_id(self):
        return self.get("question_id")

    @question_id.setter
    def question_id(self, value: int):
        self.set("question_id", value)

    @property
    def answer_ids(self) -> list[int]:
        """
        Getter for answer_ids. Returns a list of answer IDs.
        """
        answer_str = self.get("answer_ids")
        return json.loads(answer_str) if answer_str else []
    @answer_ids.setter
    def answer_ids(self, value: list[int]):
        """
        Setter for answer_ids. Takes a list of answer IDs and stores it as a JSON string.
        """
        answer_str = json.dumps(value)
        self.set("answer_ids", answer_str)

    @property
    def correct_ids(self) -> list[int]:
        """
        Getter for correct_ids. Returns a list of correct IDs.
        """
        correct_str = self.get("correct_ids")
        return json.loads(correct_str) if correct_str else []

    @correct_ids.setter
    def correct_ids(self, value: list[int]):
        """
        Setter for correct_ids. Takes a list of correct IDs and stores it as a JSON string.
        """
        correct_str = json.dumps(value)
        self.set("correct_ids", correct_str)

    @property
    def created_at(self):
        return self.get("created_at")

    @created_at.setter
    def created_at(self, value):
        self.set("created_at", str(value))

    @property
    def updated_at(self):
        return self.get("updated_at")

    @updated_at.setter
    def updated_at(self, value):
        self.set("updated_at", str(value))
