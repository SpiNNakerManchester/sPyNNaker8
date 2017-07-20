from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as p


class SynfireIfCurrExp(BaseTestCase):

    def test_run(self):
        p.setup()
        p.Population(10, p.SpikeSourceArray, {'spike_times': [100, 200]},
                     label='messed up')


if __name__ == '__main__':
    w = SynfireIfCurrExp()
    w.test_run()
