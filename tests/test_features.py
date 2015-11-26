import unittest
import pep8
from glob import glob


class TestFeaturesModule(unittest.TestCase):
    def test_import(self):
        """Test import of features module"""
        import foreperiodanalysis.features
