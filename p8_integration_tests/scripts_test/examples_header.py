import os
from p8_integration_tests.base_test_case import BaseTestCase
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E401


class TestExamples(BaseTestCase):
    """
    test the introlabs
    """
    def setUp(self):
        super(TestExamples, self).setUp()
        examples_tests_dir = os.path.dirname(__file__)
        p8_integration_tests_dir = os.path.dirname(examples_tests_dir)
        spynnaker8_dir = os.path.dirname(p8_integration_tests_dir)
        self._introlab_dir = os.path.join(spynnaker8_dir, "PyNN8Examples")
        # Jenkins appears to place "PyNN8Examples" here
        if not os.path.exists(self._introlab_dir):
            parent_dir = os.path.dirname(spynnaker8_dir)
            self._introlab_dir = os.path.join(parent_dir, "PyNN8Examples")

    def mockshow(self):
        self._show = True

    def check_script(self, script, broken):
        plotting = "import matplotlib.pyplot" in open(script).read()
        if plotting:
            self._show = False
            plt.show = self.mockshow
        from runpy import run_path
        try:
            run_path(script)
            if plotting:
                assert self._show
            self.report(script, "scripts_ran_successfully")
        except Exception as ex:
            if broken:
                self.report(
                    script, "scripts_skipped_with_unkown_issues")
            else:
                print("Error on {}".format(script))
                raise ex
