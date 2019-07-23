from p8_integration_tests.quick_test.test_debug_mode.check_debug import (
    CheckDebug)


class TestDebug(CheckDebug):

    def debug_no_zero(self):
        self.debug(False)

    def test_debug_no_zero(self):
        self.runsafe(self.debug_no_zero)

    def debug_with_zero(self):
        self.debug(True)

    def test_debug_with_zero(self):
        self.runsafe(self.debug_with_zero)
