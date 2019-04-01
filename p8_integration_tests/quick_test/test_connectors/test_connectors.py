import numpy
import spynnaker8 as sim
from spynnaker.pyNN.exceptions import SpynnakerException
from p8_integration_tests.base_test_case import BaseTestCase

SOURCES = 5
DESTINATIONS = 10
OVERFLOW = 6


class ConnectorsTest(BaseTestCase):

    def spike_received_count(self, v_line):
        counts = []
        for v in v_line:
            if v < -64:
                counts.append(0)
            elif v < -62.5:  # -63.0
                counts.append(1)
            elif v < -60.5:  # -61.0
                counts.append(2)
            elif v < -58:  # 59.0
                counts.append(3)
            elif v < -56:  # -57.0
                counts.append(4)
            elif v < -54:  # --55.0
                counts.append(5)
            else:
                counts.append(OVERFLOW)
        return counts

    def calc_spikes_received(self, v):
        counts = list()
        counts.append(self.spike_received_count(v[2]))
        counts.append(self.spike_received_count(v[22]))
        counts.append(self.spike_received_count(v[42]))
        counts.append(self.spike_received_count(v[62]))
        counts.append(self.spike_received_count(v[82]))
        return counts

    def check_counts(self, counts, connections, repeats):
        for count in counts:
            if not repeats:
                self.assertEqual(1, max(count))
        if max(count) < OVERFLOW:
            self.assertEqual(connections, sum(count))

    def check_connection(self, projection, destination, connections, repeats,
                         type, n_destinations=DESTINATIONS):
        neo = destination.get_data(["v"])
        v = neo.segments[0].filter(name="v")[0]
        weights = projection.get(["weight"], "list")
        counts = self.calc_spikes_received(v)

        expected = numpy.zeros([SOURCES, n_destinations])
        for (src, dest, _) in weights:
            expected[src][dest] += 1
        the_max = max(map(max, counts))
        if not numpy.array_equal(expected, counts):
            if the_max < OVERFLOW:
                print(counts)
                print(expected)
                raise AssertionError("Weights and v differ")

        for (source, destination, _) in weights:
            self.assertLess(source, SOURCES)
            self.assertLess(destination, n_destinations)
        if type == "post":
            self.assertEqual(connections * SOURCES, len(weights))
            self.check_counts(counts, connections, repeats)
        elif type == "pre":
            self.assertEqual(connections * n_destinations, len(weights))
            self.check_counts(numpy.transpose(counts), connections, repeats)
        elif type == "one":
            self.assertEqual(connections, len(weights))
            last_source = -1
            for (source, destination, _) in weights:
                self.assertNotEqual(source, last_source)
                last_source = source
                self.assertEqual(source, destination)
            while len(counts) > n_destinations:
                no_connections = counts.pop()
                self.assertEqual(0, sum(no_connections))
            self.check_counts(counts, 1, repeats)
        else:
            self.assertEqual(connections, len(weights))
            if not repeats:
                self.assertEqual(1, the_max)
            if the_max < OVERFLOW:
                self.assertEqual(connections, sum(map(sum, counts)))

    def check_connector(self, connector, connections, repeats, type="post",
                        n_destinations=DESTINATIONS):
        sim.setup(1.0)
        # sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 2)

        input = sim.Population(SOURCES, sim.SpikeSourceArray(
            spike_times=[[0], [20], [40], [60], [80]]), label="input")
        destination = sim.Population(
            n_destinations, sim.IF_curr_exp(
                tau_syn_E=1, tau_refrac=0,  tau_m=1),
            {}, label="destination")
        synapse_type = sim.StaticSynapse(weight=5, delay=1)
        projection = sim.Projection(
            input, destination, connector, synapse_type=synapse_type)
        destination.record("v")
        sim.run(100)
        self.check_connection(
            projection, destination, connections, repeats, type,
            n_destinations)
        sim.end()

    def one_to_one(self):
        connections = min(SOURCES, DESTINATIONS)
        with_replacement = False
        self.check_connector(
            sim.OneToOneConnector(), connections,  with_replacement,
            type="one")

    def test_one_to_one(self):
        self.runsafe(self.one_to_one)

    def one_to_one_short_destination(self):
        n_destinations = SOURCES-1
        connections = min(SOURCES, n_destinations)
        with_replacement = False
        self.check_connector(
            sim.OneToOneConnector(), connections, with_replacement,
            type="one", n_destinations=4)

    def test_one_to_one_short_destination(self):
        self.runsafe(self.one_to_one_short_destination)

    def total_connector_with_replacement(self):
        connections = 20
        with_replacement = True
        self.check_connector(
            sim.FixedTotalNumberConnector(
                connections, with_replacement=with_replacement),
            connections,  with_replacement, type="total")

    def test_total_connector_with_replacement(self):
        self.runsafe(self.total_connector_with_replacement)

    def total_connector_no_replacement(self):
        connections = 20
        with_replacement = False
        self.check_connector(
            sim.FixedTotalNumberConnector(
                connections, with_replacement=with_replacement),
            connections,  with_replacement, type="total")

    def test_total_connector_no_replacement(self):
        self.runsafe(self.total_connector_no_replacement)

    def total_connector_with_replacement_many(self):
        connections = 60
        with_replacement = True
        self.check_connector(
            sim.FixedTotalNumberConnector(
                connections, with_replacement=with_replacement),
            connections,  with_replacement, type="total")

    def test_total_connector_with_replacement_many(self):
        self.runsafe(self.total_connector_with_replacement_many)

    def total_connector_too_many(self):
        connections = 60
        with_replacement = False
        with self.assertRaises(SpynnakerException):
            self.check_connector(
                sim.FixedTotalNumberConnector(
                    connections, with_replacement=with_replacement),
                connections,  with_replacement, type="total")

    def test_total_connector_too_many(self):
        self.runsafe(self.total_connector_too_many)

    def multiple_connectors(self):
        n_destinations = 5
        sim.setup(1.0)
        input = sim.Population(SOURCES, sim.SpikeSourceArray(
            spike_times=[[0], [20], [40], [60], [80]]), label="input")
        destination = sim.Population(
            n_destinations, sim.IF_curr_exp(
                tau_syn_E=1, tau_refrac=0,  tau_m=1),
            {}, label="destination")
        synapse_type = sim.StaticSynapse(weight=5, delay=1)
        sim.Projection(
            input, destination, sim.OneToOneConnector(),
            synapse_type=synapse_type)
        sim.Projection(
            input, destination, sim.AllToAllConnector(),
            synapse_type=synapse_type)
        destination.record("v")
        sim.run(100)
        neo = destination.get_data(["v"])
        v = neo.segments[0].filter(name="v")[0]
        counts = self.calc_spikes_received(v)
        for i, count in enumerate(counts):
            for j in range(n_destinations):
                if i == j:
                    self.assertEqual(count[j], 2)
                else:
                    self.assertEqual(count[j], 1)
        sim.end()

    def test_multiple_connectors(self):
        self.runsafe(self.multiple_connectors)
