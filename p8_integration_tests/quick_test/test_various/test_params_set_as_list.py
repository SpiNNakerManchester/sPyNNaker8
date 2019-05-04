from pyNN.random import RandomDistribution, NumpyRNG
import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


class ParamsSetAsList(BaseTestCase):

    def do_run(self):
        nNeurons = 500
        p.setup(timestep=1.0, min_delay=1.0, max_delay=32.0)

        p.set_number_of_neurons_per_core(p.IF_curr_exp, 100)

        cm = list()
        i_off = list()
        tau_m = list()
        tau_re = list()
        tau_syn_e = list()
        tau_syn_i = list()
        v_reset = list()
        v_rest = list()

        for atom in range(0, nNeurons):
            cm.append(0.25)
            i_off.append(0.0 + atom * 0.01)
            tau_m.append(10.0 + atom // 2 * 0.1)
            tau_re.append(2.0 + atom % 2 * 0.01)
            tau_syn_e.append(0.5)
            tau_syn_i.append(0.5 + atom * 0.01)
            v_reset.append(-65.0 + atom // 2 * 0.01)
            v_rest.append(-65.0 + atom % 2 * 0.01)

        gbar_na_distr = RandomDistribution('normal', (20.0, 2.0),
                                           rng=NumpyRNG(seed=85524))

        cell_params_lif = {'cm': 0.25, 'i_offset': i_off, 'tau_m': tau_m,
                           'tau_refrac': tau_re, 'v_thresh': gbar_na_distr}

        pop_1 = p.Population(
            nNeurons, p.IF_curr_exp, cell_params_lif, label='pop_1')

        pop_1.set(tau_syn_E=0.5)
        pop_1.set(tau_syn_I=tau_syn_i)
        pop_1.set(v_reset=v_reset, v_rest=v_rest)
        p.run(1)

        self.assertEquals(cm, pop_1.get("cm"))
        self.assertEquals(i_off, pop_1.get("i_offset"))
        self.assertEquals(tau_m, pop_1.get("tau_m"))
        self.assertEquals(tau_re, pop_1.get("tau_refrac"))
        self.assertEquals(tau_syn_e, pop_1.get("tau_syn_E"))
        self.assertEquals(tau_syn_i, pop_1.get("tau_syn_I"))
        self.assertEquals(v_reset, pop_1.get("v_reset"))
        self.assertEquals(v_rest, pop_1.get("v_rest"))
        self.assertGreater(len(set(pop_1.get("v_thresh"))), nNeurons/2)
        p.end()

    def test_run(self):
        self.runsafe(self.do_run)