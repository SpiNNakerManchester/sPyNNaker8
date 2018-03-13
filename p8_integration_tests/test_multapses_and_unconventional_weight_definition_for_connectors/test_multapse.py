from __future__ import print_function
import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
from six import assertCountEqual


def do_run():
    p.setup(timestep=1.0)
    cellparams = {"spike_times": [0]}
    input_pop = p.Population(1, p.SpikeSourceArray(**cellparams),
                             label="input")
    cell_params_lif = {'cm': 0.25,  # nF
                       'i_offset': 0.0, 'tau_m': 20.0, 'tau_refrac': 2.0,
                       'tau_syn_E': 5.0, 'tau_syn_I': 5.0, 'v_reset': -70.0,
                       'v_rest': -65.0, 'v_thresh': -50.0}
    pop = p.Population(2, p.IF_curr_exp(**cell_params_lif),
                       label="pop")

    connections = list()
    connections.append(p.Projection(input_pop, pop,
                                    p.AllToAllConnector(),
                                    p.StaticSynapse(weight=[0.3, 1.0],
                                                    delay=[1, 17])))
    connections.append(p.Projection(input_pop, pop,
                                    p.AllToAllConnector(),
                                    p.StaticSynapse(weight=[0.3, 1.0],
                                                    delay=[2, 15])))
    connections.append(p.Projection(input_pop, pop,
                                    p.AllToAllConnector(),
                                    p.StaticSynapse(weight=[0.7, 0.3],
                                                    delay=[3, 33])))

    pre_weights = list()
    pre_delays = list()
    for connection in connections:
        pre_weights.append(connection.get('weight', 'list'))
        pre_delays.append(connection.get('delay', 'list'))

    p.run(100)

    post_weights = list()
    post_delays = list()
    for connection in connections:
        post_weights.append(connection.get('weight', 'list'))
        post_delays.append(connection.get('delay', 'list'))

    p.end()

    return (pre_weights, pre_delays, post_weights, post_delays)


class TestMultapse(BaseTestCase):

    def test_multapse(self):
        (pre_weights, pre_delays, post_weights, post_delays) = do_run()
        for pre_weight, post_weight, pre_delay, post_delay in zip(
                pre_weights, post_weights, pre_delays, post_delays):
            assertCountEqual(self, pre_weight, post_weight)
            assertCountEqual(self, pre_delay, post_delay)


if __name__ == '__main__':
    (pre_weights, pre_delays, post_weights, post_delays) = do_run()
    for pre_weight, post_weight, pre_delay, post_delay in zip(
            pre_weights, post_weights, pre_delays, post_delays):
        print("Weights before:", pre_weight, "and after:", post_weight)
        print("Delays before:", pre_delay, "and after:", post_delay)
