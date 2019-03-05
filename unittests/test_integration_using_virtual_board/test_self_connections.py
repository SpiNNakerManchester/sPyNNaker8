import spynnaker8 as sim
from spynnaker.pyNN.exceptions import SpynnakerException
from p8_integration_tests.base_test_case import BaseTestCase

DESTINATIONS = 10


class TestSelfConnection(BaseTestCase):

    def check_weights(self, projection, connections, with_replacement,
                      allow_self_connections):
        weights = projection.get(["weight"], "list")
        last_source = -1
        last_destination = -1
        count = connections
        for (source, destination, _) in weights:
            if source != last_source:
                self.assertEqual(connections, count)
                last_source = source
                count = 1
            else:
                count += 1
                if not with_replacement:
                    self.assertNotEqual(last_destination, destination)
            last_destination = destination
            if not allow_self_connections:
                self.assertNotEqual(source, destination)

        self.assertEqual(connections, count)

    def check_pre(self, connections, with_replacement, allow_self_connections):
        sim.setup(1.0)
        pop = sim.Population(DESTINATIONS, sim.IF_curr_exp(), label="pop")
        synapse_type = sim.StaticSynapse(weight=5, delay=1)
        projection = sim.Projection(
            pop, pop, sim.FixedNumberPostConnector(
                connections, with_replacement=with_replacement,
                allow_self_connections=allow_self_connections),
             synapse_type=synapse_type)
        sim.run(0)
        self.check_weights(projection, connections, with_replacement,
                           allow_self_connections)
        sim.end()

    def test_replace_self(self):
        with_replacement = True
        allow_self_connections = True
        self.check_pre(7, with_replacement, allow_self_connections )

    def test_replace_no_self(self):
        with_replacement = True
        allow_self_connections = False
        self.check_pre(7,  with_replacement, allow_self_connections)

    def test_no_replace_self(self):
        with_replacement = True
        allow_self_connections = True
        self.check_pre(7, with_replacement, allow_self_connections )

    def test_no_replace_no_self(self):
        with_replacement = True
        allow_self_connections = False
        self.check_pre(7,  with_replacement, allow_self_connections)

    def test_with_many_replace_self(self):
        with_replacement = True
        allow_self_connections = True
        self.check_pre(15,  with_replacement, allow_self_connections)

    def test_all_no_replace_self(self):
        with_replacement = False
        allow_self_connections = True
        self.check_pre(DESTINATIONS,  with_replacement, allow_self_connections)

    def test_all_no_replace_no_self(self):
        with_replacement = False
        allow_self_connections = False
        with self.assertRaises(SpynnakerException):
            self.check_pre(DESTINATIONS,  with_replacement,
                           allow_self_connections)
