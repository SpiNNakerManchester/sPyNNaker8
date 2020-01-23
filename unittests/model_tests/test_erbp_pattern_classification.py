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

    required_named = parser.add_argument_group('required named arguments')

    required_named.add_argument('--nvis', help='Number of visual neurons', type=int, default=10)
    required_named.add_argument('--nhid', help='Number of first hidden layer neurons', type=int, default=20)
    required_named.add_argument('--learn-epoch', help='Number of learning epoch', type=int, default=10)
    required_named.add_argument('--simtime', help='Simulation time of an epoch', type=float, default=700.)
    required_named.add_argument('--nclass', help='Number of class', type=int, default=3)
    required_named.add_argument('--cooloff', help='Simtime between samples', type=float, default=100.)

    args = parser.parse_args()
    np.random.seed(12345)

    timestep = 1
    pyNN.setup(timestep)  # simulation timestep (ms)

    neuron_params_hid = {
        "v_thresh": 30.0,
        "v_reset": 0.0,
        "v_rest": 0.0,
        "i_offset": 0,
        "v": 0.0,
        "tau_err": 1000
        }
    neuron_params_out = dict(neuron_params_hid, **{"i_offset": 1.})

    highest_input_spike_rate = 100.
    input_rate_patterns = (np.random.sample(args.nclass * args.nvis) * highest_input_spike_rate).reshape(args.nclass, args.nvis)
    label_spike_rate = 60

    # Input neuron population
    pop_vis = pyNN.Population(args.nvis,
                              pyNN.SpikeSourcePoisson(rate=np.zeros(args.nvis).tolist()),
                              label="input_pop")

    # Hidden neuron population
    pop_hidden = pyNN.Population(args.nhid,
                                 pyNN.extra_models.IFCurrExpERBP(**neuron_params_hid),
                                 label="ERBP Neuron")

    # Out neuron population
    pop_out = pyNN.Population(args.nclass,
                              pyNN.extra_models.IFCurrExpERBP(**neuron_params_out),
                              label="ERBP Neuron")

    pop_label = pyNN.Population(args.nclass,
                                pyNN.SpikeSourcePoisson(rate=np.zeros(args.nclass).tolist()),
                                label="label_pop")

    pop_error_pos = pyNN.Population(args.nclass,
                                    pyNN.extra_models.ErrorNeuron(tau_m=1000),
                                    label="err_pop_pos")
    pop_error_neg = pyNN.Population(args.nclass,
                                    pyNN.extra_models.ErrorNeuron(tau_m=1000),
                                    label="err_pop_neg")

    # Learning rule parameters
    w_err_to_hid = np.random.sample(args.nclass * args.nhid) * 10.
    w_err_to_out = 10.

    w_label_to_err = 1.0
    w_out_to_err = w_label_to_err

    w_vis_to_hid = 0.5
    w_hid_to_out = 0.2

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
        synapse_type=get_erbp_learning_rule(w_vis_to_hid),
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
    pop_hidden.record("spikes")
    pop_out.record("spikes")

    def compute_accuracy(out_spikes, sample_orders, start_sample_times):
        n_correct_classifications = 0
        for sample_idx, (start, stop) in enumerate(zip(start_sample_times[:-1], start_sample_times[1:])):
            spike_counter = Counter()
            for neuron_idx, spiketrain in enumerate(out_spikes):
                spike_counter[neuron_idx] = len(spiketrain[ (spiketrain >= start) & (spiketrain < stop) ])
            winner_idx = spike_counter.most_common(n=1)[0][0]
            n_correct_classifications += (winner_idx == sample_orders[sample_idx])
            n_samples = len(start_sample_times)
            acc = n_correct_classifications * 100. / n_samples
        return n_correct_classifications, n_samples, acc


    def train_test_accuracy(out_spikes, sample_orders):
        current_time = int(pyNN.get_current_time())
        time_per_sample = args.simtime + args.cooloff
        assert(current_time == time_per_sample * args.nclass * (args.learn_epoch + 1))
        start_sample_times = np.arange(0, current_time, step=time_per_sample)
        start_sample_times_train,  sample_orders_train = start_sample_times[:-args.nclass], sample_orders[:-args.nclass]
        start_sample_times_test,  sample_orders_test = start_sample_times[args.nclass:], sample_orders[args.nclass:]
        correct_train, count_train, acc_train = compute_accuracy(out_spikes, sample_orders_train, start_sample_times_train)
        correct_test, count_test, acc_test = compute_accuracy(out_spikes, sample_orders_test, start_sample_times_test)
        print('Train accuracy: {}/{} ({}%)\tTest accuracy: {}/{} ({}%)'.format(
            correct_train, count_train, acc_train,
            correct_test, count_test, acc_test
        ))
        return acc_train, acc_test


    def run_sample(input_rates, label_idx=None):
        pop_vis.set(rate=input_rates.tolist())
        if label_idx is not None:
            label_rates = np.zeros(args.nclass)
            label_rates[label_idx] = label_spike_rate
            pop_label.set(rate=label_rates.tolist())
        pyNN.run(args.simtime)
        pop_vis.set(rate=np.zeros(args.nvis).tolist())
        pop_label.set(rate=np.zeros(args.nclass).tolist())
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
    network_spikes = OrderedDict([
        ('vis', pop_vis.get_data()),
        ('hidden', pop_hidden.get_data()),
        ('out', pop_out.get_data()),
        ('label', pop_label.get_data()),
        ('err_neg', pop_error_neg.get_data()),
        ('err_pos', pop_error_pos.get_data())
    ])

    acc_train, acc_test = train_test_accuracy(network_spikes['out'].segments[0].spiketrains,
                                              np.concatenate(all_sample_orders))

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
