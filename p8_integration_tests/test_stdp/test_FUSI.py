import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
import numpy as np
import math
import unittest


class TestFUSI(BaseTestCase):

    # input w_max is calculated: w_max = w_max * w_mult / n_inp
    # change the n_inp parameter to change input weights: to get w_max=0.1, n_inp should be set to 20
    shared_params = { 'w_min':0.0, 'w_max':1.0,  'w_drift': .0035, 'th_w':0.50,  'w_mult': 2.0, 'n_inp':20,
        'V_th':-55.0,  'Ca_th_l': 3.0, 'Ca_th_h1': 4.0, 'Ca_th_h2' : 13.0,
        'a_plus' : 0.15,  'a_minus': 0.15,
        'tau_Ca' : 150, 'J_Ca' : 1.0, 'V_reset' : -65.0,
        'w_drive' : 2.0
        }


    """
    A procedure that runs simulations for individual tests
    init_vals:    initial values for weight and neuron state
    runtime:        runtime
    expected_wgt:        correct weight for this test
    spike_times:    input spikes
    spike_times:    driving spikes
    test_name:    test name string to print in report
    atol:        atol, relative to w_max (atol = atol * w_max)
    """
    def run_one_test(self, init_vals, runtime, expected_wgt, spike_times, spike_times2,  test_name, atol = 0.01):
        p.setup(1)



        V0 = init_vals['V0']
        w0 = init_vals['w0']
        Ca0 = init_vals['Ca0']

        w_min = self.shared_params['w_min']
        w_max = self.shared_params['w_max']
        w_drift = self.shared_params['w_drift']
        th_w = self.shared_params['th_w']
        V_th = self.shared_params['V_th']
        Ca_th_l = self.shared_params['Ca_th_l']
        Ca_th_h1 = self.shared_params['Ca_th_h1']
        Ca_th_h2 = self.shared_params['Ca_th_h2']
        tau_Ca = self.shared_params['tau_Ca']
        J_Ca = self.shared_params['J_Ca']
        V_reset = self.shared_params['V_reset']
        w_drive = self.shared_params['w_drive']

        a_plus = self.shared_params['a_plus']
        a_minus = self.shared_params['a_minus']

        n_inp = self.shared_params['n_inp']
        w_mult =self.shared_params['w_mult']
        w_mult = w_mult/n_inp

        runtime = runtime
        expected_wgt = expected_wgt* w_mult

        # Spike source to send spike via plastic synapse
        pop_src1 = p.Population(n_inp, p.SpikeSourceArray,
                                {'spike_times': spike_times}, label="src1")

        # Spike source to send spike via static synapse to make
        # post-plastic-synapse neuron fire
        pop_src2 = p.Population(1, p.SpikeSourceArray,
                                {'spike_times': spike_times2}, label="src2")

        # Post-plastic-synapse population
        cell_params = {"i_offset":0.0,  "tau_ca2":tau_Ca, "i_alpha":J_Ca, "i_ca2":Ca0,  'v_reset':V_reset}
        pop_exc = p.Population(1, p.extra_models.IFCurrExpCa2Concentration, cell_params, label="test")
        pop_exc.initialize(v=V0)

        # Create projections
        syn_plas = p.STDPMechanism(
            timing_dependence = p.PreOnly(A_plus = a_plus*w_max*w_mult, A_minus = a_minus*w_max*w_mult, th_v_mem=V_th, th_ca_up_l = Ca_th_l, th_ca_up_h = Ca_th_h2, th_ca_dn_l = Ca_th_l, th_ca_dn_h = Ca_th_h1),
            weight_dependence = p.WeightDependenceFusi(w_min=w_min*w_mult, w_max=w_max*w_mult, w_drift=w_drift*w_mult, th_w=th_w * w_mult), weight=w0*w_mult, delay=1.0)


        proj = p.Projection(
            pop_src1,
            pop_exc,
            p.AllToAllConnector(),
            synapse_type=syn_plas, receptor_type='excitatory'
            )

        proj2 = p.Projection(pop_src2,  pop_exc,  p.OneToOneConnector(),
               synapse_type=p.StaticSynapse(weight=w_drive),  receptor_type='excitatory')


        pop_src1.record('all')
        pop_exc.record("all")

        p.run(runtime)

        weight = proj.get('weight', 'list',
                                           with_address=False)[0]
        w_cur = expected_wgt
        print test_name,"weight exact: {}".format(w_cur)
        print "New weight SpiNNaker: {}".format(weight)
#         v = pop_exc.get_data('v').segments[0].filter(name='v')[0]
#         for i in range(len(v)):
#             print i, v[i]
        #print v[len(v)-1]
        self.assertTrue(np.allclose(weight,
                                      w_cur, atol=atol*w_max*w_mult))

        p.end()




    """
    Potentiation from w = w_min
    """
    def test_test1_wmin_potentiation(self):
        w0=0.0
        potentiation_1 = 0.15
        expected_weight = w0 + potentiation_1
        runtime = 97
        initial_vals = {'t0':0, 'V0':-65.0, 'Ca0': 3.0, 'w0' : w0 }
        spike_times2 = np.arange(10, 180, 10)
        spike_times = np.arange(96, 97, 30)
        self.run_one_test(initial_vals, runtime, expected_weight, spike_times, spike_times2, "Test 1:")


    """
    Drift to w_min + potentiation from w = w_min (no drift below w_min)
    """
    def test_test2_drift_wmin_potentiation(self):
        expected_weight = 0.15
        w0=0.15
        runtime = 186.0-97
        spike_times2 = np.arange(0, 180, 10)
        spike_times = np.arange(185, 190, 30)-97
        initial_vals = { 'V0':-51.15844727, 'Ca0': 3.115447998, 'w0' : w0 }
        self.run_one_test(initial_vals, runtime, expected_weight, spike_times, spike_times2, "Test 2:")

    """
    If weight is depressed below w_min, it is held at w_min
    """
    def test_test3_clip_depression(self):
        expected_weight = 0.0
        w0=0.15
        runtime = 20
        spike_times2 = np.arange(0, -2, 10)
        spike_times = np.arange(10, 12, 30)
        initial_vals = { 'V0':-55, 'Ca0': 4.0, 'w0' : w0 }
        self.run_one_test(initial_vals, runtime, expected_weight, spike_times, spike_times2, "Test 3:")

    """
    Multiple potentiation and depression events with drift down
    """
    def test_test4_drift_down_potentiation_depression(self):
        w_min = self.shared_params['w_min']
        w_max = self.shared_params['w_max']
        w_drift = self.shared_params['w_drift']
        th_w = self.shared_params['th_w']
        w_mult =self.shared_params['w_mult']
        a_plus = self.shared_params['a_plus']
        a_minus = self.shared_params['a_minus']

        w0=0.15
        expected_weight = (w0 + 3*a_plus -a_minus -w_drift*(100) )
        runtime = 101
        spike_times2 = np.arange(0, 70, 10)
        spike_times = np.arange(10, 180, 30)
        initial_vals = { 'V0':-55, 'Ca0': 4.0, 'w0' : w0 }
        self.run_one_test(initial_vals, runtime, expected_weight, spike_times, spike_times2, "Test 4:")

    """
    Multiple potentiations with drift down and up
    """
    def test_test5_long_potentiation_seq(self):
        w_min = self.shared_params['w_min']
        w_max = self.shared_params['w_max']
        w_drift = self.shared_params['w_drift']
        th_w = self.shared_params['th_w']
        w_mult =self.shared_params['w_mult']
        a_plus = self.shared_params['a_plus']
        a_minus = self.shared_params['a_minus']

        w0=0.2
        expected_weight = (w0 + 8*a_plus - w_drift*(160) +w_drift*(200-160) )
        runtime = 201
        spike_times2 = np.arange(0, 300, 10)
        spike_times = np.append(np.arange(10, 170, 30), [180, 200])
        initial_vals = { 'V0':-55, 'Ca0': 5.0, 'w0' : w0 }
        self.run_one_test(initial_vals, runtime, expected_weight, spike_times, spike_times2, "Test 5:")

    """
    Depression from w = w_max
    """
    def test_test6_wmax_depression(self):
        w0=1.0
        potentiation_1 = 0.15
        expected_weight = w0 - potentiation_1
        runtime = 21
        initial_vals = {'t0':0, 'V0':-65.0, 'Ca0': 4.0, 'w0' : w0 }
        spike_times2 = np.arange(10, 0, 10)
        spike_times = np.arange(20, 21, 30)
        self.run_one_test(initial_vals, runtime, expected_weight, spike_times, spike_times2, "Test 6:")


    """
    Drift to w_max + depression from w = w_max (no drift above w_max)
    """
    def test_test7_drift_wmax_depression(self):
        expected_weight = 1 - 0.15
        w0=1 - 0.15
        runtime = 51
        spike_times2 = np.arange(0, -5, 10)
        spike_times = np.arange(50, 200, 30)
        initial_vals = { 'V0':-65, 'Ca0': 5.0, 'w0' : w0 }
        self.run_one_test(initial_vals, runtime, expected_weight, spike_times, spike_times2, "Test 7:")

    """
    If weight is potentiated above w_max, it is held at w_max
    """
    def test_test8_clip_potentiation(self):
        expected_weight = 1.0
        w0=1.0-0.05
        runtime = 5
        spike_times2 = np.arange(0, -2, 10)
        spike_times = np.arange(4, 12, 30)
        initial_vals = { 'V0':-51, 'Ca0': 4.0, 'w0' : w0 }
        self.run_one_test(initial_vals, runtime, expected_weight, spike_times, spike_times2, "Test 8:")

    """
    Only drift down
    """
    def test_test9_just_drift_down(self):
        w_min = self.shared_params['w_min']
        w_max = self.shared_params['w_max']
        w_drift = self.shared_params['w_drift']
        th_w = self.shared_params['th_w']
        w_mult =self.shared_params['w_mult']
        w0=0.4
        runtime = 101
        expected_weight = w0 - (runtime-1) * w_drift
        spike_times2 = np.arange(0, -2, 10)
        spike_times = np.arange(100, 101, 10)
        initial_vals = { 'V0':-51, 'Ca0': 3.0, 'w0' : w0 }
        self.run_one_test(initial_vals, runtime, expected_weight, spike_times, spike_times2, "Test 9:")

    """
    Only drift up
    our minimum unit of weight is 0.00035, so scaled w0 should be >= scaled(0.5) + 0.00035;
    TODO: update this for the final version, where minimum weight will not be hardcoded
    """
    def test_testA_just_drift_up(self):
        w_min = self.shared_params['w_min']
        w_max = self.shared_params['w_max']
        w_drift = self.shared_params['w_drift']
        th_w = self.shared_params['th_w']
        w_mult =self.shared_params['w_mult']
        w0=0.5036
        runtime = 101
        expected_weight = w0 + (runtime-1) * w_drift
        spike_times2 = np.arange(0, -2, 10)
        spike_times = np.arange(100, 101, 10)
        initial_vals = { 'V0':-51, 'Ca0': 3.0, 'w0' : w0 }
        self.run_one_test(initial_vals, runtime, expected_weight, spike_times, spike_times2, "Test 10:")

    """
    Long test that performs all subtests in one 1 second long simulation
    (turned off for now)
    """
    def atest_long_test_potentiation_and_depression(self):
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

        a_plus = 0.15
        a_minus = 0.15

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
