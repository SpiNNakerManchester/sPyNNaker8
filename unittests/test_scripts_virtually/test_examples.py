import os
import unittest
from p8_integration_tests.base_test_case import BaseTestCase
import matplotlib.pyplot as plt


class TestScripts(BaseTestCase):
    """
    test the introlabs
    """
    def setUp(self):
        super(TestScripts, self).setUp()
        examples_tests_dir = os.path.dirname(__file__)
        unittest_dir = os.path.dirname(examples_tests_dir)
        spynnaker8_dir = os.path.dirname(unittest_dir)
        self._introlab_dir = os.path.join(spynnaker8_dir, "PyNN8Examples")
        # Jenkins appears to place "PyNN8Examples" here
        # if not os.path.exists(self._introlab_dir):
        #    parent_dir = os.path.dirname(spynnaker8_dir)
        #    print(parent_dir)
        #    self._introlab_dir = os.path.join(parent_dir, "PyNN8Examples")

    def mockshow(self):
        self._show = True

    def check_script(self, script):
        from runpy import run_path
        run_path(script)
        self.report(script, "scripts_ran_successfully")

    def check_plotting_script(self, script):
        self._show = False
        plt.show = self.mockshow
        self.check_script(script)
        assert self._show

    def check_directory(self, path, skips=[]):
        directory = os.path.join(self._introlab_dir, path)
        for a_script in os.listdir(directory):
            if a_script.endswith(".py"):
                script = os.path.join(directory, a_script)
                try:
                    plotting = "import matplotlib.pyplot" in open(
                        script).read()
                    if plotting:
                        self.check_plotting_script(script)
                    else:
                        self.check_script(script)
                except Exception as ex:
                    if a_script in skips:
                        self.report(
                            script, "scripts_skipped_with_unkown_issues")
                    else:
                        print("Error on {}".format(script))
                        raise ex

    def examples(self):
        self.check_directory(
            "examples", ["synfire_if_curr_exp_large_array.py"])

    def test_examples(self):
        self.runsafe(self.examples)


if __name__ == '__main__':
    unittest.main()
