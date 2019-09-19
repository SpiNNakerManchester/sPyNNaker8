# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
import scipy
import numpy


def array(value):
    return numpy.array(value).reshape(-1)


def do_run():
    p.setup(1.0)
    n_neurons = 2
    run_time = 20000
    seed = 0

    pop_a = p.Population(n_neurons, p.extra_models.SpikeSourcePoissonVariable(
        rates=[10, 20, 50],
        starts=[0, 5000, 10000]),
        label="pop_a",
        additional_parameters={"seed": seed})
    pop_a.record("spikes")

    pop_b = p.Population(n_neurons, p.extra_models.SpikeSourcePoissonVariable(
        rates=[[1, 2, 5], [10, 20, 50]],
        starts=[0, 5000, 10000]),
        label="pop_b",
        additional_parameters={"seed": seed})
    pop_b.record("spikes")

    pop_c = p.Population(n_neurons, p.extra_models.SpikeSourcePoissonVariable(
        rates=[10, 20, 50],
        starts=[100, 6000, 12000],
        durations=[5000, 5000, 5000]),
        label="pop_c",
        additional_parameters={"seed": seed})
    pop_c.record("spikes")

    pop_d = p.Population(n_neurons, p.extra_models.SpikeSourcePoissonVariable(
        rates=[[1, 2, 5], [10, 20, 50]],
        starts=[0, 5000, 10000],
        durations=[5000, 4000, 3000]),
        label="pop_d",
        additional_parameters={"seed": seed})
    pop_d.record("spikes")

    pop_e = p.Population(n_neurons, p.extra_models.SpikeSourcePoissonVariable(
        rates=[[1, 2, 5], [10, 20, 50]],
        starts=[[0, 5000, 10000], [1000, 6000, 11000]],
        durations=[4000, 3000, 2000]),
        label="pop_e",
        additional_parameters={"seed": seed})
    pop_e.record("spikes")

    pop_f = p.Population(n_neurons, p.extra_models.SpikeSourcePoissonVariable(
        rates=[[1, 2, 5], [10, 20, 50]],
        starts=[[0, 5000, 10000], [1000, 6000, 11000]],
        durations=[[4000, 3000, 2000], [3000, 2000, 1000]]),
        label="pop_f",
        additional_parameters={"seed": seed})
    pop_f.record("spikes")

    pop_g = p.Population(n_neurons, p.extra_models.SpikeSourcePoissonVariable(
        rates=[[1, 2, 5], [10, 50]],
        starts=[[0, 1000, 2000], [2000, 3000]]),
        label="pop_g",
        additional_parameters={"seed": seed})
    pop_g.record("spikes")

    pop_h = p.Population(n_neurons, p.SpikeSourcePoisson(rate=1),
                         label="pop_h", additional_parameters={"seed": seed})
    pop_h.record("spikes")

    pop_i = p.Population(n_neurons, p.SpikeSourcePoisson(rate=1, start=100),
                         label="pop_i", additional_parameters={"seed": seed})
    pop_i.record("spikes")

    pop_j = p.Population(n_neurons, p.SpikeSourcePoisson(rate=[1, 10]),
                         label="pop_j", additional_parameters={"seed": seed})
    pop_j.record("spikes")

    pop_k = p.Population(
        n_neurons, p.SpikeSourcePoisson(rate=1, start=[0, 5000]),
        label="pop_k",
        additional_parameters={"seed": seed})
    pop_k.record("spikes")

    pop_l = p.Population(
        n_neurons, p.SpikeSourcePoisson(rate=1, start=10, duration=5000),
        label="pop_l",
        additional_parameters={"seed": seed})
    pop_l.record("spikes")

    pop_m = p.Population(n_neurons, p.SpikeSourcePoisson(
        rate=[1, 10], start=[0, 5000], duration=5000),
        label="pop_m",
        additional_parameters={"seed": seed})
    pop_m.record("spikes")

    pop_n = p.Population(n_neurons, p.SpikeSourcePoisson(
        rate=[1, 10], start=[0, 5000], duration=[5000, 8000]),
        label="pop_n",
        additional_parameters={"seed": seed})
    pop_n.record("spikes")

    pop_o = p.Population(
        n_neurons, p.SpikeSourcePoisson(rate=1, duration=5000), label="pop_o")
    pop_o.record("spikes")

    p.run(run_time)

    pops = [pop_a, pop_b, pop_c, pop_d, pop_e, pop_f, pop_g, pop_h,
            pop_i, pop_j, pop_k, pop_l, pop_m, pop_n, pop_o]
    all_spikes = list()
    for pop in pops:
        all_spikes.append(pop.get_data("spikes").segments[0].spiketrains)
    p.end()

    for pop, spikes in zip(pops, all_spikes):
        print("")
        print("==============================")
        print(pop.label)
        if isinstance(pop.celltype, p.SpikeSourcePoisson):
            names = ["rate", "start", "duration"]
        else:
            names = ["rates", "starts", "durations"]

        for i in range(n_neurons):
            output = ""
            values = []
            for name in names:
                output += "{}: {{}}; ".format(name)
                values.append(pop.get(name)[i])
            print(output.format(*values))
            print(spikes[i])

            # Check the rates
            rates, starts, durations = (
                array(values[0]), array(values[1]), array(values[2]))
            ends = list()
            for j, (start, duration) in enumerate(zip(starts, durations)):
                if duration is None and (j + 1) >= len(starts):
                    ends.append(run_time)
                elif duration is None:
                    ends.append(starts[j + 1])
                else:
                    ends.append(start + duration)
            for rate, start, end in zip(rates, starts, ends):
                rate_spikes = spikes[i][(spikes[i] >= start) &
                                        (spikes[i] < end)]
                expected = (rate / 1000.0) * (end - start)
                tolerance = scipy.stats.poisson.ppf(0.99, expected) - expected
                n_spikes = len(rate_spikes)
                print("Received {} spikes, expected {} spikes"
                      " (with tolerance {}) for rate {}"
                      " for duration {}".format(
                          n_spikes, expected, tolerance, rate, (end - start)))
                assert(n_spikes >= (expected - tolerance))
                assert(n_spikes <= (expected + tolerance))


class TestCreatePoissons(BaseTestCase):

    def test_run(self):
        do_run()


if __name__ == '__main__':
    do_run()
