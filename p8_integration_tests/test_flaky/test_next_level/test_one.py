from flaky import flaky
from spalloc.job import JobDestroyedError
from p8_integration_tests.base_test_case import BaseTestCase

count1 = 0
count2 = 0


def is_job_destroyed(err, *args):
    return issubclass(err[0], JobDestroyedError)


@flaky(max_runs=3)
class TestOne(BaseTestCase):

    def test_always_pass(self):
        return

    def test_destory_once(self):
        global count1
        if count1 == 0:
            count1 = 1
            raise JobDestroyedError("Destroyed")
