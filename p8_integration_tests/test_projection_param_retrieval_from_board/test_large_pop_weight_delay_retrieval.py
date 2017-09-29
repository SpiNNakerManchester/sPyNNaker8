import numpy

from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as p

n_neurons = 900


def do_run():
    p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
    n_neurons = 900  # number of neurons in each population

    cell_params_lif = {'cm': 0.25,  # nF
                       'i_offset': 0.0, 'tau_m': 20.0, 'tau_refrac': 2.0,
                       'tau_syn_E': 5.0, 'tau_syn_I': 5.0, 'v_reset': -70.0,
                       'v_rest': -65.0, 'v_thresh': -50.0}

    populations = list()
    projections = list()

    weight_to_spike = 2.0
    delay = 1

    populations.append(
        p.Population(n_neurons, p.IF_curr_exp, cell_params_lif, label='pop_1'))

    populations.append(
        p.Population(n_neurons, p.IF_curr_exp, cell_params_lif, label='pop_2'))

    connectors = p.AllToAllConnector()
    synapse_type = p.StaticSynapse(weight=weight_to_spike, delay=delay)
    projections.append(p.Projection(populations[0], populations[1],
                                    connectors, synapse_type=synapse_type))

    delays = []
    weights = []

    # before
    delays.append(projections[0].get(attribute_names=["delay"],
                                     format="nparray"))
    weights.append(projections[0].get(attribute_names=["weight"],
                                      format="array"))

    p.run(100)

    # after
    delays.append(projections[0].get(attribute_names=["delay"],
                                     format="array"))
    weights.append(projections[0].get(attribute_names=["weight"],
                                      format="array"))

    p.end()

    return (delays, weights)


class LargePopWeightDelayRetrival(BaseTestCase):
    def test_compare_before_and_after(self):
        (delays, weights) = do_run()
        self.assertEquals(n_neurons * n_neurons,
                          len(weights[0][0])*len(weights[0][0][0]))
        self.assertEquals(n_neurons * n_neurons,
                          len(weights[1][0])*len(weights[1][0][0]))
        self.assertTrue(numpy.allclose(weights[0][0][0], weights[1][0][0]))

        self.assertEquals(n_neurons * n_neurons,
                          len(delays[0][0])*len(delays[0][0][0]))
        self.assertEquals(n_neurons * n_neurons,
                          len(delays[1][0])*len(delays[1][0][0]))
        self.assertTrue(numpy.allclose(delays[0][0][0], delays[1][0][0]))


if __name__ == '__main__':
    (delays, weights) = do_run()
    print weights[0][0]
    print weights[1][0]
    print delays[0][0]
    print delays[1][0]
