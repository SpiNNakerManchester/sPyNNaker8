from p8_integration_tests.base_test_case import BaseTestCase
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E401


class ScriptChecker(BaseTestCase):

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
