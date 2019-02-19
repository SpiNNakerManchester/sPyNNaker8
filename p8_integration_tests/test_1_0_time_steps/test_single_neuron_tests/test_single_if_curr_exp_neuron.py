"""
test that a single neuron of if curr exp works as expected
"""

# general imports
import spynnaker.plot_utils as plot_utils
from spynnaker8 import SpikeSourcePoisson
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner

cell_params = {'cm': 0.25,
               'i_offset': 0.0,
               'tau_m': 20.0,
               'tau_refrac': 2.0,
               'tau_syn_E': 2.0,
               'tau_syn_I': 2.0,
               'v_reset': -60.0,
               'v_rest': -60.0,
               'v_thresh': -40.0}

simtime = 4000
noise_rate = 200


def do_run(seed=None):

    # Simulate using both simulators
    synfire_run = SynfireRunner()
    synfire_run.do_run(
        n_neurons=1, input_class=SpikeSourcePoisson, rate=noise_rate,
        start_time=0, duration=simtime, seed=seed,
        use_spike_connections=False,
        cell_params=cell_params, run_times=[simtime], record=True,
        record_v=True, randomise_v_init=True, record_input_spikes=True,
        weight_to_spike=0.4)

    s_pop_voltages = synfire_run.get_output_pop_voltage_numpy()
    s_pop_spikes = synfire_run.get_output_pop_spikes_numpy()
    noise_spike_times = synfire_run.get_spike_source_spikes_numpy()

    return noise_spike_times, s_pop_spikes, s_pop_voltages


class TestIfCurrExpSingleNeuron(BaseTestCase):
    """
    tests the get spikes given a simulation at 0.1 ms time steps
    """
    def test_single_neuron(self):
        results = do_run(seed=1)
        (noise_spike_times, s_pop_spikes, _) = results
        self.assertEquals(758, len(noise_spike_times))
        self.assertEquals(15, len(s_pop_spikes))


if __name__ == '__main__':
    results = do_run(seed=1)
    (noise_spike_times, s_pop_spikes, s_pop_voltages) = results
    print(noise_spike_times)
    print(len(noise_spike_times))
    print(s_pop_spikes)
    print(len(s_pop_spikes))
    print(s_pop_voltages)
    plot_utils.plot_spikes([noise_spike_times, s_pop_spikes])
    plot_utils.line_plot(s_pop_voltages, title="s_pop_voltages")
