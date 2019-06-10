import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.patternSpiker import PatternSpiker


class TestSampling(BaseTestCase):

    def small(self):
        ps = PatternSpiker()
        sim.setup(timestep=1)
        simtime = 100
        spike_rate = 5
        spike_rec_indexes = [1, 3, 5, 7, 9, 10]
        v_rec_indexes = [0, 21, 32, 45]
        v_rate = 3
        pop = ps.create_population(
            sim, n_neurons=32 * 2, label="test",
            spike_rate=spike_rate, spike_rec_indexes=spike_rec_indexes,
            v_rate=v_rate, v_rec_indexes=v_rec_indexes)
        sim.run(simtime)
        ps.check(
            pop, simtime, spike_rate=spike_rate,
            spike_rec_indexes=spike_rec_indexes,
            v_rate=v_rate, v_rec_indexes=v_rec_indexes, is_view=False)
        sim.end()

    def test_small(self):
        self.runsafe(self.small)

    def multirun(self):
        ps = PatternSpiker()
        sim.setup(timestep=1)
        simtime = 32
        spike_rate = 5
        spike_rec_indexes = [1, 3, 5, 7, 9, 10]
        v_rec_indexes = [0, 21, 32, 45]
        v_rate = 3
        pop = ps.create_population(sim, n_neurons=32 * 2, label="test",
                                   spike_rate=spike_rate,
                                   spike_rec_indexes=spike_rec_indexes,
                                   v_rate=v_rate, v_rec_indexes=v_rec_indexes)
        sim.run(simtime)
        sim.run(simtime)
        sim.run(simtime)
        ps.check(pop, simtime * 3,
                 spike_rate=spike_rate, spike_rec_indexes=spike_rec_indexes,
                 v_rate=v_rate, v_rec_indexes=v_rec_indexes, is_view=False)
        ps.check(pop, simtime * 3,
                 spike_rate=spike_rate, spike_rec_indexes=spike_rec_indexes,
                 v_rate=v_rate, v_rec_indexes=v_rec_indexes, is_view=True)
        sim.end()

    def test_multirun(self):
        self.runsafe(self.multirun)

    def different_views(self):
        ps = PatternSpiker()
        sim.setup(timestep=1)
        simtime = 100
        pop = ps.create_population(
            sim, n_neurons=10, v_rec_indexes=[2, 4, 6, 8], label="test")
        sim.run(simtime)
        ps.check(pop, simtime, v_rec_indexes=[2, 3, 4], is_view=True,
                 missing=True)
        sim.end()

    def test_different_views(self):
        self.runsafe(self.different_views)

    def standard(self):
        ps = PatternSpiker()
        sim.setup(timestep=1)
        simtime = 100
        pop = ps.create_population(sim, n_neurons=32 * 4, label="test")
        sim.run(simtime)
        ps.check(pop, simtime)
        sim.end()

    def test_standard(self):
        self.runsafe(self.standard)
