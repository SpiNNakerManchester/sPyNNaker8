from pyNN.random import NumpyRNG
import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase

def check_spikes1(spikes):
    count1 = 0
    count2 = 0
    for (neuron, time) in spikes:
        if time < 100:
            count1 += 1
        else:
            count2 += 1
    if count2 * 5 > count1:
        raise AssertionError(
            "Expected a lots less spike after set but found {} before and "
            "{} after".format(count1, count2))


def check_spikes(spikes):
    last_time = None
    counts = [0] * 200
    for (neuron, time) in spikes:
        counts[time] += 1
        if time < 100:
            last_time = None
            # For the first 100 all neurons spike at the same time
            if time not in [21, 50, 79]:
                print(spikes)
                raise AssertionError(
                    "Unxpected spike for neuron {} at time {}".format(
                        neuron, time))
        else:
            if last_time is not None:
                # For the second all neurons spike every 29 timesteps
                if time-last_time != 29:
                    print(spikes)
                    raise AssertionError(
                        "Unxpected spikes for neuron {} at times {} and {}".
                        format(neuron, last_time, time))
            last_time = time
    for time in range(100):
        # For the first 100 all neurons spike at the same time
        if time in [21, 50, 79]:
            if counts[time] != 100:
                "Expected 100 spikes at time {} but found".format(
                    time, counts[time])
        else:
            if counts[time] != 0:
                "Expected 0 spikes at time {} but found".format(
                    time, counts[time])
    for time in range(100, 200):
        # Now the neurons will fire at randomly different times.
        # more than half at the same time is technically possible but so rare!
        if counts[time] > 50:
            "Expected less 50 spikes at time {} but found".format(
                time, counts[time])


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

    # Turn off SpikeSourcePoisson
    inp.set(rate=0)
    # Set pop to be self spiking every 29 timesteps
    pop.set(i_offset=1.0)
    # start all the same which causes spikes at  21, 50, 79
    pop.initialize(v=-60)

    p.run(100)
    #Now stuffle the vs.
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
        self._test_seed = 2
        results = do_run(split=False, seed=self._test_seed)
        (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2) = results
        self.assertEqual(865, len(pop_spikes1))
        self.assertEqual(1020, len(inp_spikes1))
        self.assertEqual(0, len(inp_spikes2))
        check_spikes(pop_spikes2)

    def test_split(self):
        self._test_seed = 2
        results = do_run(split=True, seed=self._test_seed)
        (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2) = results
        # Range here as the order of the data generated in the cores could
        # change the output
        self.assertEqual(865, len(pop_spikes1))
        self.assertEqual(1012, len(inp_spikes1))
        self.assertEqual(0, len(inp_spikes2))
        check_spikes(pop_spikes2)


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
