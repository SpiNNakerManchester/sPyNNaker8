import os
from p8_integration_tests.scripts_test.script_checker import ScriptChecker


class TestIntroLabs(ScriptChecker):
    """
    test the introlabs
    """
    def setUp(self):
        super(TestIntroLabs, self).setUp()
        introllab_tests_dir = os.path.dirname(__file__)
        p8_integration_tests_dir = os.path.dirname(introllab_tests_dir)
        spynnaker8_dir = os.path.dirname(p8_integration_tests_dir)
        self._introlab_dir = os.path.join(spynnaker8_dir, "IntroLab")
        # Jenkins appears to place Intorlabs here
        if not os.path.exists(self._introlab_dir):
            parent_dir = os.path.dirname(spynnaker8_dir)
            self._introlab_dir = os.path.join(parent_dir, "IntroLab")
