import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
from pyNN.random import NumpyRNG
from unittest import SkipTest


def do_run(split, seed=None):
    p.setup(1.0)

    if split:
        p.set_number_of_neurons_per_core(p.SpikeSourcePoisson, 27)
        p.set_number_of_neurons_per_core(p.IF_curr_exp, 22)

    inp = p.Population(100, p.SpikeSourcePoisson(rate=100),
                       label="input", additional_parameters={"seed": seed})
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
    vs = p.RandomDistribution(
        "uniform", [-65.0, -55.0], rng=NumpyRNG(seed=seed))
    pop.initialize(v=vs)

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
    except ImportError:
        print("matplotlib not installed so plotting skipped")


class TestChangeParameter(BaseTestCase):

    def test_no_split(self):
        results = do_run(split=False, seed=self._test_seed)
        (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2) = results
        self.assertEqual(911, len(pop_spikes1))
        self.assertEqual(1172, len(inp_spikes1))
        self.assertEqual(323, len(pop_spikes2))
        self.assertEqual(0, len(inp_spikes2))

    def test_split(self):
        results = do_run(split=True, seed=self._test_seed)
        (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2) = results
        self.assertEqual(879, len(pop_spikes1))
        self.assertEqual(1168, len(inp_spikes1))
        self.assertEqual(304, len(pop_spikes2))
        self.assertEqual(0, len(inp_spikes2))


if __name__ == '__main__':
    (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2) = do_run(
        split=False, seed=1)
    print(len(pop_spikes1), len(inp_spikes1), len(pop_spikes2),
          len(inp_spikes2))
    plot_spikes(pop_spikes1, inp_spikes1)
    plot_spikes(pop_spikes2, inp_spikes2)
    (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2) = do_run(
        split=True, seed=1)
    print(len(pop_spikes1), len(inp_spikes1), len(pop_spikes2),
          len(inp_spikes2))
    plot_spikes(pop_spikes1, inp_spikes1)
    plot_spikes(pop_spikes2, inp_spikes2)
