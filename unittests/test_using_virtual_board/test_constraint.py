import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase


class TestConstraint(BaseTestCase):

    def test_placement_constraint(self):
        """
        test the get_placements call.

        """
        sim.setup(timestep=1.0)
        sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 50)

        pop_1 = sim.Population(200, sim.IF_curr_exp(), label="pop_1")
        pop_1.add_placement_constraint(x=1, y=1)
        input = sim.Population(1, sim.SpikeSourceArray(spike_times=[0]),
                               label="input")
        sim.Projection(input, pop_1, sim.AllToAllConnector(),
                       synapse_type=sim.StaticSynapse(weight=5, delay=1))
        simtime = 10
        sim.run(simtime)
        placements = self.get_placements("pop_1")
        sim.end()
        self.assertEqual(4, len(placements))
        for [x, y, _] in placements:
            self.assertEqual("1", x)
            self.assertEqual("1", y)
