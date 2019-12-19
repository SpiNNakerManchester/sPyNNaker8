import matplotlib
matplotlib.use('Agg')

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

    required_named.add_argument('--simtime', help='Simulation time', type=int, default=10000)
    required_named.add_argument('--nvis', help='Number of visual neurons', type=int, default=100)
    required_named.add_argument('--nhid', help='Number of first hidden layer neurons', type=int, default=20)
    required_named.add_argument('--label', help='Index of label (0 or 1)', type=int, default=0)

    args = parser.parse_args()

    print (args)
    np.random.seed(12345)

    simtime = float(args.simtime)
    nvis = int(args.nvis)
    nhid = int(args.nhid)
    nc = 2
    label_refr = 1

    print(dir, simtime, nvis, nhid, nc)

    timestep = 1
    pyNN.setup(timestep)  # simulation timestep (ms)

    neuron_params = {
        "v_thresh": 30.0,
        "v_reset": 0.0,
        "v_rest": 0.0,
        "i_offset": 1,
        "v": 0.0,
        "tau_err": 1000
        }

    highest_input_spike_rate = 100

    input_spike_rates = ((highest_input_spike_rate / nvis) * np.array(range(1, nvis + 1)))
    label_spike_rate = 100

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
    label_rate = [0, 0]
    label_rate[args.label] = label_spike_rate
    pop_label = pyNN.Population(nc,
                                pyNN.SpikeSourcePoisson,
                                {'rate': label_rate},
                                label="input_pop")

    pop_error_pos = pyNN.Population(nc,
                                    pyNN.extra_models.ErrorNeuron(tau_m=1000),
                                    label="err_pos_pop")
    pop_error_neg = pyNN.Population(nc,
                                    pyNN.extra_models.ErrorNeuron(tau_m=1000),
                                    label="err_pos_neg")

    # Learning rule parameters
    tau_err = 200.0
    w_err_to_hid = np.random.sample(nc * nhid) * 10.
    w_err_to_out = 10.

    w_label_to_err = 1.0
    w_out_to_err = w_label_to_err

    def get_erbp_learning_rule(init_weight_factor=0.2, tau_err=20., l_rate=1., reg_rate=0.):
        weight_dist = pyNN.RandomDistribution(
            distribution='normal_clipped', mu=init_weight_factor, sigma=init_weight_factor,
            low=0.0, high=2*init_weight_factor)

        return pyNN.STDPMechanism(
            timing_dependence=pyNN.TimingDependenceERBP(
                tau_plus=tau_err, A_plus=l_rate, A_minus=l_rate),
            weight_dependence=pyNN.WeightDependenceERBP(
                w_min=0.0, w_max=1, reg_rate=reg_rate),
            weight=weight_dist,
            delay=timestep)

    # Create projection from input to hidden neuron using learning rule
    vis_hid_synapse_plastic = pyNN.Projection(
        pop_vis,
        pop_hidden,
        pyNN.AllToAllConnector(),
        synapse_type=get_erbp_learning_rule(0.2),
        receptor_type="excitatory")

    # # Create projection from hidden to output neuron using learning rule
    hid_out_synapse = pyNN.Projection(
        pop_hidden,
        pop_out,
        pyNN.AllToAllConnector(),
        synapse_type=get_erbp_learning_rule(0.2),
        receptor_type="excitatory")

    # Create static dendritic projection from error to hidden neuron
    error_pos_hid_synapse = pyNN.Projection(
        pop_error_pos,
        pop_hidden,
        pyNN.AllToAllConnector(),
        pyNN.StaticSynapse(weight=w_err_to_hid, delay=timestep),
        receptor_type="inh_err")

    error_pos_out_synapse = pyNN.Projection(
        pop_error_pos,
        pop_out,
        pyNN.OneToOneConnector(),
        pyNN.StaticSynapse(weight=w_err_to_out, delay=timestep),
        receptor_type="inh_err")

    error_neg_hid_synapse = pyNN.Projection(
        pop_error_neg,
        pop_hidden,
        pyNN.AllToAllConnector(),
        pyNN.StaticSynapse(weight=w_err_to_hid, delay=timestep),
        receptor_type="exc_err")

    error_neg_out_synapse = pyNN.Projection(
        pop_error_neg,
        pop_out,
        pyNN.OneToOneConnector(),
        pyNN.StaticSynapse(weight=w_err_to_out, delay=timestep),
        receptor_type="exc_err")

    out_error_neg_synapse = pyNN.Projection(
        pop_out,
        pop_error_neg,
        pyNN.OneToOneConnector(),
        pyNN.StaticSynapse(weight=w_out_to_err, delay=timestep),
        receptor_type="inhibitory")


    label_error_neg_synapse = pyNN.Projection(
        pop_label,
        pop_error_neg,
        pyNN.OneToOneConnector(),
        pyNN.StaticSynapse(weight=w_label_to_err, delay=timestep),
        receptor_type="excitatory")

    label_error_synapse = pyNN.Projection(
        pop_label,
        pop_error_neg,
        pyNN.AllToAllConnector(),
        pyNN.StaticSynapse(weight=w_label_to_err, delay=timestep),
        receptor_type="label")

    pop_error_pos_target = True
    if pop_error_pos_target:
        label_error_synapse = pyNN.Projection(
            pop_label,
            pop_error_pos,
            pyNN.AllToAllConnector(),
            pyNN.StaticSynapse(weight=w_label_to_err, delay=timestep),
            receptor_type="label")

        label_error_pos_synapse = pyNN.Projection(
            pop_label,
            pop_error_pos,
            pyNN.OneToOneConnector(),
            pyNN.StaticSynapse(weight=w_label_to_err, delay=timestep),
            receptor_type="inhibitory")

        out_error_pos_synapse = pyNN.Projection(
            pop_out,
            pop_error_pos,
            pyNN.OneToOneConnector(),
            pyNN.StaticSynapse(weight=w_out_to_err, delay=timestep),
            receptor_type="excitatory")


    # Setup recording
    pop_vis.record('spikes')
    pop_error_pos.record('all')
    pop_error_neg.record('all')
    pop_label.record('spikes')
    pop_hidden.record("all")
    pop_out.record("all")

    # Run simulation
    pyNN.run(simtime)

    # Get data
    input_spikes = pop_vis.get_data('spikes')
    err_spikes_pos = pop_error_pos.get_data()
    err_spikes_neg = pop_error_neg.get_data()
    label_spikes = pop_label.get_data('spikes')
    hidden_neuron_data = pop_hidden.get_data()
    out_neuron_data = pop_out.get_data()
    # weight = vis_hid_synapse_plastic.get('weight', 'list', with_address=False)

    # Plot
    F = Figure(
        Panel(input_spikes.segments[0].spiketrains,
              yticks=True, markersize=2, xlim=(0, simtime), data_labels=["input"]),
        Panel(hidden_neuron_data.segments[0].filter(name='v')[0],
              ylabel="Hid mem p (mV)",
              data_labels=[pop_hidden.label], yticks=True, xlim=(0, simtime)),
#         Panel(hidden_neuron_data.segments[0].filter(name='gsyn_exc')[0],
#               ylabel="Hid gsyn exc (mV)",
#               data_labels=[pop_hidden.label], yticks=True, xlim=(0, simtime)),
        Panel(hidden_neuron_data.segments[0].spiketrains,
              yticks=True, markersize=2, xlim=(0, simtime), data_labels=["hidden"]),
        Panel(out_neuron_data.segments[0].filter(name='v')[0],
              ylabel="Out mem p (mV)",
              data_labels=[pop_out.label], yticks=True, xlim=(0, simtime)),
        Panel(out_neuron_data.segments[0].spiketrains,
              yticks=True, markersize=2, xlim=(0, simtime), data_labels=["out"]),
        Panel(err_spikes_pos.segments[0].filter(name='v')[0],
              ylabel="Error mem p (mV)",
              data_labels=[pop_error_pos.label], yticks=True, xlim=(0, simtime)),
        Panel(err_spikes_pos.segments[0].spiketrains,
              yticks=True, markersize=2, xlim=(0, simtime),
              xlabel="Time (ms)", data_labels=["error pos"]),
        Panel(err_spikes_neg.segments[0].filter(name='v')[0],
              ylabel="Error mem p (mV)",
              data_labels=[pop_error_neg.label], yticks=True, xlim=(0, simtime)),
        Panel(err_spikes_neg.segments[0].spiketrains,
              yticks=True, markersize=2, xlim=(0, simtime),
              xlabel="Time (ms)", data_labels=["error neg"]),
        Panel(label_spikes.segments[0].spiketrains,
              yticks=True, markersize=2, xlim=(0, simtime),
              xlabel="Time (ms)", data_labels=["label"]),
        title="Network spikes", marker=u'|',
        annotations="Simulated with {}".format(pyNN.name())
    )

    plt.savefig("minimal_network.png", dpi=300, bbox_inches='tight')

    pyNN.end()
    print("job done")


if __name__ == "__main__":
    main(sys.argv[1:])
