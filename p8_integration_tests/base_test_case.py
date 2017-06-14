import os
import random
import sys
import unittest
from unittest import SkipTest

print os.environ.get('P8_INTEGRATION_FACTOR', "1")
p8_integration_factor = float(os.environ.get('P8_INTEGRATION_FACTOR', "1"))
random.seed(os.environ.get('P8_INTEGRATION_SEED', None))


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        factor = random.random()
        if factor > p8_integration_factor:
            msg = "Test skipped by random number {} above " \
                  "P8_INTEGRATION_FACTOR {}" \
                  "".format(factor, p8_integration_factor)
            raise SkipTest(msg)
        class_file = sys.modules[self.__module__].__file__
        path = os.path.dirname(os.path.abspath(class_file))
        os.chdir(path)

    def assert_logs_error(self, log_records, sub_message):
        for record in log_records:
            print record
            if record.levelname == 'ERROR':
                if sub_message in record.msg:
                    return
        msg = "\"{}\" not found in any ERROR logs".format(sub_message)
        raise self.failureException(msg)
