"""
Simple question generation mechanism
"""

import random
from uuid import uuid4

try:
    from src.question_adapters import AdapterJson
    from src.question_manager import QuestionManager
    from src.question import Question, QuestionQueryLine, \
        ComplexityLevel, QuestionRecommendation
    from src.constants import SRC_FOLDER
except ModuleNotFoundError:
    from question_adapters import AdapterJson
    from question_manager import QuestionManager
    from question import Question, QuestionQueryLine, \
        ComplexityLevel, QuestionRecommendation
    from constants import SRC_FOLDER


class RandomQuestionGenerator:
    """
    Generates questions using QuestionManager and list of queries
    """

    def __init__(self, manager: QuestionManager,
                 queries: list[QuestionQueryLine]) -> None:
        self._manager = manager
        self._queries = queries
        self._generated: list[QuestionRecommendation] = []

    def get_recommendations(self) -> list[QuestionRecommendation]:
        """
        Processes questions using queries and return recommended questions
        """
        questions = self._manager.get_questions()
        for query_line in self._queries:
            query_recommendations = []
            for question in questions:
                if self._match_question_category(question, query_line) and \
                    self._match_question_complexity(question, query_line) and \
                        self._match_question_labels(question, query_line):
                    query_recommendations.append(question)
            recommended = self._get_question_selection(
                query_recommendations, query_line.number_questions)
            self._generated.append(QuestionRecommendation(
                query=query_line, questions=recommended))
        return self._generated

    def _get_question_selection(self, recommendations: list[Question],
                                num_questions: int) -> list[Question]:
        """
        Samples recommended questions if any
        """
        if len(recommendations) < num_questions:
            return recommendations
        return random.sample(recommendations, num_questions)

    def _match_question_labels(self, question: Question,
                               query: QuestionQueryLine) -> bool:
        """
        Checks Question labels match QuestionQueryLine labels
        """
        if not query.labels or not question.labels:
            return True
        return True if not query.labels.difference(question.labels) else False

    def _match_question_complexity(self, question: Question,
                                   query: QuestionQueryLine) -> bool:
        """
        Checks Question complexity is appropriate for QueryLine complexity
        """
        return True if (question.complexity == query.complexity) \
            or not query.complexity else False

    def _match_question_category(self, question: Question,
                                 query: QuestionQueryLine) -> bool:
        """
        Checks Question category is appropriate according to QueryLine category
        """
        return True if (question.category == query.category) \
            or not query.category else False


def print_recommendations(recommendations:
                          list[QuestionRecommendation]) -> None:
    """
    Prints generator recommendations
    """
    for rec in recommendations:
        print(f'''
        -------------PARAMS--------------------
        Questions: {rec.query.number_questions}
        Category: {rec.query.category}
        Complexity: {rec.query.complexity}
        Labels: {rec.query.labels}
        -------------QUESTIONS-----------------
        ''')
        for q in rec.questions:
            print(f'>>> {q.original_text}')
            print(f'   possible-> {q.possible_answers}')
            print(f'    correct-> {q.correct_answers}')
        print('---------------------------------------')


def main() -> None:
    """
    Entrypoint for the module
    """
    adapter = AdapterJson(SRC_FOLDER / 'questions')
    manager = QuestionManager(adapter=adapter)
    queries = [
        QuestionQueryLine(id=uuid4(), number_questions=2,
                          category="Программирование",
                          complexity=None,
                          labels=set(["Python", "Первая лекция"])),
        QuestionQueryLine(uuid4(), 2, "Программирование",
                          ComplexityLevel.HARD,
                          set(["Python", "Вторая лекция"])),
        QuestionQueryLine(uuid4(), 3, "Программирование",
                          ComplexityLevel.MEDIUM,
                          set(["Python", "Вторая лекция"])),
        QuestionQueryLine(uuid4(), 3, "Программирование",
                          ComplexityLevel.SIMPLE,
                          set(["Python", "Вторая лекция"])),
    ]
    generator = RandomQuestionGenerator(manager=manager, queries=queries)
    print_recommendations(generator.get_recommendations())


if __name__ == '__main__':
    main()
