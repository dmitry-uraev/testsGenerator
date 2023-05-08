"""
Adapters for different data formats
"""

import dataclasses
import json

from abc import ABC
from pathlib import Path
from uuid import uuid4

try:
    from src.question import Question, ComplexityLevel
    from src.constants import TEST_DATA
    from src.errors import PathNotExists
except ModuleNotFoundError:
    from question import Question, ComplexityLevel
    from constants import TEST_DATA
    from errors import PathNotExists


class Adapter(ABC):
    """
    Abstract adapter interface
    """
    def __init__(self, data_path: Path) -> None:
        self.path = data_path

    def _is_folder(self) -> bool:
        """
        Checks path specified is folder or specific file
        """
        return self.path.is_dir()

    def _check_data_folder(self) -> bool:
        """
        Check path target exists
        """
        return self.path.exists()

    def _load_from_folder(self) -> list[Question]:
        """
        Gets questions from all files in the folder specified
        """
        raise NotImplementedError

    def _load_from_file(self, fp: Path) -> list[Question]:
        """
        Gets questions from specific file specified
        """
        raise NotImplementedError

    def load_questions(self) -> list[Question]:
        """
        Returns a list of questions from the path specified
        """
        raise NotImplementedError


class AdapterJson(Adapter):
    """
    Gets questions from the json files
    """

    def _load_from_file(self, fp: Path) -> list[Question]:
        """
        Gets questions from json file
        """
        with open(file=fp, encoding='utf-8', mode='r') as questions_file:
            questions_data = json.load(questions_file)
            return [Question(id=uuid4(),
                             original_text=q_data["original_text"],
                             category=q_data["category"],
                             labels=set(q_data["labels"]),
                             complexity=ComplexityLevel(q_data["complexity"]),
                             possible_answers=q_data["possible_answers"],
                             correct_answers=q_data["correct"]
                             )
                    for _, q_data in questions_data.items()]

    def _load_from_folder(self) -> list[Question]:
        """
        Gets all json files in folder and calls _load_from_file on each
        """
        questions = []
        for file in self.path.iterdir():
            if str(file).endswith('.json'):
                questions.extend(self._load_from_file(fp=file))
        return questions

    def load_questions(self) -> list[Question]:
        """
        Checks path specified and return questions retreived
        """
        if not self._check_data_folder():
            raise PathNotExists
        return self._load_from_folder() if self._is_folder() \
            else self._load_from_file(fp=self.path)

    def save_questions(self, questions: list[Question], path: Path) -> None:
        """
        DEPRECATED: Saves a list of Question objects to the folder specified
        """
        with open(file=path, mode='w', encoding='utf-8') as file:
            formatted = dict()
            for q in questions:
                formatted[str(q.id)] = dataclasses.asdict(q)
                formatted[str(q.id)].pop('id')
            json.dump(obj=formatted, fp=file, ensure_ascii=False, indent=2)


def get_questions(path: Path) -> list[Question]:
    """
    Module entrypoint
    """
    adapter = AdapterJson(TEST_DATA)
    return adapter.load_questions()


if __name__ == "__main__":
    get_questions(path=TEST_DATA)
