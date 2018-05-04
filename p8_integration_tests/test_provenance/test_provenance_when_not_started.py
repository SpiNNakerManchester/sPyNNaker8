import spynnaker8 as p
from testfixtures import LogCapture
from p8_integration_tests.base_test_case import BaseTestCase


def do_run():
    # this test ensures there is too much dtcm used up, thus crashes during
    # initisation
    p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)

    input_pop = p.Population(1024, p.SpikeSourcePoisson, {'rate': 10}, "input")
    relay_on = p.Population(1024, p.IF_curr_exp, {}, "input")

    t_rule_LGN = p.SpikePairRule(tau_plus=17, tau_minus=34, A_plus=0.01,
                                 A_minus=0.0085)
    w_rule_LGN = p.AdditiveWeightDependence(w_min=0.0, w_max=0.3)
    stdp_model_LGN = p.STDPMechanism(timing_dependence=t_rule_LGN,
                                     weight_dependence=w_rule_LGN, weight=1)
    # TODO weights=1
    p.Projection(input_pop, relay_on, p.OneToOneConnector(),
                 synapse_type=stdp_model_LGN, receptor_type="excitatory")

    p.run(1000)
    p.end()


class ProvenanceWhenNotStartedTest(BaseTestCase):
    def test_error(self):
        with LogCapture() as lc:
            try:
                do_run()
                self.assertTrue(False)
            except Exception:
                self.assert_logs_messages(lc.records, "Out of DTCM",
                                          allow_more=True)


if __name__ == '__main__':
    do_run()
