import os
from p8_integration_tests.base_test_case import BaseTestCase


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
