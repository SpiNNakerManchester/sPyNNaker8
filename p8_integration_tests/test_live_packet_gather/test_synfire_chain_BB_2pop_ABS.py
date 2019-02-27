#!/usr/bin/python
import numpy
import spynnaker8 as p
from spynnaker8.utilities import neo_convertor
from p8_integration_tests.base_test_case import BaseTestCase


def do_run(plot):
    p.setup(timestep=1.0)

    # n_pop = 2  # 60
    nNeurons = 10  # 100

    rng = p.NumpyRNG(seed=28374)
    # rng1 = p.NumpyRNG(seed=12345)

    # delay_distr = p.RandomDistribution('uniform', [5, 10], rng)
    # weight_distr = p.RandomDistribution('uniform', [0, 2], rng1)

    v_distr = p.RandomDistribution('uniform', [-55, -95], rng)

    v_inits = []
    for i in range(nNeurons):
        v_inits.append(v_distr.next())

    cell_params_lif_in = {
                          'tau_m':      32,
                          'v': -80,
                          'v_rest': -75,
                          'v_reset': -95,
                          'v_thresh': -55,
                          'tau_syn_E':  5,
                          'tau_syn_I':  10,
                          'tau_refrac': 20,
                          'i_offset':   1
                          }

    cell_params_lif = {'tau_m':       32,
                       'v': -80,
                       'v_rest': -75,
                       'v_reset': -95,
                       'v_thresh': -55,
                       'tau_syn_E':   5,
                       'tau_syn_I':   10,
                       'tau_refrac':  5,
                       'i_offset':    0
                       }

    cell_params_ext_dev = {'port': 34567}

    populations = list()
    projections = list()

    weight_to_spike = 20

    populations.append(
        p.Population(
            nNeurons, p.IF_curr_exp(**cell_params_lif_in), label='pop_%d' % 0))
    populations[0].initialize(v=v_distr)

    p.external_devices.activate_live_output_for(populations[0])

    pop_external = p.Population(
        nNeurons, p.external_devices.SpikeInjector(),
        additional_parameters=cell_params_ext_dev,
        label='Babel_Dummy')

    populations.append(
        p.Population(nNeurons, p.IF_curr_exp(**cell_params_lif),
                     label='pop_%d' % 1))

    projections.append(
        p.Projection(pop_external, populations[1], p.OneToOneConnector(),
                     p.StaticSynapse(weight=weight_to_spike, delay=10)))

    # populations[0].record_v()
    #  at the moment is only possible to observe one population per core
    populations[1].record(['v'])

    for pop in populations:
        pop.record(['spikes'], to_file=False)
        # sends spike to the Monitoring application

    #    populations[i].record_variable('rate', save_to='eth')
    #  sends spike to the Monitoring application

    p.run(10000)

    # retrieving spike results and plotting...

    id_accumulator = 0

    shapes = []

    if plot:
        import matplotlib.pyplot as p_plot
    for pop_o in populations:
        data = numpy.asarray(neo_convertor.convert_spikes(
            pop_o.get_data('spikes')))
        print(data.shape)
        shapes.append(data.shape)
        if plot:
            p_plot.scatter(data[:, 0], data[:, 1] + id_accumulator,
                           color='green', s=1)
        id_accumulator = id_accumulator + pop_o.size

    if plot:
        p_plot.show()

    return shapes


class SynfireChainBB2popABStest(BaseTestCase):

    def test_synfire_chain_BB_2pop_ABS_test(self):
        shapes = do_run(plot=False)
        self.assertEqual((1493, 2), shapes[0])
        self.assertEqual((0, 2), shapes[1])


if __name__ == '__main__':
    do_run(plot=True)
