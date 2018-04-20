from p8_integration_tests.base_test_case import BaseTestCase

import spynnaker8 as sim
from spynnaker8.utilities import neo_convertor
import spynnaker.plot_utils as plot_utils


def do_run(seed=None):
    sim.setup(timestep=1.0, min_delay=1.0, max_delay=1.0)

    simtime = 1000

    if seed is None:
        pg_pop1 = sim.Population(2, sim.SpikeSourcePoisson(
            rate=10.0, start=0, duration=simtime), label="pg_pop1")
        pg_pop2 = sim.Population(2, sim.SpikeSourcePoisson(
            rate=10.0, start=0, duration=simtime), label="pg_pop2")
    else:
        pg_pop1 = sim.Population(2, sim.SpikeSourcePoisson(
            rate=10.0, start=0, duration=simtime, seed=seed), label="pg_pop1")
        pg_pop2 = sim.Population(2, sim.SpikeSourcePoisson(
            rate=10.0, start=0, duration=simtime, seed=seed+1),
                                 label="pg_pop2")

    pg_pop1.record("spikes")
    pg_pop2.record("spikes")

    sim.run(simtime)

    neo = pg_pop1.get_data("spikes")
    spikes1 = neo_convertor.convert_spikes(neo)
    neo = pg_pop2.get_data("spikes")
    spikes2 = neo_convertor.convert_spikes(neo)

    sim.end()

    return (spikes1, spikes2)


class TestPoisson(BaseTestCase):

    def test_run(self):
        (spikes1, spikes2) = do_run(self._test_seed)
        self.assertEquals(19, len(spikes1))
        self.assertEquals(24, len(spikes2))


if __name__ == '__main__':
    (spikes1, spikes2) = do_run()
    print(len(spikes1))
    print(spikes1)
    print(len(spikes2))
    print(spikes2)
    plot_utils.plot_spikes([spikes1, spikes2])
