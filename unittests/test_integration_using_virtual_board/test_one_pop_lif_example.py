#!/usr/bin/python
import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


def do_run(nNeurons):

    p.setup(timestep=1.0, min_delay=1.0, max_delay=8.0)

    cell_params_lif_in = {'tau_m': 333.33, 'cm': 208.33, 'v': 0.0,
                          'v_rest': 0.1, 'v_reset': 0.0, 'v_thresh': 1.0,
                          'tau_syn_E': 1, 'tau_syn_I': 2, 'tau_refrac': 2.5,
                          'i_offset': 3.0}

    pop1 = p.Population(nNeurons, p.IF_curr_exp, cell_params_lif_in,
                        label='pop_0')

    pop1.record("v")
    pop1.record("gsyn_exc")
    pop1.record("spikes")

    p.run(3000)

    neo = pop1.get_data()
    assert(neo is not None)

    p.end()


class OnePopLifExample(BaseTestCase):
    def test_run(self):
        nNeurons = 255  # number of neurons in each population
        do_run(nNeurons)


if __name__ == '__main__':
    nNeurons = 255  # number of neurons in each population
    do_run(nNeurons)
