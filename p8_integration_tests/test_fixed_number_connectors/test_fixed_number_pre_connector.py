from __future__ import print_function
import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
import pylab
import numpy
import pyNN.random


def do_run(plot):

    p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
    p.set_number_of_neurons_per_core(p.IF_cond_exp, 100)

    # Experiment Parameters
    rng = pyNN.random.NumpyRNG(seed=124578)

    n_groups = 6  # Number of Synfire Groups
    n_exc = 100  # Number of excitatory neurons per group
    n_inh = 25  # Number of inhibitory neurons per group

    sim_duration = 500.

    # defining the initial pulse-packet
    pp_a = 5  # Nr of pulses in the packet
    pp_sigma = 5.0  # sigma of pulse-packet
    pp_start = 50.  # start = center of pulse-packet

    # Neuron Parameters as in Kremkow et al. paper
    cell_params = {'cm': 0.290,  # nF
                   'tau_m': 290.0/29.0,  # pF / nS = ms
                   'v_rest': -70.0,  # mV
                   'v_thresh': -57.0,  # mV
                   'tau_syn_E': 1.5,  # ms
                   'tau_syn_I': 10.0,  # ms
                   'tau_refrac': 2.0,  # ms
                   'v_reset': -70.0,  # mV
                   'e_rev_E': 0.0,  # mV
                   'e_rev_I': -75.0,  # mV
                   }

    weight_exc = 0.001  # uS weight for excitatory to excitatory connections
    weight_inh = 0.002  # uS weight for inhibitory to excitatory connections

    # list of excitatory populations
    exc_pops = []
    # list of inhibitory populations
    inh_pops = []
    # and Assembly of all populations
    all_populations = []

    # Create Groups
    print("Creating ", n_groups, " SynfireGroups")
    for group_index in range(n_groups):
        # create the excitatory Population
        exc_pop = p.Population(n_exc, p.IF_cond_exp(**cell_params),
                               label=("pop_exc_%s" % group_index))

        exc_pops.append(exc_pop)  # append to excitatory populations
        all_populations += [exc_pop]  # and to the Assembly

        # create the inhibitory Population
        inh_pop = p.Population(n_inh, p.IF_cond_exp(**cell_params),
                               label=("pop_inh_%s" % group_index))
        inh_pops.append(inh_pop)
        all_populations += [inh_pop]

        # connect Inhibitory to excitatory Population
        p.Projection(inh_pop, exc_pop,
                     p.AllToAllConnector(),
                     synapse_type=p.StaticSynapse(weight=weight_inh, delay=8.),
                     receptor_type='inhibitory')

    # Create Stimulus and connect it to first group
    print("Create Stimulus Population")
    # We create a Population of SpikeSourceArrays of the same dimension
    # as excitatory neurons in a synfire group
    pop_stim = p.Population(n_exc, p.SpikeSourceArray({}), label="pop_stim")

    # We create a normal distribution around pp_start with sigma = pp_sigma
    rd = pyNN.random.RandomDistribution(
        'normal', [pp_start, pp_sigma], rng=rng)
    all_spiketimes = []
    # for each cell in the population, we take pp_a values from the
    # random distribution
    for cell in range(len(pop_stim)):
        spiketimes = []
        for pulse in range(pp_a):
            spiketimes.append(rd.next())  # draw from the random distribution
        spiketimes.sort()
        all_spiketimes.append(spiketimes)

    # convert into a numpy array
    all_spiketimes = numpy.array(all_spiketimes)
    # 'topographic' setting of parameters.
    # all_spiketimes must have the same dimension as the Population
    pop_stim.set(spike_times=all_spiketimes)

    # Connect Groups with the subsequent ones
    print("Connecting Groups with subsequent ones")
    for group_index in range(n_groups-1):
        p.Projection(exc_pops[group_index % n_groups],
                     exc_pops[(group_index+1) % n_groups],
                     p.FixedNumberPreConnector(60, rng=rng,
                                               with_replacement=True),
                     synapse_type=p.StaticSynapse(weight=weight_exc,
                                                  delay=10.),
                     receptor_type='excitatory')
        p.Projection(exc_pops[group_index % n_groups],
                     inh_pops[(group_index+1) % n_groups],
                     p.FixedNumberPreConnector(60, rng=rng,
                                               with_replacement=True),
                     synapse_type=p.StaticSynapse(weight=weight_exc,
                                                  delay=10.),
                     receptor_type='excitatory')

    # Make another projection for testing that connects to itself
    p.Projection(exc_pops[1], exc_pops[1],
                 p.FixedNumberPreConnector(60, rng=rng,
                                           allow_self_connections=False),
                 synapse_type=p.StaticSynapse(weight=weight_exc,
                                              delay=10.),
                 receptor_type='excitatory')

    # Connect the Stimulus to the first group
    print("Connecting Stimulus to first group")
    p.Projection(pop_stim, inh_pops[0],
                 p.FixedNumberPreConnector(20, rng=rng),
                 synapse_type=p.StaticSynapse(weight=weight_exc, delay=20.),
                 receptor_type='excitatory')
    p.Projection(pop_stim, exc_pops[0],
                 p.FixedNumberPreConnector(60, rng=rng),
                 synapse_type=p.StaticSynapse(weight=weight_exc, delay=20.),
                 receptor_type='excitatory')

    # Recording spikes
    pop_stim.record('spikes')

    for pop in all_populations:
        pop.record('spikes')

    # Run
    print("Run the simulation")
    p.run(sim_duration)

    # Get data
    print("Simulation finished, now collect all spikes and plot them")

    stim_spikes = pop_stim.spinnaker_get_data('spikes')
    stim_spikes[:, 0] -= n_exc

    # collect all spikes and make a raster_plot
    spklist_exc = []
    spklist_inh = []
    for group in range(n_groups):
        EXC_spikes = exc_pops[group].spinnaker_get_data('spikes')
        INH_spikes = inh_pops[group].spinnaker_get_data('spikes')
        EXC_spikes[:, 0] += group*(n_exc+n_inh)
        INH_spikes[:, 0] += group*(n_exc+n_inh) + n_exc
        spklist_exc += EXC_spikes.tolist()
        spklist_inh += INH_spikes.tolist()

    # Plot
    if plot:
        pylab.figure()
        pylab.plot([i[1] for i in spklist_exc],
                   [i[0] for i in spklist_exc], "r.")
        pylab.plot([i[1] for i in spklist_inh],
                   [i[0] for i in spklist_inh], "b.")
        pylab.plot([i[1] for i in stim_spikes],
                   [i[0] for i in stim_spikes], "k.")
        pylab.xlabel('Time/ms')
        pylab.ylabel('spikes')
        pylab.title('spikes')

        for group in range(n_groups):
            pylab.axhline(y=(group+1)*(n_exc+n_inh), color="lightgrey")
            pylab.axhline(y=(group+1)*(n_exc+n_inh)-n_inh, color="lightgrey")

        pylab.axhline(y=0, color="grey", linewidth=1.5)
        pylab.show()

    p.end()

    return stim_spikes, spklist_exc, spklist_inh


class FixedNumberPreConnectorTest(BaseTestCase):
    def test_run(self):
        stim_spikes, spklist_exc, spklist_inh = do_run(plot=False)
        # any checks go here
        self.assertEquals(500, len(stim_spikes))
        # CB Jan 15 2019 Was 1348
        self.assertEquals(1367, len(spklist_exc))
        self.assertEquals(291, len(spklist_inh))


if __name__ == '__main__':
    stim_spikes, spklist_exc, spklist_inh = do_run(plot=True)
    print(len(stim_spikes), len(spklist_exc), len(spklist_inh))
