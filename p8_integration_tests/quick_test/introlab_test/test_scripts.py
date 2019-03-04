import os
import unittest
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from p8_integration_tests.base_test_case import BaseTestCase


class TestScripts(BaseTestCase):
    def setUp(self):
        super(TestScripts, self).setUp()
        introllab_tests_dir = os.path.dirname(__file__)
        print(introllab_tests_dir)
        quick_tests_dir = os.path.dirname(introllab_tests_dir)
        print(quick_tests_dir)
        p8_integration_tests_dir = os.path.dirname(quick_tests_dir)
        print(p8_integration_tests_dir)
        spynnaker8_dir = os.path.dirname(p8_integration_tests_dir)
        print(spynnaker8_dir)
        # Jenkins appears to place Intorlabs here
        self._introlab_dir = os.path.join(spynnaker8_dir, "IntroLab")
        if not os.path.exists(self._introlab_dir):
            parent_dir = os.path.dirname(spynnaker8_dir)
            print(parent_dir)
            self._introlab_dir = os.path.join(parent_dir, "IntroLab")

    def mockshow(self):
        self._show = True

    """
    test the introlabs
    """
    def test_simple(self):
        self._show = False
        plt.show = self.mockshow
        simple = os.path.join(self._introlab_dir, "learning", "simple.py")
        from runpy import run_path
        run_path(simple)
        assert self._show


if __name__ == '__main__':
    unittest.main()
