"""
Script to demo why some connectors not tested virtually.

They do on machine generation so guess what they need!
"""
import spynnaker8 as sim
sim.setup(1.0)

pop1 = sim.Population(5, sim.IF_curr_exp(), {}, label="pop")
pop2 = sim.Population(4, sim.IF_curr_exp(), {}, label="pop")
synapse_type = sim.StaticSynapse(weight=5, delay=1)
# connector = sim.FromListConnector([[0,0,5,5]])
connector = sim.OneToOneConnector()

# connector = sim.FixedTotalNumberConnector(10, with_replacement=False)
# connector = sim.AllToAllConnector()

projection = sim.Projection(
    pop1, pop2, connector, synapse_type=synapse_type)
sim.run(10)
weights = projection.get(["weight"], "list")
try:
    print(weights)
except Exception as ex:
    print(ex)
sim.end()
