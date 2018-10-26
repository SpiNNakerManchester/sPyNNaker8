import spynnaker8 as p
import time
from random import randint
from collections import defaultdict
from six import iteritems
from p8_integration_tests.base_test_case import BaseTestCase
import unittest


class TestRecordableSpikeInjector(BaseTestCase):

    _n_spikes = defaultdict(lambda: 0)
    _n_neurons = 100

    def _inject(self, label, connection):
        time.sleep(0.1)
        for _ in range(5000):
            neuron_id = randint(0, self._n_neurons - 1)
            self._n_spikes[neuron_id] += 1
            connection.send_spike(label, neuron_id)
            time.sleep(0.001)
        print("Finished")

    def test_recordable_spike_injector(self):
        p.setup(1.0)
        pop = p.Population(
            self._n_neurons, p.external_devices.SpikeInjector(), label="input")
        pop.record("spikes")

        connection = p.external_devices.SpynnakerLiveSpikesConnection(
            send_labels=["input"])
        connection.add_start_callback("input", self._inject)

        p.run(10000)
        spikes = pop.get_data("spikes").segments[0].spiketrains

        p.end()

        spike_trains = dict()
        for spiketrain in spikes:
            i = spiketrain.annotations['source_index']
            if __name__ == "__main__":
                if self._n_spikes[i] != len(spiketrain):
                    print("Incorrect number of spikes, expected {} but got {}:"
                          .format(self._n_spikes[i], len(spiketrain)))
                    print(spiketrain)
            else:
                assert self._n_spikes[i] == len(spiketrain)
            spike_trains[i] = spiketrain

        for (index, count) in iteritems(self._n_spikes):
            if __name__ == "__main__":
                if index not in spike_trains:
                    print("Neuron {} should have spiked {} times but didn't"
                          .format(index, count))
            else:
                assert index in spike_trains


if __name__ == "__main__":
    unittest.main()
