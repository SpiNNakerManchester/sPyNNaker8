# Standard library imports
import argparse
import cPickle as pickle

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
# Local application imports
import utilities as util
# Third party imports
from pyNN.utility.plotting import Figure, Panel

DIR = ''
RUNTIME = ''
N_ROW = 0
N_COL = 0

cmap = mcolors.LinearSegmentedColormap.from_list("",
                                                 [(0, "black"),
                                                  (0.5, "yellow"),
                                                  (1, "red")], N=256)

cmap_rainbow = mcolors.LinearSegmentedColormap.from_list("",
                                                         [(0, "#001aff"),  # blue
                                                          (0.2, "#00ffea"),  # cyan
                                                          (0.4, "#00ff2f"),  # green
                                                          (0.6, "#fff700"),  # yellow
                                                          (0.8, "#ff8000"),  # orange
                                                          (1, "#ff0000")], N=256)  # red

DEFAULT_FIG_SETTINGS = {
    'lines.linewidth': 0.5,
    'axes.linewidth': 0.5,
    'axes.labelsize': 'small',
    'legend.fontsize': 'small',
    'font.size': 9,
    'savefig.dpi': 600,
}


def main(vel_input_cells, trajectory, exc_dir_view, times):
    if vel_input_cells:
        with open(DIR + "pop_vel_input_spike_trains.pkl", 'rb') as f:
            pop_input_spike_trains = pickle.load(f)
        # with open(DIR + "pop_input_v.pkl", 'rb') as f:
        #     pop_input_v = pickle.load(f)
        with open(DIR + "pop_vel_input_label.pkl", 'rb') as f:
            pop_input_label = pickle.load(f)
        input_cell_plots(pop_input_label, pop_input_spike_trains)

    if exc_dir_view:
        with open(DIR + "pop_exc_north_spike_train.pkl", 'rb') as f:
            pop_exc_north_spike_train = pickle.load(f)
        with open(DIR + "pop_exc_east_spike_train.pkl", 'rb') as f:
            pop_exc_east_spike_train = pickle.load(f)
        with open(DIR + "pop_exc_west_spike_train.pkl", 'rb') as f:
            pop_exc_west_spike_train = pickle.load(f)
        with open(DIR + "pop_exc_south_spike_train.pkl", 'rb') as f:
            pop_exc_south_spike_train = pickle.load(f)
        grid_cell_dir_plots(pop_exc_north_spike_train, pop_exc_east_spike_train,
                            pop_exc_west_spike_train, pop_exc_south_spike_train)

    # with open(DIR + "pop_exc_v.pkl", 'rb') as f:
    #     pop_exc_v = pickle.load(f)
    # with open(DIR + "pop_exc_gsyn_exc.pkl", 'rb') as f:
    #     pop_exc_gsyn_exc = pickle.load(f)
    # with open(DIR + "pop_exc_gsyn_inh.pkl", 'rb') as f:
    #     pop_exc_gsyn_inh = pickle.load(f)
    with open(DIR + "pop_exc_gc_spiketrains.pkl", 'rb') as f:
        pop_exc_spiketrains = pickle.load(f)
    with open(DIR + "pop_exc_gc_label.pkl", 'rb') as f:
        pop_exc_label = pickle.load(f)
    with open(DIR + "pop_exc_gc_positions.pkl", 'rb') as f:
        pop_exc_pos = pickle.load(f)
    with open(DIR + "pop_exc_gc_parameters.pkl", 'rb') as f:
        pop_exc_parameters = pickle.load(f)

    grid_cell_plots(times, pop_exc_label, pop_exc_spiketrains,
                    pop_exc_pos)

    # if trajectory:
    #     # Single grid cell response

    time_window = 1000  # time window for firing rate plots
    plot_population_firing_rate(times, pop_exc_label, pop_exc_spiketrains, pop_exc_pos, time_window)
    # get_active_neuron_counts(pop_exc_spiketrains, pop_exc_pos, times[-1])


def input_cell_plots(pop_input_label, pop_input_spike_trains):
    Figure(
        # Panel(pop_input_v,
        #       ylabel="Membrane potential (mV)",
        #       xlabel="Time (ms)",
        #       data_labels=[pop_input_label],
        #       yticks=True, xticks=True, xlim=(0, RUNTIME)
        #       ),
        Panel(pop_input_spike_trains,
              xlabel="Time (ms)",
              ylabel="Neuron index",
              yticks=True, xticks=True, marker='o', markersize=0.2, xlim=(0, RUNTIME)
              ),
        settings=DEFAULT_FIG_SETTINGS,
        title="Input cells",
        annotations="0=N, 1=E, 2=W, 3=S"
    )
    plt.savefig(DIR + "input_cells.eps", format='eps')
    plt.clf()


# def plot_trajectory_2d(trajectory, x_lim, y_lim, folderpath, spiketrains):
#     plt.xlabel('x (cm)')
#     plt.xlim(0, x_lim)
#     plt.ylim(0, y_lim)
#     plt.ylabel('y (cm)')
#
#     plt.scatter(trajectory[0, 0], trajectory[0, 1], s=50, marker='o', c="r")
#     plt.plot(trajectory[:, 0], trajectory[:, 1], linestyle='-', color='k', linewidth=1)
#
#     plt.tick_params(axis='both', labelsize=9)
#     plt.savefig(folderpath + 'trajectory.png', bbox_inches='tight')


def grid_cell_dir_plots(pop_exc_north_spike_train, pop_exc_east_spike_train,
                        pop_exc_west_spike_train, pop_exc_south_spike_train):
    Figure(
        Panel(pop_exc_north_spike_train,
              yticks=True, xticks=False, xlabel="Time (ms) (N)", marker='o', markersize=0.2, xlim=(0, RUNTIME)
              ),
        Panel(pop_exc_east_spike_train,
              yticks=True, xticks=False, xlabel="Time (ms) (E)", marker='o', markersize=0.2, xlim=(0, RUNTIME)
              ),
        Panel(pop_exc_west_spike_train,
              yticks=True, xticks=False, xlabel="Time (ms) (W)", marker='o', markersize=0.2, xlim=(0, RUNTIME)
              ),
        Panel(pop_exc_south_spike_train,
              yticks=True, xticks=True, xlabel="Time (ms) (S)", marker='o', markersize=0.2, xlim=(0, RUNTIME)
              ),
        settings=DEFAULT_FIG_SETTINGS,
        title="Excitatory grid cells for each direction",
        annotations=""
    )
    plt.savefig(DIR + "exc_grid_cells_dir.eps", format='eps')
    plt.clf()


def grid_cell_plots(times, pop_exc_label, pop_exc_spiketrains,
                    pop_exc_pos):
    Figure(
        # Panel(pop_exc_v,
        #       ylabel="Membrane potential (mV)",
        #       xlabel="Time (ms)",
        #       data_labels=[pop_exc_label], yticks=True, xticks=True, xlim=(0, RUNTIME)
        #       ),
        # Panel(pop_exc_gsyn_exc,
        #       ylabel="Excitatory synaptic conduction (uS)",
        #       xlabel="Time (ms)",
        #       data_labels=[pop_exc_label], yticks=True, xticks=True, xlim=(0, RUNTIME)
        #       ),
        # Panel(pop_exc_gsyn_inh,
        #       ylabel="Inhibitory synaptic conduction (uS)",
        #       xlabel="Time (ms)",
        #       data_labels=[pop_exc_label], yticks=True, xticks=True, xlim=(0, RUNTIME)
        #       ),
        Panel(pop_exc_spiketrains,
              yticks=True, xticks=True, xlabel="Time (ms)", marker='o', markersize=0.2, xlim=(0, RUNTIME)
              ),
        settings=DEFAULT_FIG_SETTINGS,
        title=pop_exc_label,
        annotations=""
    )
    plt.savefig(DIR + "exc_grid_cells_pop.eps", format='eps', bbox_inches='tight')
    plt.clf()


def plot_population_firing_rate(times, label, spiketrains, pos, time_window):
    # plt.style.use('dark_background')
    num_times = len(times)
    # fig, axs = plt.subplots(ncols=num_times, figsize=(6, 3))
    # fig, axs = plt.subplots(ncols=num_times)
    fig, axs = plt.subplots(int(len(times) / 5), 5,
                            sharex='col', sharey='row', gridspec_kw={'wspace': 0.2, 'hspace': 0},
                            figsize=(6, 3))
    # fig.suptitle(label + ' firing rates')
    subplot_counter = 0

    for ax_row in axs:
        for ax in ax_row:
            t = times[subplot_counter]
            subplot_counter += 1
            ax.set_xlim(0, N_COL - 1)
            ax.set_ylim(0, N_ROW - 1)
            ax.set_title(str(t) + 'ms')
            ax.set_facecolor('k')
            ax.get_xaxis().set_ticks([0, N_COL])
            ax.get_yaxis().set_ticks([0, N_ROW])

            ax.set_aspect('equal')
            firing_rates = util.compute_firing_rates_from_spike_trains(spiketrains, t, time_window)
            firing_rate_max = max(firing_rates)

            if firing_rate_max != 0:
                for x, val in enumerate(firing_rates):
                    norm_firing_rate = util.normalise_round(val, 0, firing_rate_max)
                    ax.scatter(pos[x][0], pos[x][1], s=10,
                               c=norm_firing_rate, cmap=cmap, norm=plt.Normalize(0, 1))
            print("Plotting subplot " + str(t))
    # plt.annotate("Firing rate computed over time window of " + str(time_window) + "ms up until timestamp")
    # fig.colorbar(cmap)
    # plt.subplots_adjust(wspace=0.5, hspace=0.5)
    # fig.tight_layout()
    plt.savefig(DIR + 'pop_exc_gc_firing_rate.eps', format='eps',
                facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=600)
    plt.clf()


def get_active_neuron_counts(spike_trains, neuron_positions, time):
    count_n = 0
    count_e = 0
    count_w = 0
    count_s = 0

    for neuron_id, spike_train in enumerate(spike_trains):
        if time in spike_train:
            dir = util.get_dir_pref((neuron_positions[neuron_id])[:2])
            if dir == [0, 1]:
                count_n += 1
            elif dir == [0, -1]:
                count_s += 1
            elif dir == [1, 0]:
                count_w += 1
            elif dir == [-1, 0]:
                count_e += 1

    f = open(DIR + "active_neurons.txt", "w")
    f.write("Active neurons at " + str(time) + "ms")
    f.write("\nN: " + str(count_n))
    f.write("\nE: " + str(count_e))
    f.write("\nW: " + str(count_w))
    f.write("\nS: " + str(count_s))
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", "-d", help="set output directory")
    parser.add_argument("--runtime", "-r", help="set runtime")
    parser.add_argument("--row", "-row", help="set pop_exc grid row")
    parser.add_argument("--col", "-col", help="set pop_exc grid col")
    parser.add_argument("--inputs", "-i", help="set flag for input plots")
    parser.add_argument("--trajectory", "-traj", help="set flag for trajectory plots")
    parser.add_argument("--dir_views", "-dv", help="set flag for gc dir view plots")
    parser.add_argument("--times", "-t", help="set timestamps for plots")

    args = parser.parse_args()
    DIR = args.dir
    RUNTIME = int(args.runtime)
    N_ROW = int(args.row)
    N_COL = int(args.col)
    times = map(int, args.times.strip('[]').split(','))
    if args.inputs == 'True':
        inputs = True
    else:
        inputs = False

    if args.trajectory == 'True':
        trajectory = True
    else:
        trajectory = False

    if args.dir_views == 'True':
        dir_views = True
    else:
        dir_views = False

    main(inputs, trajectory, dir_views, times)
