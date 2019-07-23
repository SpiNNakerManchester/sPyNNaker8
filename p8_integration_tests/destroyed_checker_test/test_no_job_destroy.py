import os
from p8_integration_tests.base_test_case import BaseTestCase


class TestNoJobDestory(BaseTestCase):

    def test_no_destory_file(self):
        warning_path = self.spinnman_exception_path()
        if os.path.exists(warning_path):
            with open(warning_path) as warning_file:
                warning_text = warning_file.read()
            print(warning_text)
            raise AssertionError(warning_text)
        warning_path = self.destory_path()
        if os.path.exists(warning_path):
            with open(warning_path) as warning_file:
                warning_text = warning_file.read()
            print(warning_text)
            raise AssertionError(warning_text)
