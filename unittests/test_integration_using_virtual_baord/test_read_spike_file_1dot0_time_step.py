from p8_integration_tests.base_test_case import BaseTestCase
import p8_integration_tests.test_1_0_time_steps.\
    test_spike_array_from_read_in_spikes_and_big_slices.\
    test_read_spike_file_1dot0_time_step as integration


class TestReadingSpikeArrayDataAndBigSlices(BaseTestCase):
    def test_script(self):
        integration.do_run()


if __name__ == '__main__':
    integration.do_run()
