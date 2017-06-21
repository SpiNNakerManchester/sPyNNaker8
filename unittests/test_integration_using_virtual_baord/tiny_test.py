import p8_integration_tests.test_various.tiny_test as tiny_test
from p8_integration_tests.base_test_case import BaseTestCase


class TinyTest(BaseTestCase):

    def test_run(self):
        all1, all2 = tiny_test.do_run()


if __name__ == '__main__':
    all1, all2 = tiny_test.do_run()
