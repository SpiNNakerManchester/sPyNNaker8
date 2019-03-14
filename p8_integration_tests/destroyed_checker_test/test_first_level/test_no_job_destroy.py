import os
from p8_integration_tests.base_test_case import BaseTestCase


class TestNoJobDestory(BaseTestCase):

    def test_no_destory_file(self):
        destory_path = self.destory_path()
        if os.path.exists(destory_path):
            with open(destory_path) as destroy_file:
                destroy_text = destroy_file.read()
            print(destroy_text)
            raise AssertionError(destroy_text)