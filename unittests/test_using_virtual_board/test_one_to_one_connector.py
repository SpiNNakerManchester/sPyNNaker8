import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase


class TestOneToOneConnector(BaseTestCase):

    def check_weights(self, projection, sources, destinations):
        weights = projection.get(["weight"], "list")
        last_source = -1
        for (source, destination, _) in weights:
            self.assertNotEqual(source, last_source)
            last_source = source
            self.assertEqual(source, destination)
            self.assertLess(source, sources)
            self.assertLess(destination, sources)
        self.assertEqual(len(weights), min(sources, destinations))

    def check_other_connect(self, sources, destinations):
        sim.setup(1.0)
        pop1 = sim.Population(sources, sim.IF_curr_exp(), label="pop1")
        pop2 = sim.Population(destinations, sim.IF_curr_exp(), label="pop2")
        synapse_type = sim.StaticSynapse(weight=5, delay=1)
        projection = sim.Projection(
            pop1, pop2, sim.OneToOneConnector(), synapse_type=synapse_type)
        sim.run(0)
        self.check_weights(projection, sources, destinations)
        sim.end()

    def test_same(self):
        self.check_other_connect(5, 5)

    # Does not work on VM
    # def test_less_sources(self):
    #    self.check_other_connect(5, 10)

    # Does not work on VM
    # def test_less_destinations(self):
    #    self.check_other_connect(10, 5)

    def test_many(self):
        self.check_other_connect(500, 500)
