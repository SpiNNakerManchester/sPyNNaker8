import spynnaker8 as sim
# import neo_convertor

sim.setup(timestep=1)
pop_1 = sim.Population(1, sim.IF_curr_exp, {}, label="pop_1")
input = sim.Population(1, sim.SpikeSourceArray, {'spike_times': [[0]]},
                       label="input")
input_proj = sim.Projection(input, pop_1, sim.OneToOneConnector(),
                            synapse_type=sim.StaticSynapse(weight=5.0,
                                                           delay=1),
                            receptor_type="excitatory", source=None,
                            space=None)
loop = sim.Projection(pop_1, pop_1, sim.OneToOneConnector(),
                      synapse_type=sim.StaticSynapse(weight=5.0, delay=1),
                      receptor_type="excitatory", source=None,
                      space=None)

pop_1.record("spikes")
pop_1.record("v")
sim.run(20)
# old_neo = pop_1.get_data("all")
# old_spikes = neo_convertor.convert_spikes(old_neo)
old_spikes = pop_1.spinnaker_get_data("spikes")
print old_spikes
old_v = pop_1.spinnaker_get_data("v")
# old_v = neo_convertor.convert_data(old_neo, "v")
print old_v

loop = sim.Projection(input, pop_1, sim.FromListConnector([[0, 0, 5, 5]]),
                      synapse_type=sim.StaticSynapse(weight=5.0, delay=1),
                      receptor_type="excitatory", source=None,
                      space=None)
sim.reset()
sim.run(20)
# neo = pop_1.get_data("all")
# spikes = neo_convertor.convert_spikes(neo)
spikes = pop_1.spinnaker_get_data("spikes")
print spikes
# v = neo_convertor.convert_data(neo, "v")
v = pop_1.spinnaker_get_data("v")
print v

print "DONE"