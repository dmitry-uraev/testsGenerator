"""
Adapters package test suit
"""


import pytest
import unittest

from src.constants import TEST_DATA
from src.adapters import AdapterJson


class AdapterJsonTest(unittest.TestCase):
    """
    AdapterJson implementation tests
    """

    def test_ideal_case(self) -> None:
        """
        Check questions are retreived with no errors
        """
        self.assertTrue(AdapterJson(TEST_DATA).load_questions())
