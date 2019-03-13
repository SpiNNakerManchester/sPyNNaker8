from flaky import flaky
from p8_integration_tests.base_test_case import BaseTestCase


@flaky(max_runs=4, min_passes=2)
class TestOne(BaseTestCase):

    count1 = 0

    def test_always_pass(self):
        return

    def fail_once(self):
        global count1
        if count1 == 0:
            count1 = 1
            raise Exception("Pop One")
