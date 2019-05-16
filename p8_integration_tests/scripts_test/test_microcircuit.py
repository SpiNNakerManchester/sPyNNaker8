from p8_integration_tests.scripts_test.script_checker import ScriptChecker
import os
import sys
import stat


class TestMicrocircuit(ScriptChecker):

    def test_microcircuit(self):
        self.runsafe(self.microcircuit)

    def microcircuit(self):
        tests_dir = os.path.dirname(__file__)
        p8_integration_tests_dir = os.path.dirname(tests_dir)
        spynnaker8_dir = os.path.dirname(p8_integration_tests_dir)
        microcircuit_dir = os.path.join(spynnaker8_dir, "microcircuit_model")
        if not os.path.exists(microcircuit_dir):
            parent_dir = os.path.dirname(spynnaker8_dir)
            microcircuit_dir = os.path.join(parent_dir, "microcircuit_model")
        # Get the microcircuit sub directory
        microcircuit_dir = os.path.join(microcircuit_dir, "microcircuit")
        sys.path.append(microcircuit_dir)
        microcircuit_script = os.path.join(
            microcircuit_dir, "microcircuit.py")
        os.makedirs("results")
        self.check_script(microcircuit_script, False)
        for result_file in [
                "spikes_L23E.pkl", "spikes_L23I.pkl",
                "spikes_L4E.pkl", "spikes_L4I.pkl",
                "spikes_L5E.pkl", "spikes_L5I.pkl",
                "spikes_L6E.pkl", "spikes_L6I.pkl",
                "spiking_activity.png"]:
            result_path = os.path.join("results", result_file)
            assert(os.path.exists(result_path))
            assert(os.stat(result_path)[stat.ST_SIZE])
