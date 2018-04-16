from p8_integration_tests.base_test_case import BaseTestCase
import p8_integration_tests.scripts.pynnBrunnelBrianNestSpinnaker as script

Neurons = 3000  # number of neurons in each population
sim_time = 1000
simulator_Name = 'spiNNaker'
record = False


class PynnBrunnelBrianNestSpinnaker(BaseTestCase):

    def test_run(self):
        (esp, s, N_E) = script.do_run(Neurons, sim_time, record=record)
        self.assertIsNone(esp)
        self.assertIsNone(s)
        self.assertEquals(2400, N_E)


if __name__ == '__main__':
    (esp, s, N_E) = script.do_run(Neurons, sim_time, record=record)
    print(esp)
    print(s)
    print(N_E)
