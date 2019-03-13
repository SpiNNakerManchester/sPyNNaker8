from flaky import flaky
from spalloc.job import JobDestroyedError
from p8_integration_tests.base_test_case import BaseTestCase

count1 = 0
count2 = 0


def is_job_destroyed(err, *args):
    return issubclass(err[0], JobDestroyedError)


class TestOne(BaseTestCase):

    @flaky(max_runs=3, rerun_filter=is_job_destroyed)
    def test_always_pass(self):
        return

    @flaky(max_runs=3, rerun_filter=is_job_destroyed)
    def test_destory_once(self):
        global count1
        if count1 == 0:
            count1 = 1
            raise JobDestroyedError("Destroyed")

    @flaky(max_runs=3, rerun_filter=is_job_destroyed)
    def test_fail_once(self):
        global count2
        if count2 == 0:
            count2 = 1
            self.assertEquals(count2, 3)
