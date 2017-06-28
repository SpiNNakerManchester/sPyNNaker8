from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as p


def before_run(nNeurons):
    p.setup(timestep=1, min_delay=1, max_delay=15)

    neuron_parameters = {'cm': 0.25, 'i_offset': 2, 'tau_m': 10.0,
                         'tau_refrac': 2.0, 'tau_syn_E': 0.5, 'tau_syn_I': 0.5,
                         'v_reset': -65.0, 'v_rest': -65.0, 'v_thresh': -50.0}

    pop = p.Population(nNeurons, p.IF_curr_exp, neuron_parameters,
                       label='pop_1')

    return pop.celltype


class Test_celltype(BaseTestCase):

    def test_before_run(self):
        nNeurons = 20  # number of neurons in each population
        celltype = before_run(nNeurons)
        self.assertEqual(p.IF_curr_exp.build_model(), type(celltype))


if __name__ == '__main__':
    nNeurons = 20  # number of neurons in each population
    celltype = before_run(nNeurons)
    print celltype
