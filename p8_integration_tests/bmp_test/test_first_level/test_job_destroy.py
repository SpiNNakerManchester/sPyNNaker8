import spynnaker8 as sim
from spalloc.job import JobDestroyedError
from p8_integration_tests.base_test_case import BaseTestCase

count1 = 0


class TestJobDestory(BaseTestCase):

    def test_script_ok(self):
        print("ok")

    def destory_once(self):
        global count1
        if count1 < 1:
            count1 = 1
            raise JobDestroyedError("Machine configuration failed. Error: Requests failed on BMP 10.11.213.0")

    def test_destory_once(self):
        self.runsafe(self.destory_once)