import spynnaker8 as p
import numpy
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

timestep = 1
p.setup(timestep)  # simulation timestep (ms)
runtime = 200

# Learning rule parameters
tau_err = 200.0
gamma = 0.3
w_err_exc = 1
w_err_inh = 0.75
w_plastic = 2
dt_exc = [16,
        43, 44, 45, 46
          ]  # time difference of 15, +1 for a single timestep delay
dt_inh = [18,
        42,
        67
          ]  # time difference of 8, +1 for a single timestep delay

# Hidden neuron population - i.e. postsynaptic population
neuron_params = {
    "v_thresh": -50.0,  # do not change - hard-coded in C for now
    "v_reset": -70.0,
    "v_rest": -65.0,
    "v": -60.0,
    "i_offset": 0.25}  # DC input - to enable interesting p_j

pop_hidden = p.Population(1,  # number of neurons
                          p.extra_models.IFCurrExpERBP(**neuron_params),
                          label="ERBP Neuron")

# Input spike source (sends presynaptic spike)
input_spike_times = [[50, 150]]
input_src = p.Population(1,  # number of sources
                         p.SpikeSourceArray,
                         {'spike_times': input_spike_times},
                         label="input_pop")

# Error spike source (sends error spike)
exc_err_spike_times = [input_spike_times[0][0] + dt - timestep for dt in dt_exc]

exc_err_src = p.Population(1,
                       p.SpikeSourceArray,
                       {'spike_times': [exc_err_spike_times]},
                       label="exc_err_pop")

inh_err_spike_times = [input_spike_times[0][0] + dt - timestep for dt in dt_inh]

inh_err_src = p.Population(1,
                       p.SpikeSourceArray,
                       {'spike_times': [inh_err_spike_times]},
                       label="inh_err_pop")

# Define learning rule object
learning_rule = p.STDPMechanism(
    timing_dependence=p.TimingDependenceERBP(
        tau_plus=tau_err, A_plus=1, A_minus=1),
    weight_dependence=p.WeightDependenceERBP(
        w_min=0.0, w_max=2 * w_plastic),
    weight=w_plastic,
    delay=timestep)

# Create projection from input to hidden neuron using learning rule
synapse_plastic = p.Projection(
    input_src,
    pop_hidden,
    p.OneToOneConnector(),
    synapse_type=learning_rule,
    receptor_type="excitatory")

# Create static projection from error to hidden neuron
exc_err_synapse = p.Projection(
    exc_err_src,
    pop_hidden,
    p.AllToAllConnector(),
    p.StaticSynapse(weight=w_err_exc, delay=timestep),
    receptor_type="exc_err")

inh_err_synapse = p.Projection(
    inh_err_src,
    pop_hidden,
    p.AllToAllConnector(),
    p.StaticSynapse(weight=w_err_inh, delay=timestep),
    receptor_type="inh_err")

# Setup recording
input_src.record('spikes')
exc_err_src.record('spikes')
inh_err_src.record('spikes')
pop_hidden.record("all")


# Run simulation
p.run(runtime)


# Get data
input_spikes = input_src.get_data('spikes')
exc_err_spikes = exc_err_src.get_data('spikes')
inh_err_spikes = inh_err_src.get_data('spikes')
hidden_neuron_data = pop_hidden.get_data()
weight = synapse_plastic.get('weight', 'list', with_address=False)[0]


# Hand calculate weight update to check SpiNNajer operation
dw_exc = 0
for exc_err_spike in dt_exc:
    p_j = gamma * ((neuron_params["v"] - neuron_params["v_rest"]) /
                   (neuron_params["v_thresh"] - neuron_params["v_rest"]))
    trace_at_err_spike = p_j * numpy.exp(-exc_err_spike / tau_err)
    dw_exc += trace_at_err_spike * w_err_exc
    # print dw_exc

# Hand calculate weight update to check SpiNNajer operation
dw_inh = 0
for inh_err_spike in dt_inh:
    p_j = gamma * ((neuron_params["v"] - neuron_params["v_rest"]) /
                   (neuron_params["v_thresh"] - neuron_params["v_rest"]))
    trace_at_err_spike = p_j * numpy.exp(-inh_err_spike / tau_err)
    dw_inh += trace_at_err_spike * w_err_inh
    # print dw_inh




hand_calc_weight = w_plastic + dw_exc - dw_inh

print "Original weight: {}".format(w_plastic)
print "Updated SpiNNaker weight: {}".format(weight)
print "Handcalculated updated weight: {}".format(hand_calc_weight)


# Plot
F = Figure(
    # plot data for postsynaptic neuron
    Panel(input_spikes.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)),
    Panel(exc_err_spikes.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)),
    Panel(inh_err_spikes.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)),
    Panel(hidden_neuron_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop_hidden.label], yticks=True, xlim=(0, runtime)
          ),
    Panel(hidden_neuron_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[pop_hidden.label], yticks=True, xlim=(0, runtime)))

plt.show()
p.end()
