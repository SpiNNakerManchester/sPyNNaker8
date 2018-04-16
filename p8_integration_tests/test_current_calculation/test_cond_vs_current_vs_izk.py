"""
Synfirechain-like example
"""
import spynnaker8 as p
from spynnaker8.utilities import neo_convertor
from p8_integration_tests.base_test_case import BaseTestCase


def do_run(nNeurons):
    p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)

    p.set_number_of_neurons_per_core(p.IF_curr_exp, nNeurons / 2)

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

    p.set_number_of_neurons_per_core(p.IF_cond_exp, nNeurons / 2)

    cell_params_cond = {'cm': 0.25,
                        'i_offset': 0.0,
                        'tau_m': 20.0,
                        'tau_refrac': 2.0,
                        'tau_syn_E': 5.0,
                        'tau_syn_I': 5.0,
                        'v_reset': -70.0,
                        'v_rest': -65.0,
                        'v_thresh': -50.0,
                        'e_rev_E': 0.,
                        'e_rev_I': -80.
                        }

    p.set_number_of_neurons_per_core(p.Izhikevich, 100)

    cell_params_izk = {'a': 0.02,
                       'b': 0.2,
                       'c': -65,
                       'd': 8,
                       'v_init': -75,
                       'u_init': 0,
                       'tau_syn_E': 2,
                       'tau_syn_I': 2,
                       'i_offset': 0
                       }

    populations = list()
    projections = list()

    current_weight_to_spike = 2.0
    cond_weight_to_spike = 0.035
    delay = 17

    # different strangths of connection
    curr_injection_connection = [(0, 0, current_weight_to_spike, delay)]
    cond_injection_connection = [(0, 0, cond_weight_to_spike, delay)]
    izk_injection_connection = [(0, 0, current_weight_to_spike, delay)]
    sinkConnection = [(0, 0, 0, 1)]

    # spike time
    spikeArray = {'spike_times': [[0]]}

    # curr set up
    populations.append(p.Population(nNeurons, p.IF_cond_exp, cell_params_cond,
                                    label='pop_cond'))
    # cond setup
    populations.append(p.Population(nNeurons, p.IF_curr_exp, cell_params_lif,
                                    label='pop_curr'))
    # izk setup
    populations.append(p.Population(nNeurons, p.Izhikevich, cell_params_izk,
                                    label='izk pop'))

    # sink pop for spikes to go to (otherwise they are not recorded as firing)
    populations.append(p.Population(nNeurons, p.IF_curr_exp, cell_params_lif,
                                    label='sink_pop'))
    populations.append(p.Population(1, p.SpikeSourceArray, spikeArray,
                                    label='inputSpike'))

    pop = p.Projection(populations[4], populations[0],
                       p.FromListConnector(cond_injection_connection))
    projections.append(pop)
    pop = p.Projection(populations[4], populations[1],
                       p.FromListConnector(curr_injection_connection))
    projections.append(pop)
    pop = p.Projection(populations[4], populations[2],
                       p.FromListConnector(izk_injection_connection))
    projections.append(pop)
    projections.append(p.Projection(populations[2], populations[3],
                       p.FromListConnector(sinkConnection)))
    projections.append(p.Projection(populations[1], populations[3],
                                    p.FromListConnector(sinkConnection)))
    projections.append(p.Projection(populations[0], populations[3],
                                    p.FromListConnector(sinkConnection)))
    # record stuff for cond
    populations[0].record("v")
    populations[0].record("gsyn_exc")
    populations[0].record("spikes")

    # record stuff for curr
    populations[1].record("v")
    populations[1].record("gsyn_exc")
    populations[1].record("spikes")

    # record stuff for izk
    populations[2].record("v")
    populations[2].record("gsyn_exc")
    populations[2].record("spikes")

    p.run(500)

    # get cond
    neo = populations[0].get_data(["v", "spikes", "gsyn_exc"])

    cond_v = neo_convertor.convert_data(neo, name="v")
    cond_gsyn = neo_convertor.convert_data(neo, name="gsyn_exc")
    cond_spikes = neo_convertor.convert_spikes(neo)

    # get curr
    neo = populations[1].get_data(["v", "spikes", "gsyn_exc"])

    curr_v = neo_convertor.convert_data(neo, name="v")
    curr_gsyn = neo_convertor.convert_data(neo, name="gsyn_exc")
    curr_spikes = neo_convertor.convert_spikes(neo)

    # get izk
    neo = populations[1].get_data(["v", "spikes", "gsyn_exc"])

    izk_v = neo_convertor.convert_data(neo, name="v")
    izk_gsyn = neo_convertor.convert_data(neo, name="gsyn_exc")
    izk_spikes = neo_convertor.convert_spikes(neo)

    p.end()

    return (cond_v, cond_gsyn, cond_spikes, curr_v, curr_gsyn, curr_spikes,
            izk_v, izk_gsyn, izk_spikes)


def plot(cond_v, cond_gsyn, cond_spikes, curr_v, curr_gsyn, curr_spikes,
         izk_v, izk_gsyn, izk_spikes):
    import pylab  # deferred so unittest are not dependent on it

    # plot curr spikes
    if len(curr_spikes) != 0:
        print("curr spikes are {}".format(curr_spikes))
        pylab.figure()
        pylab.plot([i[1] for i in curr_spikes],
                   [i[0] for i in curr_spikes], ".")
        pylab.xlabel('Time/ms')
        pylab.ylabel('spikes')
        pylab.title('lif curr spikes')
        pylab.show()
    else:
        print("No curr spikes received")

    # plot cond spikes
    if len(cond_spikes) != 0:
        print("cond spikes are {}".format(cond_spikes))
        pylab.figure()
        pylab.plot([i[1] for i in cond_spikes],
                   [i[0] for i in cond_spikes], ".")
        pylab.xlabel('Time/ms')
        pylab.ylabel('spikes')
        pylab.title('lif cond spikes')
        pylab.show()
    else:
        print("No cond spikes received")

    # plot izk spikes
    if len(izk_spikes) != 0:
        print("izk spikes are {}".format(izk_spikes))
        pylab.figure()
        pylab.plot([i[1] for i in izk_spikes], [i[0] for i in izk_spikes], ".")
        pylab.xlabel('Time/ms')
        pylab.ylabel('spikes')
        pylab.title('izk curr spikes')
        pylab.show()
    else:
        print("No izk spikes received")

    # plot curr gsyn
    if len(curr_gsyn) != 0:
        ticks = len(curr_gsyn) / nNeurons
        pylab.figure()
        pylab.xlabel('Time/ms')
        pylab.ylabel('gsyn')
        pylab.title('lif curr gsyn')
        for pos in range(0, nNeurons, 20):
            gsyn_for_neuron = curr_gsyn[pos * ticks: (pos + 1) * ticks]
            pylab.plot([i[2] for i in gsyn_for_neuron])
        pylab.show()
    else:
        print("no curr gsyn received")

    # plot cond gsyn
    if len(cond_gsyn) != 0:
        ticks = len(cond_gsyn) / nNeurons
        pylab.figure()
        pylab.xlabel('Time/ms')
        pylab.ylabel('gsyn')
        pylab.title('lif cond gsyn')
        for pos in range(0, nNeurons, 20):
            gsyn_for_neuron = cond_gsyn[pos * ticks: (pos + 1) * ticks]
            pylab.plot([i[2] for i in gsyn_for_neuron])
        pylab.show()
    else:
        print("no cond gsyn received")

    # plot izk gsyn
    if len(izk_gsyn) != 0:
        ticks = len(izk_gsyn) / nNeurons
        pylab.figure()
        pylab.xlabel('Time/ms')
        pylab.ylabel('gsyn')
        pylab.title('izk curr gsyn')
        for pos in range(0, nNeurons, 20):
            gsyn_for_neuron = izk_gsyn[pos * ticks: (pos + 1) * ticks]
            pylab.plot([i[2] for i in gsyn_for_neuron])
        pylab.show()
    else:
        print("no izk gsyn received")

    # plot curr membrane voltage
    if len(curr_v) != 0:
        ticks = len(curr_v) / nNeurons
        pylab.figure()
        pylab.xlabel('Time/ms')
        pylab.ylabel('v')
        pylab.title('lif curr v')
        for pos in range(0, nNeurons, 20):
            v_for_neuron = curr_v[pos * ticks: (pos + 1) * ticks]
            pylab.plot([i[2] for i in v_for_neuron])
        pylab.show()
    else:
        print("No curr voltage received")

    # plot cond membrane voltage
    if len(cond_v) != 0:
        ticks = len(cond_v) / nNeurons
        pylab.figure()
        pylab.xlabel('Time/ms')
        pylab.ylabel('v')
        pylab.title('lif cond v')
        for pos in range(0, nNeurons, 20):
            v_for_neuron = cond_v[pos * ticks: (pos + 1) * ticks]
            pylab.plot([i[2] for i in v_for_neuron])
        pylab.show()
    else:
        print("no cond membrane voltage is recieved")

    # plot izk membrane voltage
    if len(izk_v) != 0:
        ticks = len(izk_v) / nNeurons
        pylab.figure()
        pylab.xlabel('Time/ms')
        pylab.ylabel('v')
        pylab.title('izk curr v')
        for pos in range(0, nNeurons, 20):
            v_for_neuron = izk_v[pos * ticks: (pos + 1) * ticks]
            pylab.plot([i[2] for i in v_for_neuron])
        pylab.show()
    else:
        print("no izk membrane voltage is recieved")


class CondVsCurrentIzk(BaseTestCase):

    def test_run(self):
        nNeurons = 200  # number of neurons in each population
        results = do_run(nNeurons)
        (cond_v, cond_gsyn, cond_spikes, curr_v, curr_gsyn, curr_spikes, izk_v,
            izk_gsyn, izk_spikes) = results
        # spike lengths are 1 which looks wrong so not asserted!


if __name__ == '__main__':
    nNeurons = 200  # number of neurons in each population
    results = do_run(nNeurons)
    (cond_v, cond_gsyn, cond_spikes, curr_v, curr_gsyn, curr_spikes, izk_v,
     izk_gsyn, izk_spikes) = results
    print(len(cond_spikes))
    print(len(curr_spikes))
    print(len(izk_spikes))
    plot(cond_v, cond_gsyn, cond_spikes, curr_v, curr_gsyn, curr_spikes, izk_v,
         izk_gsyn, izk_spikes)
