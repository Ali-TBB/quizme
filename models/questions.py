import json


from utils.collection import Collection

class Questions(Collection):

    table = "questions"

    def __init__(
        self, id: int,
        quiz_id: int,
        content:str,
        options_ids: str,
        correct_option_id: int,
        created_at=None,
        updated_at=None
    ):
        super().__init__(
            {
                "id": id,
                "quiz_id": quiz_id,
                "content": content,
                "options_ids": options_ids,
                "correct_option_id": correct_option_id,
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )

    @property
    def quiz_id(self) -> int:
        return self.get("quiz_id")

    @quiz_id.setter
    def quiz_id(self, value: int):
        self.set("quiz_id", value)

    @property
    def question_type(self) -> str:
        return self.get("question_type")

    @question_type.setter
    def question_type(self, value: str):
        self.set("question_type", value)

    @property
    def content(self) -> str:
        return self.get("content")

    @content.setter
    def content(self, value: str):
        self.set("content", value)

    @property
    def options_ids(self) -> list[int]:
        # Deserialize the JSON string into a list
        options_str = self.get("options_ids")
        return json.loads(options_str) if options_str else []

    @options_ids.setter
    def options_ids(self, value: list[int]):
        # Convert the list to a JSON string
        options_str = json.dumps(value)
        # Set the JSON string in the collection
        self.set("options_ids", options_str)

    @property
    def correct_option_id(self) -> int:
        return self.get("correct_option_id")

    @correct_option_id.setter
    def correct_option_id(self, value: int):
        self.set("correct_option_id", value)

    @property
    def created_at(self):
        return self.get("created_at")

    @created_at.setter
    def created_at(self, value):
        self.set("created_at", value)

    @property
    def updated_at(self):
        return self.get("updated_at")

    @updated_at.setter
    def updated_at(self, value):
        self.set("updated_at", value)
    @property
    def difficulty(self) -> str:
        return self.get("difficulty")

    @difficulty.setter
    def difficulty(self, value: str):
        self.set("difficulty", value)