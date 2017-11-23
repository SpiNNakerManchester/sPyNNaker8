import spynnaker8 as p


def test_alpha():
    p.setup(0.1)
    runtime = 50
    populations = []

    pop_src1 = p.Population(1, p.SpikeSourceArray,
                            {'spike_times': [[5, 15, 20, 30]]}, label="src1")

    populations.append(p.Population(1, p.IF_curr_alpha, {}, label="test"))

    populations[0].set(tau_syn_E=2)
    populations[0].set(tau_syn_I=4)

    # define the projections
    p.Projection(
        pop_src1, populations[0], p.OneToOneConnector(),
        p.StaticSynapse(weight=1, delay=1), receptor_type="excitatory")
    p.Projection(
        pop_src1, populations[0], p.OneToOneConnector(),
        p.StaticSynapse(weight=1, delay=100), receptor_type="inhibitory")

    populations[0].record("all")
    p.run(runtime)
    p.end()
