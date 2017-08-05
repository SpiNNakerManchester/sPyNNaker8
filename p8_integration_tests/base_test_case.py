import os
import random
import sys
import unittest
from unittest import SkipTest
from spinn_front_end_common.utilities import globals_variables

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
        globals_variables.unset_simulator()
        class_file = sys.modules[self.__module__].__file__
        path = os.path.dirname(os.path.abspath(class_file))
        os.chdir(path)

    def assert_logs_messages(
            self, log_records, sub_message, log_level='ERROR', count=1,
            allow_more=False):
        seen = 0
        for record in log_records:
            if record.levelname == log_level:
                if sub_message in record.msg:
                    seen += 1
        if allow_more:
            if seen >= count:
                return
        if seen == count:
            return
        msg = "\"{}\" not found in any {} logs {} times, was found {} " \
              "times".format(sub_message, log_level, count, seen)
        raise self.failureException(msg)
