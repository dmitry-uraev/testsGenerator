"""
Question manager implementation
"""

try:
    from src.question_adapters import AdapterJson
    from src.constants import TEST_DATA
    from src.question import Question
except ModuleNotFoundError:
    from question_adapters import AdapterJson
    from constants import TEST_DATA
    from question import Question


class QuestionManager:
    """
    Loads questions into the programm
    """

    def __init__(self, adapter: AdapterJson) -> None:
        self._adapter: AdapterJson = adapter
        self._storage: list[Question] = self._init_questions_collection()

    def _init_questions_collection(self) -> list[Question]:
        """
        Initializes self._storage with all questions
        """
        return self._adapter.load_questions()

    def get_questions(self) -> list[Question]:
        """
        Gets all questions
        """
        return self._storage


def get_manager(adapter: AdapterJson) -> QuestionManager:
    """
    Entrypoint for the module
    """
    return QuestionManager(adapter=adapter)


if __name__ == "__main__":
    get_manager(adapter=AdapterJson(TEST_DATA))
