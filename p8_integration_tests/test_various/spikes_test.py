"""
Synfirechain-like example
"""
# !/usr/bin/python
import spynnaker8 as p
from spynnaker8.utilities import neo_convertor
from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker.plot_utils as plot_utils
import unittest

SPIKE_TIMES = [11, 22]


def do_run(nNeurons, timestep):

    spike_list = {'spike_times': SPIKE_TIMES}
    print(spike_list)
    p.setup(timestep=timestep, min_delay=timestep, max_delay=timestep*10)

    pop = p.Population(nNeurons, p.SpikeSourceArray, spike_list, label='input')

    pop.record("spikes")

    p.run(200)

    neo = pop.get_data("spikes")
    p.end()

    return neo


class SpikesTest(BaseTestCase):

    @unittest.skip("https://github.com/SpiNNakerManchester/sPyNNaker/issues/"
                   "335")
    def test_many(self):
        nNeurons = 100  # number of neurons in each population
        neo = do_run(nNeurons, timestep=1.0)
        spikes = neo_convertor.convert_spikes(neo)
        spikes = neo_convertor.convert_spikes(neo)
        self.assertEqual(nNeurons * len(SPIKE_TIMES), len(spikes))
        for i in range(0, len(spikes), 2):
            self.assertEqual(i/2, spikes[i][0])
            self.assertEqual(11, spikes[i][1])
            self.assertEqual(i/2, spikes[i+1][0])
            self.assertEqual(22, spikes[i+1][1])

    def test_few(self):
        nNeurons = 10  # number of neurons in each population
        neo = do_run(nNeurons, timestep=1.0)
        spikes = neo_convertor.convert_spikes(neo)
        self.assertEqual(nNeurons * len(SPIKE_TIMES), len(spikes))
        for i in range(0, len(spikes), 2):
            self.assertEqual(i/2, spikes[i][0])
            self.assertEqual(11, spikes[i][1])
            self.assertEqual(i/2, spikes[i+1][0])
            self.assertEqual(22, spikes[i+1][1])

    def test_slow(self):
        nNeurons = 1  # number of neurons in each population
        neo = do_run(nNeurons, timestep=10.0)
        spikes = neo_convertor.convert_spikes(neo)
        self.assertEqual(nNeurons * len(SPIKE_TIMES), len(spikes))
        for i in range(0, len(spikes), 2):
            self.assertEqual(i/2, spikes[i][0])
            # Note spike times rounded up to next timestep
            self.assertEqual(20, spikes[i][1])
            self.assertEqual(i/2, spikes[i+1][0])
            self.assertEqual(30, spikes[i+1][1])

    def test_fast(self):
        nNeurons = 1  # number of neurons in each population
        neo = do_run(nNeurons, timestep=0.1)
        spikes = neo_convertor.convert_spikes(neo)
        self.assertEqual(nNeurons * len(SPIKE_TIMES), len(spikes))
        for i in range(0, len(spikes), 2):
            self.assertEqual(i/2, spikes[i][0])
            self.assertEqual(11, spikes[i][1])
            self.assertEqual(i/2, spikes[i+1][0])
            self.assertEqual(22, spikes[i+1][1])


if __name__ == '__main__':
    nNeurons = 100  # number of neurons in each population
    neo = do_run(nNeurons)
    spikes = neo_convertor.convert_spikes()
    plot_utils.plot_spikes(spikes)
    print(spikes)
