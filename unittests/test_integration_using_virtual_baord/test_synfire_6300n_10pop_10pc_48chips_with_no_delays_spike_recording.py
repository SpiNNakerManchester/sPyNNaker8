from p8_integration_tests.base_test_case import BaseTestCase
import p8_integration_tests.scripts.synfire_npop_run as synfire_npop_run

n_neurons = 10  # number of neurons in each population
n_pops = 630


class Synfire6300n10pop10pc48chipsNoDelaysSpikeRecording(BaseTestCase):

    def test_run(self):
        synfire_npop_run.do_run(n_neurons, n_pops=n_pops,
                                neurons_per_core=n_neurons)


if __name__ == '__main__':
    x = Synfire6300n10pop10pc48chipsNoDelaysSpikeRecording()
    x.test_run()
