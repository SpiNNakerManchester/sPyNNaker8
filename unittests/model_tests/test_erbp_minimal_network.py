import spynnaker8 as pyNN
import numpy as np
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import sys
import argparse
import pdb


def main(argv):
    parser = argparse.ArgumentParser(
        description='Foo')

    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('--simtime', help='Simulation time', required=True)
    required_named.add_argument('--nvis', help='Number of visual neurons', required=True)
    required_named.add_argument('--nhid', help='Number of first hidden layer neurons', required=True)
    args = parser.parse_args()

    print (args)

    eta = 0.3
    simtime = float(args.simtime)
    nvis = int(args.nvis)
    nhid = int(args.nhid)
    nc = 2
    label_refr = 1

    print(dir, eta, simtime, nvis, nhid, nc)

    timestep = 1
    pyNN.setup(timestep)  # simulation timestep (ms)
    # Learning rule parameters
    tau_err = 200.0
    w_from_err = 0.01
    w_label_to_err = 0.16
    w_out_to_err = 1.0
    np.random.seed(12345)
    w_plastic_vis_to_hid = np.random.sample(np.random.poisson(nvis * nhid)) * 0.01
    w_plastic_hid_to_out = np.random.sample(np.random.poisson(nvis * nhid))

    neuron_params = {
        "v_thresh": -50.0,  # do not change - hard-coded in C for now
        "v_reset": -70.0,
        "v_rest": -65.0,
        "v": -60.0,
        "i_offset": 0.25}  # DC input - to enable interesting p_j

    highest_input_spike_rate = 300

    input_spike_rates = ((highest_input_spike_rate / nvis) * np.array(range(1, nvis + 1)))
    label_spike_rate = 1000

    # Input neuron population
    pop_vis = pyNN.Population(nvis,
                              pyNN.SpikeSourcePoisson,
                              {'rate': input_spike_rates},
                              label="input_pop")

    # Hidden neuron population
    pop_hidden = pyNN.Population(nhid,
                                 pyNN.extra_models.IFCurrExpERBP(**neuron_params),
                                 label="ERBP Neuron")

    # Out neuron population
    pop_out = pyNN.Population(nc,
                              pyNN.extra_models.IFCurrExpERBP(**neuron_params),
                              label="ERBP Neuron")

    # Label neuron population
    pop_label = pyNN.Population(nc,
                                pyNN.SpikeSourcePoisson,
                                {'rate': [label_spike_rate, 0]},
                                label="input_pop")

    # Error neuron population TODO MAKE IT LINEAR AND NON-LEAKING
    pop_error = pyNN.Population(nc,
                                pyNN.IF_curr_exp(),
                                label="err_pop")

    # TODO MAKE NEGATIVE ERROR POP


    learning_rule_vis_to_hid = pyNN.STDPMechanism(
        timing_dependence=pyNN.TimingDependenceERBP(
            tau_plus=tau_err, A_plus=1, A_minus=1),
        weight_dependence=pyNN.WeightDependenceERBP(
            w_min=0.0, w_max=1),
        weight=w_plastic_vis_to_hid,
        delay=timestep)

    # Define learning rule object
    learning_rule_hid_to_out = pyNN.STDPMechanism(
        timing_dependence=pyNN.TimingDependenceERBP(
            tau_plus=tau_err, A_plus=1, A_minus=1),
        weight_dependence=pyNN.WeightDependenceERBP(
            w_min=0.0, w_max=1),
        weight=w_plastic_hid_to_out,
        delay=timestep)

    # Create projection from input to hidden neuron using learning rule
    vis_hid_synapse_plastic = pyNN.Projection(
        pop_vis,
        pop_hidden,
        pyNN.AllToAllConnector(),
        synapse_type=learning_rule_vis_to_hid,
        receptor_type="excitatory")

    # Create projection from hidden to output neuron using learning rule
    hid_out_synapse = pyNN.Projection(
        pop_hidden,
        pop_out,
        pyNN.AllToAllConnector(),
        synapse_type=learning_rule_hid_to_out,
        receptor_type="excitatory")

    # Create static dendritic projection from error to hidden neuron
    error_hid_synapse = pyNN.Projection(
        pop_error,
        pop_hidden,
        pyNN.AllToAllConnector(),
        pyNN.StaticSynapse(weight=w_from_err, delay=timestep),
        receptor_type="exc_err")

    # Create inhibitory static projection from out to error neuron
    out_error_synapse = pyNN.Projection(
        pop_out,
        pop_error,
        pyNN.OneToOneConnector(),
        # different weight than label_error_synapse because of the non-linear neuron model TODO asap to same weight
        pyNN.StaticSynapse(weight=w_out_to_err, delay=timestep),
        receptor_type="inhibitory")

    # Create static projection from label to error neuron
    label_error_synapse = pyNN.Projection(
        pop_label,
        pop_error,
        pyNN.OneToOneConnector(),
        # different weight than out_error_synapse because of the non-linear neuron model TODO asap to same weight
        pyNN.StaticSynapse(weight=w_label_to_err, delay=timestep),
        receptor_type="excitatory")

    # Setup recording
    pop_vis.record('spikes')
    pop_error.record('all')
    pop_label.record('spikes')
    pop_hidden.record("all")
    pop_out.record("all")

    # Run simulation
    pyNN.run(simtime)

    # Get data
    input_spikes = pop_vis.get_data('spikes')
    err_spikes = pop_error.get_data()
    label_spikes = pop_label.get_data('spikes')
    hidden_neuron_data = pop_hidden.get_data()
    out_neuron_data = pop_out.get_data()
    weight = vis_hid_synapse_plastic.get('weight', 'list', with_address=False)

    print("Original weight: {}".format(w_plastic_vis_to_hid))
    print("Updated SpiNNaker weight: {}".format(weight))

    # Plot
    F = Figure(
        Panel(input_spikes.segments[0].spiketrains,
              yticks=True, markersize=2, xlim=(0, simtime)),
        Panel(hidden_neuron_data.segments[0].filter(name='v')[0],
              ylabel="Hid mem p (mV)",
              data_labels=[pop_hidden.label], yticks=True, xlim=(0, simtime)),
#         Panel(hidden_neuron_data.segments[0].filter(name='gsyn_exc')[0],
#               ylabel="Hid gsyn exc (mV)",
#               data_labels=[pop_hidden.label], yticks=True, xlim=(0, simtime)),
        Panel(hidden_neuron_data.segments[0].spiketrains,
              yticks=True, markersize=2, xlim=(0, simtime)),
        Panel(out_neuron_data.segments[0].filter(name='v')[0],
              ylabel="Out mem p (mV)",
              data_labels=[pop_out.label], yticks=True, xlim=(0, simtime)),
        Panel(out_neuron_data.segments[0].spiketrains,
              yticks=True, markersize=2, xlim=(0, simtime)),
        Panel(err_spikes.segments[0].filter(name='v')[0],
              ylabel="Error mem p (mV)",
              data_labels=[pop_error.label], yticks=True, xlim=(0, simtime)),
        Panel(err_spikes.segments[0].spiketrains,
              yticks=True, markersize=2, xlim=(0, simtime),
              ylabel="Error mem p (mV)"))

    plt.show()
    pyNN.end()
    print("job done")


if __name__ == "__main__":
    main(sys.argv[1:])
