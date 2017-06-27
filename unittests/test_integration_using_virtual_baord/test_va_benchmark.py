import p8_integration_tests.test_0_1_time_steps.test_va_bench_mark_tests.\
    test_va_benchmark as test_va_benchmark
from p8_integration_tests.base_test_case import BaseTestCase


class TinyTest(BaseTestCase):

    def test_run(self):
        test_va_benchmark.do_run()


if __name__ == '__main__':
    test_va_benchmark.do_run()
