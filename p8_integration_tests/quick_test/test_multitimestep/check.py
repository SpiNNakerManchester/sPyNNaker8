import spynnaker8 as sim
from p8_integration_tests.quick_test.test_multitimestep.multi_if_curr_exp_base import MultiIFCurrExpBase

sim.setup(timestep=1)
sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 3)
input = sim.Population(
    1, sim.SpikeSourceArray([4]), label="input",
#    additional_parameters={"timestep_in_us": 2200}
)
input.record("spikes")
pop_1 = sim.Population(9, MultiIFCurrExpBase(), label="pop_1")
#pop_1 = sim.Population(9, sim.IF_curr_exp(), label="pop_1")
pop_1.record(["spikes","v"])

proj = sim.Projection(input, pop_1, sim.AllToAllConnector(),
                      synapse_type=sim.StaticSynapse(weight=5, delay=6))
sim.run(33)

proj.get("delay", "list")
i_neo = input.get_data(variables=["spikes"])
i_spikes = i_neo.segments[0].spiketrains
print(i_spikes)

neo = pop_1.get_data(variables="all")
spikes = neo.segments[0].spiketrains
print(spikes)
v = neo.segments[0].filter(name='v')[0]
print(v)
sim.end()
