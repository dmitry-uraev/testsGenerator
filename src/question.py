"""
Question representation
"""

from enum import Enum
from dataclasses import dataclass
from typing import NamedTuple
from uuid import UUID


class ComplexityLevel(Enum):
    """
    Complexity labels predefined
    """

    SIMPLE = 'Простой'
    MEDIUM = 'Средний'
    HARD = 'Сложный'


@dataclass
class Question:
    """
    Question representation
    """
    id: UUID
    original_text: str
    category: str | None = None
    labels: set[str] | None = None
    complexity: ComplexityLevel | None = None
    possible_answers: list[str] | None = None
    correct_answers: list[str | int] | None = None


class QuestionQueryLine(NamedTuple):
    """
    Question generation query representation
    """
    id: UUID
    number_questions: int
    category: str | None = None
    complexity: ComplexityLevel | None = None
    labels: set[str] | None = None


@dataclass
class QuestionRecommendation:
    """
    Question generator recommendation representation
    """
    query: QuestionQueryLine
    questions: list[Question]
