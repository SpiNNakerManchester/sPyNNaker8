import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
import numpy as np
import math
import unittest


class TestFUSI(BaseTestCase):

    def test_potentiation_and_depression(self):
        p.setup(1)
        runtime = 1000

        w_min = 0.0
        w_max = 1.0
        w_drift = .0035
        th_w = 0.50
        w0 = 0.0
        w_mult = 2.0
        V_th = -55.0
        Ca_th_l = 3.0
        Ca_th_h1 = 4.0
        Ca_th_h2 = 13.0

        a_plus = 0.15 # relative change
        a_minus = 0.15 # relative change
        initial_weight = 0

        spike_times2 = np.append(np.append(np.append(np.arange(10, 180, 10),np.arange(200, 330, 10)), np.arange(350, 700, 10)), np.arange(800, 1000, 10) )
        spike_times = np.append(np.append([96], np.arange(160, 700, 30)),  [800,820, 823, 834])


        # Spike source to send spike via plastic synapse
        pop_src1 = p.Population(1, p.SpikeSourceArray,
                                {'spike_times': spike_times}, label="src1")

        # Spike source to send spike via static synapse to make
        # post-plastic-synapse neuron fire
        pop_src2 = p.Population(1, p.SpikeSourceArray,
                                {'spike_times': spike_times2}, label="src2")

        # Post-plastic-synapse population
        cell_params = {"i_offset":0.0,  "tau_ca2":150, "i_alpha":1., "i_ca2":3.,  'v_reset':-65}
        pop_exc = p.Population(1, p.extra_models.IFCurrExpCa2Concentration, cell_params, label="test")

        # Create projections
        syn_plas = p.STDPMechanism(
            timing_dependence = p.PreOnly(A_plus = a_plus*w_max*w_mult, A_minus = a_minus*w_max*w_mult, th_v_mem=V_th, th_ca_up_l = Ca_th_l, th_ca_up_h = Ca_th_h2, th_ca_dn_l = Ca_th_l, th_ca_dn_h = Ca_th_h1),
            weight_dependence = p.WeightDependenceFusi(w_min=w_min*w_mult, w_max=w_max*w_mult, w_drift=w_drift*w_mult, th_w=th_w * w_mult), weight=w0*w_mult, delay=1.0)


        proj = p.Projection(
            pop_src1,
            pop_exc,
            p.OneToOneConnector(),
            synapse_type=syn_plas, receptor_type='excitatory'
            )

        proj2 = p.Projection(pop_src2,  pop_exc,  p.OneToOneConnector(),
               synapse_type=p.StaticSynapse(weight=2.0),  receptor_type='excitatory')


        pop_src1.record('all')
        pop_exc.record("all")
        weights = []

        p.run(97)

        weights.append(proj.get('weight', 'list',
                                           with_address=False)[0])
        potentiation_1 = w_max * a_plus * w_mult
        w_cur = (w0 + potentiation_1)
        print "test1 weight exact: {}".format(w_cur)
        print "New weight SpiNNaker: {}".format(weights[0])
        # 1) potentiation from w_min
        self.assertTrue(np.allclose(weights[0],
                                      w_cur, atol=0.001))

        p.run(161.0-97)
        weights.append(proj.get('weight', 'list',
                                           with_address=False)[0])
        print "test2 weight exact: {}".format(w_cur)
        print "New weight SpiNNaker: {}".format(weights[1])
        # 2) drift to w_min + potentiation (no drift below w_min)
        self.assertTrue(np.allclose(weights[1],
                                      w_cur, atol=0.001))

        p.run(191-161)
        weights.append(proj.get('weight', 'list',
                                           with_address=False)[0])
        w_cur = w_min*w_mult
        print "test3 weight exact: {}".format(w_cur)
        print "New weight SpiNNaker: {}".format(weights[2])
        # 3) no depression below w_min
        self.assertTrue(np.allclose(weights[2],
                                      w_cur, atol=0.001))
#         p.run(221-191)
#         weights.append(proj.get('weight', 'list',
#                                            with_address=False)[0])
#         w_cur = w_mult*(w_min + 4*a_plus  -w_drift*(311-221) )
#         print "test4 weight exact: {}".format(w_cur)
#         print "New weight SpiNNaker: {}".format(weights[3])
#         # 3) potentiation+ drift down + potentiations
#         self.assertTrue(np.allclose(weights[3],
#                                       w_cur, atol=1))
#         p.run(222-221)
#         weights.append(proj.get('weight', 'list',
#                                            with_address=False)[0])
#         w_cur = w_mult*(w_min + 4*a_plus  -w_drift*(311-221) )
#         print "test4 weight exact: {}".format(w_cur)
#         print "New weight SpiNNaker: {}".format(weights[4])
#         print "drift: {}".format(weights[3]*2-weights[4] )
#         # 3) potentiation+ drift down + potentiations
#         self.assertTrue(np.allclose(weights[3],
#                                       w_cur, atol=0.001))
        p.run(341-191)
        weights.append(proj.get('weight', 'list',
                                           with_address=False)[0])
        w_cur = w_mult*(w_min + 4*a_plus -a_minus -w_drift*(341-221) )
        print "test4 weight exact: {}".format(w_cur)
        print "New weight SpiNNaker: {}".format(weights[3])
        # 4) potentiation+ drift down + potentiations + depression
        self.assertTrue(np.allclose(weights[3],
                                      w_cur, atol=0.1))

        p.run(671-341)
        weights.append(proj.get('weight', 'list',
                                           with_address=False)[0])
        w_cur = w_mult*(w_min + 10*a_plus  -w_drift*(611-371) +w_drift*(671-611))
        print "test5 weight exact: {}".format(w_cur)
        print "New weight SpiNNaker: {}".format(weights[4])
        # 5) potentiation+ drift down + potentiations + drift up + potentiation
        self.assertTrue(np.allclose(weights[4],
                                      w_cur, atol=0.1))

        p.run(821-671)
        weights.append(proj.get('weight', 'list',
                                           with_address=False)[0])
        w_cur = w_mult*(w_max - 2*a_minus  +w_drift*(821-801))
        print "test6 weight exact: {}".format(w_cur)
        print "New weight SpiNNaker: {}".format(weights[5])
        # 6) drift up to w_max + depressions + drift up
        self.assertTrue(np.allclose(weights[5],
                                      w_cur, atol=0.1))

        p.run(835-821)
        weights.append(proj.get('weight', 'list',
                                           with_address=False)[0])
        w_cur = w_mult*(w_max )
        print "test7 weight exact: {}".format(w_cur)
        print "New weight SpiNNaker: {}".format(weights[6])
        # 7) drift up + potentiations, no potentiation above w_max
        self.assertTrue(np.allclose(weights[6],
                                      w_cur, atol=0.001))

        p.end()


if __name__ == '__main__':
    unittest.main()
