from p8_integration_tests.quick_test.test_debug_mode.check_debug import (
    CheckDebug)


class TestDebug(CheckDebug):

    def test_debug(self):
        self.runsafe(self.debug)
