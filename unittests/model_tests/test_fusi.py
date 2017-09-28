import spynnaker8 as p
import python.plot_utils as plot_utils
p.setup(1)


pop_src = p.Population(1, p.SpikeSourceArray, {'spike_times': [[1, 20]]}, label="src")
pop_ex = p.Population(1, p.IF_curr_exp, {}, label="test")


syn_plas = p.STDPMechanism(
     timing_dependence = p.PreOnly(),
        weight_dependence = p.WeightDependenceFusi(), weight=5.0, delay=5.0)

proj = p.Projection(
    pop_src, #_plastic,
    pop_ex,
    p.OneToOneConnector(),
    synapse_type=syn_plas, receptor_type='excitatory'
    )

pop_ex.record(['v', 'gsyn_exc', 'gsyn_inh', 'spikes'])

p.run(100)

v = pop_ex.get_data('v')
curr = pop_ex.get_data('gsyn_exc')
spikes = pop_ex.get_data('spikes')

p.end()
print "\n job done"