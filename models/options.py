from utils.collection import Collection

class Options(Collection):

    table = "Options"

    def __init__(
        self, id: int, question_id: int, option_text: str,
        created_at=None, updated_at=None
    ):
        super().__init__(
            {
                "id": id,
                "question_id": question_id,
                "option_text": option_text,
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )

    @property
    def id(self) -> int:
        return self.get("id")

    @id.setter
    def id(self, value: int):
        self.set("id", value)

    @property
    def question_id(self) -> int:
        return self.get("question_id")

    @question_id.setter
    def question_id(self, value: int):
        self.set("question_id", value)

    @property
    def option_text(self) -> str:
        return self.get("option_text")

    @option_text.setter
    def option_text(self, value: str):
        self.set("option_text", value)

