"""
Question representation
"""

from enum import Enum
from dataclasses import dataclass


class ComplexityLevel(str, Enum):
    """
    Complexity labels predefined
    """
    
    SIMPLE: str = 'Простой'
    MEDIUM: str = 'Средний'
    HARD: str = 'Сложный'


@dataclass
class Question:
    """
    Question representation
    """
    id: int
    original_text: str
    category: str | None = None
    labels: list[str] | None = None
    complexity: ComplexityLevel | None = None
    possible_answers: list[str] | None = None
