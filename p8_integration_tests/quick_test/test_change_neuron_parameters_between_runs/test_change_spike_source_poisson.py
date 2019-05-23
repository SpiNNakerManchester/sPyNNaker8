import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


class TestChangeSpikeSourcePoisson(BaseTestCase):

    def with_reset(self):
        p.setup(1.0)

        inp = p.Population(
            100, p.SpikeSourcePoisson(rate=100), label="input")
        inp.record("spikes")
        p.run(100)
        spikes1 = inp.spinnaker_get_data('spikes')
        p.reset()
        inp.set(rate=10)
        p.run(100)
        spikes2 = inp.spinnaker_get_data('spikes')
        p.end()
        assert len(spikes1) > len(spikes2) * 5

    def test_with_reset(self):
        self.runsafe(self.with_reset)

    def no_reset(self):
        p.setup(1.0)

        inp = p.Population(
            100, p.SpikeSourcePoisson(rate=100), label="input")
        inp.record("spikes")
        p.run(100)
        spikes1 = inp.spinnaker_get_data('spikes')
        inp.set(rate=10)
        p.run(100)
        spikes2 = inp.spinnaker_get_data('spikes')
        assert len(spikes1) > (len(spikes2)-len(spikes1)) * 5
        p.end()

    def test_no_reset(self):
        self.runsafe(self.no_reset)
