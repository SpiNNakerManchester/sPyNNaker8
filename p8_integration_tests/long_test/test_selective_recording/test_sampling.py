import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.patternSpiker import PatternSpiker


class TestSampling(BaseTestCase):

    def test_big(self):
        ps = PatternSpiker()
        sim.setup(timestep=1)
        simtime = 10000
        spike_rate = 5
        n_neurons = 3200
        spike_rec_indexes = list(range(0, 1000, 2))\
                            + list(range(1000, 2000, 3)) \
                            + list(range(2000, 3000, 1)) \
                            + list(range(3000, 3200, 4))
        v_rec_indexes = list(range(0, 1000, 1))\
                            + list(range(1000, 2000, 3)) \
                            + list(range(2000, 3000, 4)) \
                            + list(range(3000, 3200, 2))
        v_rate = 3
        pop = ps.create_population(sim, n_neurons=n_neurons, label="test",
                                   spike_rate=spike_rate,
                                   spike_rec_indexes=spike_rec_indexes,
                                   v_rate=v_rate, v_rec_indexes=v_rec_indexes)
        sim.run(simtime)
        ps.check(pop, simtime,
                 spike_rate=spike_rate, spike_rec_indexes=spike_rec_indexes,
                 v_rate=v_rate, v_rec_indexes=v_rec_indexes, is_view=False)
