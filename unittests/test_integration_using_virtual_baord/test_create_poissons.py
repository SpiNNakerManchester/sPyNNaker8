import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


def do_run(do_print=False):
    p.setup(1.0)

    pop_a = p.Population(2, p.extra_models.SpikeSourcePoissonVariable(
        rates=[10, 20, 50],
        starts=[0, 500, 1000]),
        label="pop_a")
    pop_a.record("spikes")

    pop_b = p.Population(2, p.extra_models.SpikeSourcePoissonVariable(
        rates=[[1, 2, 5], [10, 20, 50]],
        starts=[0, 500, 1000]),
        label="pop_b")
    pop_b.record("spikes")

    pop_c = p.Population(2, p.extra_models.SpikeSourcePoissonVariable(
        rates=[10, 20, 50],
        starts=[10, 600, 1200],
        durations=[500, 500, 500]),
        label="pop_c")
    pop_c.record("spikes")

    pop_d = p.Population(2, p.extra_models.SpikeSourcePoissonVariable(
        rates=[[1, 2, 5], [10, 20, 50]],
        starts=[0, 500, 1000],
        durations=[500, 400, 300]),
        label="pop_d")
    pop_d.record("spikes")

    pop_e = p.Population(2, p.extra_models.SpikeSourcePoissonVariable(
        rates=[[1, 2, 5], [10, 20, 50]],
        starts=[[0, 500, 1000], [100, 600, 1100]],
        durations=[400, 300, 200]),
        label="pop_e")
    pop_e.record("spikes")

    pop_f = p.Population(2, p.extra_models.SpikeSourcePoissonVariable(
        rates=[[1, 2, 5], [10, 20, 50]],
        starts=[[0, 500, 1000], [100, 600, 1100]],
        durations=[[400, 300, 200], [300, 200, 100]]),
        label="pop_f")
    pop_f.record("spikes")

    pop_g = p.Population(2, p.extra_models.SpikeSourcePoissonVariable(
        rates=[[1, 2, 5], [10, 50]],
        starts=[[0, 100, 200], [200, 300]]),
        label="pop_g")
    pop_g.record("spikes")

    pop_h = p.Population(2, p.SpikeSourcePoisson(rate=1), label="pop_h")
    pop_h.record("spikes")

    pop_i = p.Population(2, p.SpikeSourcePoisson(rate=1, start=100),
                         label="pop_i")
    pop_i.record("spikes")

    pop_j = p.Population(2, p.SpikeSourcePoisson(rate=[1, 10]), label="pop_j")
    pop_j.record("spikes")

    pop_k = p.Population(
        2, p.SpikeSourcePoisson(rate=1, start=[0, 500]), label="pop_k")
    pop_k.record("spikes")

    pop_l = p.Population(
        2, p.SpikeSourcePoisson(rate=1, start=10, duration=500), label="pop_l")
    pop_l.record("spikes")

    pop_m = p.Population(2, p.SpikeSourcePoisson(
        rate=[1, 10], start=[0, 500], duration=500),
        label="pop_m")
    pop_m.record("spikes")

    pop_n = p.Population(2, p.SpikeSourcePoisson(
        rate=[1, 10], start=[0, 500], duration=[500, 800]),
        label="pop_n")
    pop_n.record("spikes")

    pop_o = p.Population(
        2, p.SpikeSourcePoisson(rate=1, duration=500), label="pop_o")
    pop_o.record("spikes")

    p.run(2000)

    if do_print:
        for pop in [pop_a, pop_b, pop_c, pop_d, pop_e, pop_f, pop_g, pop_h,
                    pop_i, pop_j, pop_k, pop_l, pop_m, pop_n, pop_o]:
            spikes = pop.get_data("spikes").segments[0].spiketrains
            print ""
            print "=============================="
            print pop.label
            if isinstance(pop.celltype, p.SpikeSourcePoisson):
                names = ["rate", "start", "duration"]
            else:
                names = ["rates", "starts", "durations"]

            for i in range(2):
                output = ""
                values = []
                for name in names:
                    output += "{}: {{}}; ".format(name)
                    values.append(pop.get(name)[i])
                print output.format(*values)
                print spikes[i]

    p.end()


class TestCreatePoissons(BaseTestCase):

    def test_run(self):
        do_run()


if __name__ == '__main__':
    do_run(do_print=True)
