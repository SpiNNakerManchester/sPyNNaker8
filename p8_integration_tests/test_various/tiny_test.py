import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
from spynnaker8.utilities import neo_convertor


def do_run():
    p.setup(timestep=1, min_delay=1, max_delay=15)

    population = p.Population(1, p.SpikeSourceArray(spike_times=[[0]]),
                              label='inputSSA_1')

    if_pop = p.Population(2, p.IF_cond_exp(), label='pop_1')

    if_pop.record("spikes")
    p.Projection(population, if_pop, p.OneToOneConnector())

    p.run(30)
    all1 = if_pop.get_data("spikes")

    p.run(30)
    all2 = if_pop.get_data("spikes")

    p.end()

    return (all1, all2)


class TinyTest(BaseTestCase):

    def test_run(self):
        all1, all2 = do_run()


if __name__ == '__main__':
    all1, all2 = do_run()
    spikes1 = neo_convertor.convert_spiketrains(all1.segments[0].spiketrains)
    print spikes1
    spikes2 = neo_convertor.convert_spiketrains(all1.segments[0].spiketrains)
    print spikes2
    v1 = neo_convertor.convert_data(all1, name="v", run=0)
    print v1
    v2 = neo_convertor.convert_data(all1, name="v", run=1)
    print v2
