"""
Synfirechain-like example
"""
import unittest
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner

synfire_run = SynfireRunner()


class TestSimple(BaseTestCase):
    """
    that it does not crash in debug mode. All reports on.
    """
    def test_simple(self):
        """
        test for get spikes
        """
        synfire_run.do_run(5)


if __name__ == '__main__':
    unittest.main()
