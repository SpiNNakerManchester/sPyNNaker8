import spynnaker8 as p
import numpy as np

#pre_rate = 100
n_nrn = 1

p.setup(1)

simtime = 100

pop_src2 = p.Population(n_nrn, p.SpikeSourcePoisson(rate=100), label="drive")
pop_ex = p.Population(n_nrn, p.IF_curr_exp(), label="test")
proj2 = p.Projection(pop_src2,  pop_ex,  p.OneToOneConnector(),
               synapse_type=p.StaticSynapse(weight=2.0),  receptor_type='excitatory')




pop_src2.record('spikes')
pop_ex.record('spikes')
p.run(simtime)
trains2 = pop_src2.get_data('spikes')
trains = pop_ex.get_data('spikes').segments[0].spiketrains
p.reset()
p.run(simtime)
print 2
trains2 = pop_src2.get_data('spikes')
trains = pop_ex.get_data('spikes').segments[0].spiketrains
p.end();

print "\n job done"