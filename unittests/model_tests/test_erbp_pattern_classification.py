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

class AssertOnce():
    def __init__(self, assert_fn, text):
        self.assert_fn = assert_fn
        self.text = text
        self.was_called = False
    def __call__(self):
        if not self.was_called:
            if not self.assert_fn():
                raise AssertionError(self.text)
        self.was_called = True

def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--nvis', help='Number of visual neurons', type=int, default=20)
    parser.add_argument('--nhid', help='Number of first hidden layer neurons', type=int, default=200)
    parser.add_argument('--use_hidden', help='Whether to use a hidden layer', action='store_true')
    parser.add_argument('--use_recurrences', help='Whether to use recurrences', action='store_true')
    parser.add_argument('--clean_patterns', help='Whether input patterns are clean or random', action='store_true')
    parser.add_argument('--learn_epoch', help='Number of learning epoch', type=int, default=3)
    parser.add_argument('--simtime', help='Simulation time of an epoch', type=float, default=700.)
    parser.add_argument('--nclass', help='Number of class', type=int, default=3)
    parser.add_argument('--cooloff', help='Simtime between samples', type=float, default=100.)
    # Important network hyperparameters
    parser.add_argument('--l_rate', help='Learning rate e-prop', type=float, default=0.01)
    parser.add_argument('--i_offset', help='DC input to neurons', type=float, default=1.)
    parser.add_argument('--neuron_tau_err', help='Error time constant in the neurons', type=float, default=0.2) # label spikes at high frequency
    parser.add_argument('--synapse_tau_err', help='Error time constant in the synapse', type=float, default=20.)
    parser.add_argument('--error_neuron_tau_m', help='Membrane potential time constant of error neurons', type=float, default=20.)

    args = parser.parse_args()
    np.random.seed(1234)

    timestep = 1
    pyNN.setup(timestep, min_delay=1.0, max_delay=144.0)  # simulation timestep (ms)
    pyNN.set_number_of_neurons_per_core(pyNN.extra_models.IFCurrExpERBP, 4)

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
        for i in range(args.nclass):
            # make sure all class have the same max rate
            input_rate_patterns[i][np.where(input_rate_patterns[i] == input_rate_patterns[i].max())] = highest_input_spike_rate
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
                                    pyNN.extra_models.ErrorNeuron(
                                        tau_m=args.error_neuron_tau_m,
                                        tau_err=args.neuron_tau_err
                                    ),
                                    label="err_pop_pos")
    pop_error_neg = pyNN.Population(args.nclass,
                                    pyNN.extra_models.ErrorNeuron(tau_m=args.error_neuron_tau_m,
                                                                  tau_err=args.neuron_tau_err
                                    ),
                                    label="err_pop_neg")

    # Learning rule parameters
    w_err_feedback = 0.01
    make_feedback_dist = lambda err: pyNN.RandomDistribution(
        distribution='normal_clipped', mu=err, sigma=err,
        low=0.0, high=2*err)

    w_err_hid_exc = make_feedback_dist(w_err_feedback)
    w_err_hid_inh = make_feedback_dist(w_err_feedback)
    w_err_out_exc = make_feedback_dist(w_err_feedback)
    w_err_out_inh = make_feedback_dist(w_err_feedback)

    w_label_to_err = 5.
    w_out_to_err = w_label_to_err

    w_vis_to_hid = 0.2
    w_hid_to_hid = 0.2
    w_hid_to_out = 0.6

    def get_erbp_learning_rule(init_weight_factor=0.2, tau_err=args.synapse_tau_err, l_rate=args.l_rate, reg_rate=0., is_readout=False):
        weight_dist = pyNN.RandomDistribution(
            distribution='normal_clipped', mu=init_weight_factor, sigma=init_weight_factor,
            low=0.0, high=2*init_weight_factor)

        return pyNN.STDPMechanism(
            timing_dependence=pyNN.TimingDependenceERBP(
                tau_plus=tau_err, A_plus=l_rate, A_minus=l_rate,
                is_readout=is_readout),
            weight_dependence=pyNN.WeightDependenceERBP(
                w_min=0.0, w_max=1., reg_rate=reg_rate),
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
            synapse_type=get_erbp_learning_rule(w_vis_to_hid),
            receptor_type="excitatory")

        # Create projection from input to hidden neuron using learning rule
        vis_hid_inh_synapse_plastic = pyNN.Projection(
            pop_vis,
            pop_hidden,
            pyNN.AllToAllConnector(),
            synapse_type=get_erbp_learning_rule(0.5 * w_vis_to_hid),
            receptor_type="inhibitory")

        hid_out_synapse = pyNN.Projection(
            pop_hidden,
            pop_out,
            pyNN.AllToAllConnector(),
            synapse_type=get_erbp_learning_rule(w_hid_to_out,
                                                l_rate=5 * args.l_rate),
            receptor_type="excitatory")

        hid_out_inh_synapse = pyNN.Projection(
            pop_hidden,
            pop_out,
            pyNN.AllToAllConnector(),
            synapse_type=get_erbp_learning_rule(0.5 * w_hid_to_out,
                                                l_rate=5 * args.l_rate),
            receptor_type="inhibitory")

        if args.use_recurrences:
            hid_rec_synapse = pyNN.Projection(
                pop_hidden,
                pop_hidden,
                pyNN.AllToAllConnector(),
                synapse_type=get_erbp_learning_rule(w_hid_to_hid),
                receptor_type="excitatory")

            hid_rec_inh_synapse = pyNN.Projection(
                pop_hidden,
                pop_hidden,
                pyNN.AllToAllConnector(),
                synapse_type=get_erbp_learning_rule(w_hid_to_hid),
                receptor_type="inhibitory")

        # Create static dendritic projection from error to hidden neuron
        error_pos_hid_synapse = pyNN.Projection(
            pop_error_pos,
            pop_hidden,
            pyNN.AllToAllConnector(),
            pyNN.StaticSynapse(weight=w_err_hid_inh, delay=timestep),
            receptor_type="inh_err")

        error_neg_hid_synapse = pyNN.Projection(
            pop_error_neg,
            pop_hidden,
            pyNN.AllToAllConnector(),
            pyNN.StaticSynapse(weight=w_err_hid_exc, delay=timestep),
            receptor_type="exc_err")
    else:
        # Create projection from input to hidden neuron using learning rule
        vis_hid_synapse_plastic = pyNN.Projection(
            pop_vis,
            pop_out,
            pyNN.AllToAllConnector(),
            synapse_type=get_erbp_learning_rule(w_vis_to_hid,
                                                l_rate=5 * args.l_rate),
            receptor_type="excitatory")

        vis_hid_inh_synapse_plastic = pyNN.Projection(
            pop_vis,
            pop_out,
            pyNN.AllToAllConnector(),
            synapse_type=get_erbp_learning_rule(0.5 * w_vis_to_hid,
                                                l_rate=5 * args.l_rate),
            receptor_type="inhibitory")

    error_pos_out_synapse = pyNN.Projection(
        pop_error_pos,
        pop_out,
        pyNN.OneToOneConnector(),
        pyNN.StaticSynapse(weight=w_err_out_inh, delay=timestep),
        receptor_type="inh_err")

    error_neg_out_synapse = pyNN.Projection(
        pop_error_neg,
        pop_out,
        pyNN.OneToOneConnector(),
        pyNN.StaticSynapse(weight=w_err_out_exc, delay=timestep),
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

    def retrieve_weights():
        return vis_hid_synapse_plastic.getWeights()

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
    old_weights = retrieve_weights()
    check_weight_change = AssertOnce(lambda : not np.allclose(old_weights, retrieve_weights()), text='Early abort: weights did not change on first sample presentation')
    for epoch in range(1, args.learn_epoch+1):
        print("learning epoch {}/{}".format(epoch, args.learn_epoch))
        sample_order = np.random.permutation(args.nclass)
        all_sample_orders.append(sample_order)
        for i, sample_idx in enumerate(sample_order):
            print("\tsample {}/{}".format(i+1, args.nclass))
            run_sample(input_rate_patterns[sample_idx], sample_idx)
            check_weight_change()

    # test: simulate without label
    sample_order = np.random.permutation(args.nclass)
    all_sample_orders.append(sample_order)
    for sample_idx in sample_order:
        run_sample(input_rate_patterns[sample_idx])

    # Get data
    if args.use_hidden:
        network_spikes = OrderedDict([
            ('vis', pop_vis.get_data()),
            ('hidden', pop_hidden.get_data()),
            ('out', pop_out.get_data()),
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

    # Plot the test
    duration = (args.simtime + args.cooloff) * args.nclass * 2
    import quantities as pq
    t_stop = network_spikes.values()[0].segments[0].t_stop
     # plot the last seconds of recordings
    xlim = ((t_stop - duration * pq.ms).item(),
            t_stop.item())

    panels = [
        Panel(spikes.segments[0].spiketrains,
              yticks=True, markersize=1, data_labels=[name],
              xlim=xlim)
        for name, spikes in network_spikes.items()
    ]
    Figure(*panels, marker=u'|', sharex=True)
    plt.savefig("classification_results_test.png", dpi=300, bbox_inches='tight')

    pyNN.end()
    print("job done")


if __name__ == "__main__":
    main(sys.argv[1:])
