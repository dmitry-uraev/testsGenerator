"""
Adapters for different data formats
"""

import json

from abc import ABC
from pathlib import Path

try:  # awfull workaround for running code itself and running pytest
    from question import Question
    from constants import TEST_DATA
    from errors import PathNotExists
except ModuleNotFoundError:
    from src.question import Question
    from src.constants import TEST_DATA
    from src.errors import PathNotExists  


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
            return [Question(id=q_id, **q_data) for q_id, q_data in questions_data.items()]
        
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
        if not self._check_data_folder:
            raise PathNotExists
        return self._load_from_folder() if self._is_folder() else self._load_from_file(fp=self.path)


def main() -> None:
    """
    Module entrypoint
    """
    adapter = AdapterJson(TEST_DATA)
    questions = adapter.load_questions()
    [print(question) for question in questions]


if __name__ == "__main__":
    main()
