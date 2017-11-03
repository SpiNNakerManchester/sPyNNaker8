import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
from unittest import SkipTest


def do_run(split, rng=None):
    p.setup(1.0)

    if split:
        p.set_number_of_neurons_per_core(p.SpikeSourcePoisson, 27)
        p.set_number_of_neurons_per_core(p.IF_curr_exp, 22)

    inp = p.Population(100,
        p.SpikeSourcePoisson(rate=100, seed=int(rng.next() * 1000)),
        label="input")
    pop = p.Population(100, p.IF_curr_exp, {}, label="pop")

    p.Projection(inp, pop, p.OneToOneConnector(),
                 synapse_type=p.StaticSynapse(weight=5))

    pop.record("spikes")
    inp.record("spikes")

    p.run(100)

    inp.set(rate=10)
    # pop.set("cm", 0.25)
    pop.set(tau_syn_E=1)

    p.run(100)

    pop_spikes1 = pop.spinnaker_get_data('spikes')
    inp_spikes1 = inp.spinnaker_get_data('spikes')

    p.reset()

    inp.set(rate=0)
    pop.set(i_offset=1.0)
    pop.initialize(v=p.RandomDistribution("uniform", [-65.0, -55.0], rng=rng))

    p.run(100)

    pop_spikes2 = pop.spinnaker_get_data('spikes')
    inp_spikes2 = inp.spinnaker_get_data('spikes')

    p.end()

    return (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2)


def plot_spikes(pop_spikes, inp_spikes):
    try:
        import pylab  # deferred so unittest are not dependent on it
        pylab.subplot(2, 1, 1)
        pylab.plot(inp_spikes[:, 1], inp_spikes[:, 0], "r.")
        pylab.subplot(2, 1, 2)
        pylab.plot(pop_spikes[:, 1], pop_spikes[:, 0], "b.")
        pylab.show()
    except Exception:
        print "matplotlib not installed so plotting skipped"


class TestChangeParameter(BaseTestCase):

    def test_no_split(self):
        results = do_run(split=False, rng=self._rng)
        (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2) = results
        if self._test_seed == 1:
            self.assertEqual(1154, len(inp_spikes1))
            self.assertEqual(1108, len(pop_spikes1))
            self.assertEqual(300, len(pop_spikes2))
        else:
            try:
                self.assertLess(1100, len(pop_spikes1))
                self.assertGreater(1300, len(pop_spikes1))
                self.assertLess(1100, len(inp_spikes1))
                self.assertGreater(1300, len(inp_spikes1))
                self.assertLess(450, len(pop_spikes2))
                self.assertGreater(600, len(pop_spikes2))
            except Exception as ex:
                # Just in case the range failed
                raise SkipTest(ex)
        self.assertEqual(0, len(inp_spikes2))

    def test_split(self):
        results = do_run(split=True, rng=self._rng)
        (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2) = results
        if self._test_seed == 1:
            self.assertEqual(1206, len(inp_spikes1))
            self.assertEqual(1149, len(pop_spikes1))
            self.assertEqual(300, len(pop_spikes2))
        else:
            try:
                self.assertLess(1100, len(pop_spikes1))
                self.assertGreater(1300, len(pop_spikes1))
                self.assertLess(1100, len(inp_spikes1))
                self.assertGreater(1300, len(inp_spikes1))
                self.assertLess(450, len(pop_spikes2))
                self.assertGreater(600, len(pop_spikes2))
            except Exception as ex:
                # Just in case the range failed
                raise SkipTest(ex)
        self.assertEqual(0, len(inp_spikes2))


if __name__ == '__main__':
    (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2) = do_run()
    plot_spikes([pop_spikes1, inp_spikes1])
    plot_spikes([pop_spikes2, inp_spikes2])
