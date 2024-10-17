import typing_extensions as typing


class QuestionDataType(typing.TypedDict):
    question: str
    options: list[str]
    corrected_answer: list[str]
    difficulty: str

class QuizGenerateDataType(typing.TypedDict):
    questions: list[QuestionDataType]
    question_count: int
