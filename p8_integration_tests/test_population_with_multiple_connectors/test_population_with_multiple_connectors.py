import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
import matplotlib.pyplot as plt
import numpy as np


def do_run(plot):

    runtime = 100
    p.setup(timestep=1.0, min_delay=1.0, max_delay=14)
    nNeurons = 2  # number of neurons in each population
    p.set_number_of_neurons_per_core(p.IF_curr_exp, 1)
    p.set_number_of_neurons_per_core(p.SpikeSourceArray, 1)

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

    model = p.IF_curr_exp
    weight_to_spike = 0.1
    all_weight_to_spike = 3.0
    delay = 1

    spikeArray = {'spike_times': [[0], []]}

    input_pop = p.Population(nNeurons, p.SpikeSourceArray(**spikeArray),
                             label='inputSpikes_1')

    target_pop = p.Population(nNeurons, model(**cell_params_lif),
                              label='pop_1')

    proj_1 = p.Projection(
        input_pop, target_pop, p.OneToOneConnector(),
        p.StaticSynapse(weight=weight_to_spike, delay=delay))

    proj_2 = p.Projection(
        input_pop, target_pop, p.AllToAllConnector(),
        p.StaticSynapse(weight=all_weight_to_spike, delay=delay))

    target_pop.record(['spikes'])

    p.run(runtime)
    spikes = target_pop.spinnaker_get_data('spikes')

    print(spikes)

    print(proj_1.get([], format="list"))
    print(proj_2.get([], format="list"))

    if plot:
        if spikes is not None:
            recast_spikes = []
            for index in np.unique(spikes[:, 0]):
                recast_spikes.append(spikes[spikes[:, 0] == index][:, 1])
            f, ax1 = plt.subplots(1, 1, figsize=(10, 5), dpi=300)
            ax1.set_xlim((0, runtime))
            ax1.eventplot(recast_spikes, linelengths=.8)
            ax1.set_xlabel('Time(ms)')
            ax1.set_ylabel('Neuron ID')
            ax1.set_title("Both post neurons should spike")
            plt.savefig("spikes_one_to_one_connector.png",
                        bbox_inches='tight')
            plt.show()

    p.end()

    return spikes


class PopulationWithMultipleConnectorsTest(BaseTestCase):
    def test_run(self):
        spikes = do_run(plot=False)
        # any checks go here
        self.assertEquals(2, len(spikes))
        self.assertEquals(2.0, spikes[0][1])
        self.assertEquals(2.0, spikes[1][1])


if __name__ == '__main__':
    spikes = do_run(plot=True)
