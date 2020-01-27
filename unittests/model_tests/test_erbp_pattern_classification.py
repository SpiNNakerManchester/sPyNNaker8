import matplotlib
matplotlib.use('Agg')

import spynnaker8 as pyNN
import numpy as np
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import sys
import argparse
import pdb
from collections import OrderedDict, Counter

def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--nvis', help='Number of visual neurons', type=int, default=50)
    parser.add_argument('--nhid', help='Number of first hidden layer neurons', type=int, default=10)
    parser.add_argument('--use_hidden', help='Whether to use a hidden layer', action='store_true')
    parser.add_argument('--clean_patterns', help='Whether input patterns are clean or random', action='store_true')
    parser.add_argument('--learn_epoch', help='Number of learning epoch', type=int, default=3)
    parser.add_argument('--simtime', help='Simulation time of an epoch', type=float, default=700.)
    parser.add_argument('--nclass', help='Number of class', type=int, default=3)
    parser.add_argument('--cooloff', help='Simtime between samples', type=float, default=100.)
    # Important network hyperparameters
    parser.add_argument('--w_error_gain', help='Gain for feedback alignment (error synapses)', type=float, default=10.)
    parser.add_argument('--l_rate', help='Learning rate e-prop', type=float, default=1.)
    parser.add_argument('--i_offset', help='DC input to neurons', type=float, default=1.)
    parser.add_argument('--neuron_tau_err', help='Error time constant in the neurons', type=float, default=100.)
    parser.add_argument('--synapse_tau_err', help='Error time constant in the synapse', type=float, default=20.)
    parser.add_argument('--error_neuron_tau_m', help='Membrane potential time constant of error neurons', type=float, default=100.)

    args = parser.parse_args()
    np.random.seed(123456)

    timestep = 1
    pyNN.setup(timestep)  # simulation timestep (ms)

    neuron_params_hid = {
        "v_thresh": 30.0,
        "v_reset": 0.0,
        "v_rest": 0.0,
        "i_offset": args.i_offset,
        "v": 0.0,
        "tau_err": args.neuron_tau_err
        }
    neuron_params_out = dict(neuron_params_hid)

    highest_input_spike_rate = 50.
    def random_rates(threshold_low_rates=False):
        input_rate_patterns = (np.random.sample(args.nclass * args.nvis) * highest_input_spike_rate).reshape(args.nclass, args.nvis)
        if threshold_low_rates:
            input_rate_patterns[input_rate_patterns < 10] = 0.
        return np.around(input_rate_patterns - 0.5, decimals=0)

    def clean_classes():
        input_rate_patterns = np.zeros((args.nclass, args.nvis))
        n_active_input = args.nvis // args.nclass
        for i in range(args.nclass):
            input_rate_patterns[i][i * n_active_input : (i + 1) * n_active_input] = highest_input_spike_rate
        return input_rate_patterns

    if args.clean_patterns:
        input_rate_patterns = clean_classes()
    else:
        input_rate_patterns = random_rates()

        import ipdb; ipdb.set_trace()
    label_spike_rate = 60

    # Input neuron population
    pop_vis = pyNN.Population(args.nvis,
                              pyNN.SpikeSourcePoisson(rate=np.zeros(args.nvis)),
                              label="input_pop")

    # Out neuron population
    pop_out = pyNN.Population(args.nclass,
                              pyNN.extra_models.IFCurrExpERBP(**neuron_params_out),
                              label="ERBP Neuron")

    pop_label = pyNN.Population(args.nclass,
                                pyNN.SpikeSourcePoisson(rate=np.zeros(args.nclass)),
                                label="label_pop")

    pop_error_pos = pyNN.Population(args.nclass,
                                    pyNN.extra_models.ErrorNeuron(tau_m=args.error_neuron_tau_m),
                                    label="err_pop_pos")
    pop_error_neg = pyNN.Population(args.nclass,
                                    pyNN.extra_models.ErrorNeuron(tau_m=args.error_neuron_tau_m),
                                    label="err_pop_neg")

    # Learning rule parameters
    w_err_to_hid = np.random.sample(args.nclass * args.nhid) * args.w_error_gain
    w_err_to_out = 1. * args.w_error_gain

    w_label_to_err = 5.
    w_out_to_err = w_label_to_err

    w_vis_to_hid = 0.01
    w_hid_to_out = 0.2

    def get_erbp_learning_rule(init_weight_factor=0.2, tau_err=args.synapse_tau_err, l_rate=args.l_rate, reg_rate=0.):
        weight_dist = pyNN.RandomDistribution(
            distribution='normal_clipped', mu=init_weight_factor, sigma=0.5,
            low=0.0, high=2*init_weight_factor)

        return pyNN.STDPMechanism(
            timing_dependence=pyNN.TimingDependenceERBP(
                tau_plus=tau_err, A_plus=l_rate, A_minus=l_rate),
            weight_dependence=pyNN.WeightDependenceERBP(
                w_min=0.0, w_max=1, reg_rate=reg_rate),
            weight=weight_dist,
            delay=timestep)

    if args.use_hidden:
        # Hidden neuron population
        pop_hidden = pyNN.Population(args.nhid,
                                     pyNN.extra_models.IFCurrExpERBP(**neuron_params_hid),
                                     label="ERBP Neuron")

        # Create projection from input to hidden neuron using learning rule
        vis_hid_synapse_plastic = pyNN.Projection(
            pop_vis,
            pop_hidden,
            pyNN.AllToAllConnector(),
            synapse_type=get_erbp_learning_rule(w_vis_to_hid, reg_rate=0.),
            receptor_type="excitatory")

        # # Create projection from hidden to output neuron using learning rule
        hid_out_synapse = pyNN.Projection(
            pop_hidden,
            pop_out,
            pyNN.AllToAllConnector(),
            synapse_type=get_erbp_learning_rule(w_hid_to_out),
            receptor_type="excitatory")

        # Create static dendritic projection from error to hidden neuron
        error_pos_hid_synapse = pyNN.Projection(
            pop_error_pos,
            pop_hidden,
            pyNN.AllToAllConnector(),
            pyNN.StaticSynapse(weight=w_err_to_hid, delay=timestep),
            receptor_type="inh_err")

        error_neg_hid_synapse = pyNN.Projection(
            pop_error_neg,
            pop_hidden,
            pyNN.AllToAllConnector(),
            pyNN.StaticSynapse(weight=w_err_to_hid, delay=timestep),
            receptor_type="exc_err")
    else:
        # Create projection from input to hidden neuron using learning rule
        vis_hid_synapse_plastic = pyNN.Projection(
            pop_vis,
            pop_out,
            pyNN.AllToAllConnector(),
            synapse_type=get_erbp_learning_rule(w_hid_to_out),
            receptor_type="excitatory")

    error_pos_out_synapse = pyNN.Projection(
        pop_error_pos,
        pop_out,
        pyNN.OneToOneConnector(),
        pyNN.StaticSynapse(weight=w_err_to_out, delay=timestep),
        receptor_type="inh_err")

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
    pop_error_pos.record('spikes')
    pop_error_neg.record('spikes')
    pop_label.record('spikes')
    pop_out.record("spikes")
    if args.use_hidden:
        pop_hidden.record("spikes")

    def compute_epoch_accuracy(out_spikes, sample_orders, sample_times):
        n_correct_classifications = 0
        for sample_idx, (start, stop) in enumerate(zip(sample_times[:-1], sample_times[1:])):
            spike_counter = Counter()
            for neuron_idx, spiketrain in enumerate(out_spikes):
                spike_counter[neuron_idx] = len(spiketrain[ (spiketrain >= start) & (spiketrain < stop) ])
            winner_idx = spike_counter.most_common(n=1)[0][0]
            n_correct_classifications += (winner_idx == sample_orders[sample_idx])
        n_samples = len(sample_times) - 1
        acc = n_correct_classifications * 100. / n_samples
        return acc

    def compute_accuracy(out_spikes, all_sample_orders):
        current_time = int(pyNN.get_current_time())
        time_per_sample = args.simtime + args.cooloff
        assert(current_time == time_per_sample * args.nclass * (args.learn_epoch + 1)) # check we simulated the right duration
        epoch_start_times = np.arange(0, current_time, step=time_per_sample * args.nclass)
        assert(len(epoch_start_times) == (args.learn_epoch + 1) == len(all_sample_orders)) # check we did the right number of epochs
        relative_sample_times = np.arange(0, time_per_sample * args.nclass + time_per_sample, step=time_per_sample)

        all_accuracies = []
        for i_epoch, epoch_sample_order in enumerate(all_sample_orders):
            sample_times = epoch_start_times[i_epoch] + relative_sample_times
            all_accuracies.append(compute_epoch_accuracy(out_spikes, epoch_sample_order, sample_times))

        return all_accuracies

    def run_sample(input_rates, label_idx=None):
        pop_vis.set(rate=input_rates)
        if label_idx is not None:
            label_rates = np.zeros(args.nclass)
            label_rates[label_idx] = label_spike_rate
            pop_label.set(rate=label_rates)
        pyNN.run(args.simtime)
        pop_vis.set(rate=np.zeros(args.nvis))
        pop_label.set(rate=np.zeros(args.nclass))
        pyNN.run(args.cooloff)

    all_sample_orders = []
    # train
    for epoch in range(1, args.learn_epoch+1):
        print("learning epoch {}/{}".format(epoch, args.learn_epoch))
        sample_order = np.random.permutation(args.nclass)
        all_sample_orders.append(sample_order)
        for i, sample_idx in enumerate(sample_order):
            print("\tsample {}/{}".format(i+1, args.nclass))
            run_sample(input_rate_patterns[sample_idx], sample_idx)

    # test: simulate without label
    sample_order = np.random.permutation(args.nclass)
    all_sample_orders.append(sample_order)
    for sample_idx in sample_order:
        run_sample(input_rate_patterns[sample_idx])

    # Get data
    if args.use_hidden:
        network_spikes = OrderedDict([
            ('vis', pop_vis.get_data()),
            ('out', pop_out.get_data()),
            ('hidden', pop_hidden.get_data()),
            ('label', pop_label.get_data()),
            ('err_neg', pop_error_neg.get_data()),
            ('err_pos', pop_error_pos.get_data())
        ])
    else:
        network_spikes = OrderedDict([
            ('vis', pop_vis.get_data()),
            ('out', pop_out.get_data()),
            ('label', pop_label.get_data()),
            ('err_neg', pop_error_neg.get_data()),
            ('err_pos', pop_error_pos.get_data())
        ])

    all_accuracies = compute_accuracy(network_spikes['out'].segments[0].spiketrains,
                                      all_sample_orders)
    print('Train accuracy: {}\tTest accuracy: {:.2f}'.format(all_accuracies[:-1], all_accuracies[-1]))


    panels = [
        Panel(spikes.segments[0].spiketrains,
              yticks=True, markersize=1, data_labels=[name])
        for name, spikes in network_spikes.items()
    ]

    # Plot
    Figure(*panels, marker=u'|', sharex=True)
    plt.savefig("classification_results.png", dpi=300, bbox_inches='tight')

    pyNN.end()
    print("job done")


if __name__ == "__main__":
    main(sys.argv[1:])
