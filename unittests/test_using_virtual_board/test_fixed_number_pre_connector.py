import spynnaker8 as sim
from spynnaker.pyNN.exceptions import SpynnakerException
from p8_integration_tests.base_test_case import BaseTestCase

SOURCES = 5
DESTINATIONS = 10


class TestFixedNumberPreConnector(BaseTestCase):

    def check_weights(self, projection, connections, with_replacement,
                      allow_self_connections):
        weights = projection.get(["weight"], "list")
        print(weights)
        last_source = -1
        last_destination = -1
        for (source, destination, _) in weights:
            if source != last_source:
                last_source = source
            else:
                if not with_replacement:
                    self.assertNotEqual(last_destination, destination)
            last_destination = destination
            if not allow_self_connections:
                self.assertNotEqual(source, destination)

    def check_self_connect(self, connections, with_replacement,
                           allow_self_connections):
        sim.setup(1.0)
        pop = sim.Population(DESTINATIONS, sim.IF_curr_exp(), label="pop")
        synapse_type = sim.StaticSynapse(weight=5, delay=1)
        projection = sim.Projection(
            pop, pop, sim.FixedNumberPreConnector(
                connections, with_replacement=with_replacement,
                allow_self_connections=allow_self_connections),
            synapse_type=synapse_type)
        sim.run(0)
        self.check_weights(projection, connections, with_replacement,
                           allow_self_connections)
        sim.end()

    def check_other_connect(self, connections, with_replacement):
        sim.setup(1.0)
        pop1 = sim.Population(SOURCES, sim.IF_curr_exp(), label="pop1")
        pop2 = sim.Population(DESTINATIONS, sim.IF_curr_exp(), label="pop2")
        synapse_type = sim.StaticSynapse(weight=5, delay=1)
        projection = sim.Projection(
            pop1, pop2, sim.FixedNumberPreConnector(
                connections, with_replacement=with_replacement),
            synapse_type=synapse_type)
        sim.run(0)
        self.check_weights(projection, connections, with_replacement,
                           allow_self_connections=True)
        sim.end()

    def test_replace_self(self):
        with_replacement = True
        allow_self_connections = True
        self.check_self_connect(
            DESTINATIONS-2, with_replacement, allow_self_connections)

    def test_replace_no_self(self):
        with_replacement = True
        allow_self_connections = False
        self.check_self_connect(
            DESTINATIONS-2, with_replacement, allow_self_connections)

    def test_no_replace_self(self):
        with_replacement = True
        allow_self_connections = True
        self.check_self_connect(
            DESTINATIONS-2, with_replacement, allow_self_connections)

    def test_no_replace_no_self(self):
        with_replacement = True
        allow_self_connections = False
        self.check_self_connect(
            SOURCES-2, with_replacement, allow_self_connections)

    def test_with_many_replace_self(self):
        with_replacement = True
        allow_self_connections = True
        self.check_self_connect(
            DESTINATIONS+2, with_replacement, allow_self_connections)

    def test_all_no_replace_self(self):
        with_replacement = False
        allow_self_connections = True
        self.check_self_connect(
            SOURCES, with_replacement, allow_self_connections)

    def test_all_no_replace_no_self(self):
        with_replacement = False
        allow_self_connections = False
        with self.assertRaises(SpynnakerException):
            self.check_self_connect(
                DESTINATIONS, with_replacement, allow_self_connections)

    def test_all_replace_no_self(self):
        with_replacement = False
        allow_self_connections = True
        self.check_self_connect(
            DESTINATIONS, with_replacement, allow_self_connections)

    def test_replace_other(self):
        with_replacement = True
        self.check_other_connect(SOURCES-2, with_replacement)

    def test_no_replace_other(self):
        with_replacement = False
        self.check_other_connect(SOURCES-2, with_replacement)

    def test_replace_other_many(self):
        with_replacement = True
        self.check_other_connect(SOURCES+3, with_replacement)

    def test_no_replace_other_too_many(self):
        with_replacement = False
        with self.assertRaises(SpynnakerException):
            self.check_other_connect(SOURCES+3, with_replacement)
