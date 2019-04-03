import p8_integration_tests.quick_test.test_various.test_tiny_with_reset as test_tiny
from p8_integration_tests.base_test_case import BaseTestCase


class TinyTest(BaseTestCase):

    def test_run(self):
        all1, all2 = test_tiny.do_run()


if __name__ == '__main__':
    all1, all2 = test_tiny.do_run()
