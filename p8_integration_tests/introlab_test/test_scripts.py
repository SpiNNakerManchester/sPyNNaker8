import os
import unittest
from p8_integration_tests.base_test_case import BaseTestCase


class TestScripts(BaseTestCase):
    def setUp(self):
        super(TestScripts, self).setUp()
        introllab_tests_dir = os.path.dirname(__file__)
        p8_integration_tests_dir = os.path.dirname(introllab_tests_dir)
        spynnaker8_dir = os.path.dirname(p8_integration_tests_dir)
        parent_dir = os.path.dirname(spynnaker8_dir)
        self._introlab_dir = os.path.join(parent_dir, "IntroLab")


    """
    test the introlabs
    """
    def test_simple(self):
        simple = os.path.join(self._introlab_dir, "learning", "simple.py")
        from runpy import run_path
        run_path(simple)


if __name__ == '__main__':
    unittest.main()
