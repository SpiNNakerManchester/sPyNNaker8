import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


def do_run():
    p.setup(timestep=1, min_delay=1, max_delay=15)

    population = p.Population(1, p.SpikeSourceArray(spike_times=[[0]]),
                              label='inputSSA_1')

    population.record("all")

    p.run(30)
    all = population.get_data("all")

    p.end()

    return all


class TestSpikeSourceArrayGetData(BaseTestCase):

    def test_run(self):
        all1 = do_run()
        print all1


if __name__ == '__main__':

    all1 = do_run()
