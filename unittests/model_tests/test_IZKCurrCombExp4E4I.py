# import spynnaker7.pyNN as p
import spynnaker8 as p
p.setup(0.1)
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt


runtime=200
pop_src = p.Population(1, p.SpikeSourceArray, {'spike_times': [[0]]}, label="src")


pop_exc = p.Population(1, p.extra_models.IzkCurrCombExp4E4I(), label="test")

d = 12


pop_exc.set(exc_a_tau = 1.7)
pop_exc.set(exc_b_tau = 0.2)

pop_exc.set(exc2_a_tau = 3.7)
pop_exc.set(exc2_b_tau = 0.7)

pop_exc.set(exc3_a_tau = 4.7)
pop_exc.set(exc3_b_tau = 0.7)

pop_exc.set(exc4_a_tau = 1.2)
pop_exc.set(exc4_b_tau = 0.3)


pop_exc.set(inh_a_tau = 5.1)
pop_exc.set(inh_b_tau = 0.1)

pop_exc.set(inh2_a_tau = 3.7)
pop_exc.set(inh2_b_tau = 0.7)

pop_exc.set(inh3_a_tau = 2.4)
pop_exc.set(inh3_b_tau = 1)

pop_exc.set(inh4_a_tau = 6.9)
pop_exc.set(inh4_b_tau = 1.9)

j=0.6
AMPA_PY_W = j * 0.1
_AMPA_INT_W = j * 0.2
_NMDA_W = j * 0.075
_GABA_A_W = j * 0.33
_GABA_B_W = j * 0.0132
_5HT1A_W = j * 0.01375
_5HT2A_W = j * 0.15
# originally the weight was 0.2
_5HT3A_W = j * 0.31



exc_proj = p.Projection(pop_src, pop_exc,
        p.OneToOneConnector(), p.StaticSynapse(weight=AMPA_PY_W, delay=1*d),
        receptor_type="excitatory", label="projTemp")
exc_proj2 = p.Projection(pop_src, pop_exc,
        p.OneToOneConnector(), p.StaticSynapse(weight=_AMPA_INT_W, delay=3*d),
        receptor_type="excitatory2")
exc_proj3 = p.Projection(pop_src, pop_exc,
        p.OneToOneConnector(), p.StaticSynapse(weight=_5HT2A_W, delay=5*d),
        receptor_type="excitatory3")
exc_proj4 = p.Projection(pop_src, pop_exc,
        p.OneToOneConnector(), p.StaticSynapse(weight=_NMDA_W, delay=7*d),
        receptor_type="excitatory4")

inh_proj = p.Projection(pop_src, pop_exc,
        p.OneToOneConnector(), p.StaticSynapse(weight=_GABA_A_W, delay=2*d),
        receptor_type="inhibitory")
inh_proj2 = p.Projection(pop_src, pop_exc,
        p.OneToOneConnector(), p.StaticSynapse(weight=_GABA_B_W, delay=4*d),
        receptor_type="inhibitory2")
inh_proj3 = p.Projection(pop_src, pop_exc,
        p.OneToOneConnector(), p.StaticSynapse(weight=_5HT1A_W, delay=6*d),
        receptor_type="inhibitory3")
inh_proj4 = p.Projection(pop_src, pop_exc,
        p.OneToOneConnector(), p.StaticSynapse(weight=_5HT3A_W, delay=8*d),
        receptor_type="inhibitory4")


pop_src.record('all')

pop_exc.record("all")
p.run(runtime)
weights = []

# pre_spikes = pop_src1.get_data('spikes')
exc_data = pop_exc.get_data()


# Plot
Figure(
    # raster plot of the presynaptic neuron spike times
#     Panel(pre_spikes_slow.segments[0].spiketrains,
#           yticks=True, markersize=0.2, xlim=(0, runtime)),
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
          ylabel="gsyn inhibitory (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].spiketrains,
          yticks=True, markersize=0.2, xlim=(0, runtime)),
    )


plt.show()
p.end()
print "\n job done"