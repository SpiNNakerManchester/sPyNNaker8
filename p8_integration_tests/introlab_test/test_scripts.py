import os
import unittest
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from p8_integration_tests.base_test_case import BaseTestCase


class TestScripts(BaseTestCase):
    """
    test the introlabs
    """
    def setUp(self):
        super(TestScripts, self).setUp()
        introllab_tests_dir = os.path.dirname(__file__)
        p8_integration_tests_dir = os.path.dirname(introllab_tests_dir)
        spynnaker8_dir = os.path.dirname(p8_integration_tests_dir)
        self._introlab_dir = os.path.join(spynnaker8_dir, "IntroLab")
        # Jenkins appears to place Intorlabs here
        if not os.path.exists(self._introlab_dir):
            parent_dir = os.path.dirname(spynnaker8_dir)
            print(parent_dir)
            self._introlab_dir = os.path.join(parent_dir, "IntroLab")

    def mockshow(self):
        self._show = True

    def check_script(self, script):
        self._show = False
        plt.show = self.mockshow
        from runpy import run_path
        run_path(script)
        assert self._show
        self.report(script, "scrpits_ran_successfully")

    def check_directory(self, path):
        directory = os.path.join(self._introlab_dir, path)
        for a_script in os.listdir(directory):
            if a_script.endswith(".py"):
                script = os.path.join(directory, a_script)
                try:
                    self.check_script(script)
                except Exception as ex:
                    print("Error on {}".format(script))
                    raise ex

    def test_learning(self):
        self.check_directory("learning")

    def test_balanced_random(self):
        self.check_directory("balanced_random")

    def test_synfire(self):
        self.check_directory("synfire")


if __name__ == '__main__':
    unittest.main()