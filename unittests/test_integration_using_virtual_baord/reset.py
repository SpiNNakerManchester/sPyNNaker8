from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as p


class SynfireIfCurrExp(BaseTestCase):

    def test_run(self):
        p.setup()
        cell_params_lif = {'cm': 0.25, 'i_offset': 0.0, 'tau_m': 20.0,
                           'tau_refrac': 2.0, 'tau_syn_E': 5.0,
                           'tau_syn_I': 5.0, 'v_reset': -70.0, 'v_rest': -65.0,
                           'v_thresh': -50.0}

        pop = p.Population(10, p.IF_curr_exp(**cell_params_lif), label='test')
        p.run(100)
        pop.set(cm=0.30)


if __name__ == '__main__':
    p.setup()
    cell_params_lif = {'cm': 0.25, 'i_offset': 0.0, 'tau_m': 20.0,
                       'tau_refrac': 2.0, 'tau_syn_E': 5.0, 'tau_syn_I': 5.0,
                       'v_reset': -70.0, 'v_rest': -65.0, 'v_thresh': -50.0}

    pop = p.Population(10, p.IF_curr_exp(**cell_params_lif), label='test')
    p.run(100)
    pop.set(cm=0.30)
