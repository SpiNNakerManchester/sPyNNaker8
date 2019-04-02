from __future__ import division
import unittest
import spynnaker8 as p


class MyTestCase(unittest.TestCase):

    def check_spikes(self, input, expected):
        neo = input.get_data("spikes")
        spikes = neo.segments[0].spiketrains
        count = 0
        for a_spikes in spikes:
            count += len(a_spikes)
        self.assertAlmostEqual(expected, count/len(spikes), delta=expected/10)

    def recording_poisson_spikes(self):
        p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
        n_neurons = 256  # number of neurons in each population
        p.set_number_of_neurons_per_core(p.IF_curr_exp, n_neurons / 2)

        cell_params_lif = {'cm': 0.25,
                           'i_offset': 0.0,
                           'tau_m': 20.0,
                           'tau_refrac': 2.0,
                           'tau_syn_E': 5.0,
                           'tau_syn_I': 5.0,
                           'v_reset': -70.0,
                           'v_rest': -65.0,
                           'v_thresh': -50.0
                           }

        pop_1 = p.Population(
            n_neurons, p.IF_curr_exp, cell_params_lif, label='pop_1')
        input = p.Population(
            n_neurons, p.SpikeSourcePoisson, {}, label='inputSpikes_1')

        p.Projection(input, pop_1, p.OneToOneConnector())

        input.record("spikes")

        p.run(5000)
        self.check_spikes(input, 5)

        p.end()

    def test_recording_poisson_spikes(self):
        self.runsafe(self.recording_poisson_spikes)

    def recording_poisson_spikes_big(self):
        p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
        n_neurons = 2560  # number of neurons in each population
        p.set_number_of_neurons_per_core(p.IF_curr_exp, n_neurons / 2)

        cell_params_lif = {'cm': 0.25,
                           'i_offset': 0.0,
                           'tau_m': 20.0,
                           'tau_refrac': 2.0,
                           'tau_syn_E': 5.0,
                           'tau_syn_I': 5.0,
                           'v_reset': -70.0,
                           'v_rest': -65.0,
                           'v_thresh': -50.0
                           }

        pop_1 = p.Population(
            n_neurons, p.IF_curr_exp, cell_params_lif, label='pop_1')
        input = p.Population(
            n_neurons, p.SpikeSourcePoisson, {}, label='inputSpikes_1')

        p.Projection(input, pop_1, p.OneToOneConnector())

        input.record("spikes")

        p.run(5000)
        self.check_spikes(input, 5)

        p.end()

    def test_recording_poisson_spikes_big(self):
        self.runsafe(self.recording_poisson_spikes_big)

    def recording_poisson_spikes_rate_0(self):
        p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
        n_neurons = 256  # number of neurons in each population
        p.set_number_of_neurons_per_core(p.IF_curr_exp, n_neurons / 2)

        cell_params_lif = {'cm': 0.25,
                           'i_offset': 0.0,
                           'tau_m': 20.0,
                           'tau_refrac': 2.0,
                           'tau_syn_E': 5.0,
                           'tau_syn_I': 5.0,
                           'v_reset': -70.0,
                           'v_rest': -65.0,
                           'v_thresh': -50.0
                           }

        pop_1 = p.Population(
            n_neurons, p.IF_curr_exp, cell_params_lif, label='pop_1')
        input = p.Population(
            n_neurons, p.SpikeSourcePoisson, {'rate': 0}, label='input')

        p.Projection(input, pop_1, p.OneToOneConnector())

        input.record("spikes")

        p.run(5000)
        self.check_spikes(input, 0)

        p.end()

    def test_recording_poisson_spikes_rate_0(self):
        self.runsafe(self.recording_poisson_spikes_rate_0)


if __name__ == '__main__':
    unittest.main()
