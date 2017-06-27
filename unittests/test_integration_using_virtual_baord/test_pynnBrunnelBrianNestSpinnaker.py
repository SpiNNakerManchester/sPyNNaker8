from p8_integration_tests.base_test_case import BaseTestCase
import p8_integration_tests.scripts.pynnBrunnelBrianNestSpinnaker as script

Neurons = 3000  # number of neurons in each population
sim_time = 1000
simulator_Name = 'spiNNaker'


class PynnBrunnelBrianNestSpinnaker(BaseTestCase):

    # AttributeError: 'SpikeSourcePoisson' object has no attribute 'describe'
    def test_run(self):
        script.do_run(Neurons, sim_time, record=True)


if __name__ == '__main__':
    script.do_run(Neurons, sim_time, record=True)
