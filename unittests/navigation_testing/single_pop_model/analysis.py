# Standard library imports
import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import sys

# Third party imports
from pyNN.utility.plotting import Figure, Panel

# Local application imports
import utilities as util

DIR = ''
RUNTIME = ''
N_ROW = 0
N_COL = 0

cmap = mcolors.LinearSegmentedColormap.from_list("",
                                                 [(0, "black"),
                                                  (0.5, "yellow"),
                                                  (1, "red")], N=256)

DEFAULT_FIG_SETTINGS = {
    'lines.linewidth': 0.5,
    'axes.linewidth': 0.5,
    'axes.labelsize': 'small',
    'legend.fontsize': 'small',
    'font.size': 9,
    'savefig.dpi': 200,
}


def main(input_cells, exc_dir_view):

    if input_cells:
        with open(DIR + "pop_input_spike_trains.pkl", 'rb') as f:
            pop_input_spike_trains = pickle.load(f)
        with open(DIR + "pop_input_v.pkl", 'rb') as f:
            pop_input_v = pickle.load(f)
        with open(DIR + "pop_input_label.pkl", 'rb') as f:
            pop_input_label = pickle.load(f)
        input_cell_plots(pop_input_label, pop_input_spike_trains, pop_input_v)

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
    with open(DIR + "pop_exc_spiketrains.pkl", 'rb') as f:
        pop_exc_spiketrains = pickle.load(f)
    with open(DIR + "pop_exc_label.pkl", 'rb') as f:
        pop_exc_label = pickle.load(f)
    with open(DIR + "pop_exc_positions.pkl", 'rb') as f:
        pop_exc_pos = pickle.load(f)
    with open(DIR + "pop_exc_parameters.pkl", 'rb') as f:
        pop_exc_parameters = pickle.load(f)

    times = [50, 150, 200, 1000, 1200, int(RUNTIME)-1]
    grid_cell_plots(times, pop_exc_label, pop_exc_spiketrains,
                    pop_exc_pos)
    plot_population_firing_rate(times, pop_exc_label, pop_exc_spiketrains, pop_exc_pos)


def input_cell_plots(pop_input_label, pop_input_spike_trains, pop_input_v):
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
              yticks=True, xticks=True,  markersize=1, xlim=(0, RUNTIME)
              ),
        settings=DEFAULT_FIG_SETTINGS,
        title="Input cells",
        annotations="0=N, 1=E, 2=W, 3=S"
    ).save(DIR + "input_cells.png")


def grid_cell_dir_plots(pop_exc_north_spike_train, pop_exc_east_spike_train,
                        pop_exc_west_spike_train, pop_exc_south_spike_train):
    Figure(
        Panel(pop_exc_north_spike_train,
              yticks=True, xticks=True, xlabel="Time (ms) (N)", markersize=1, xlim=(0, RUNTIME)
              ),
        Panel(pop_exc_east_spike_train,
              yticks=True, xticks=True, xlabel="Time (ms) (E)", markersize=1, xlim=(0, RUNTIME)
              ),
        Panel(pop_exc_west_spike_train,
              yticks=True, xticks=True, xlabel="Time (ms) (W)", markersize=1, xlim=(0, RUNTIME)
              ),
        Panel(pop_exc_south_spike_train,
              yticks=True, xticks=True, xlabel="Time (ms) (S)", markersize=1, xlim=(0, RUNTIME)
              ),
        settings=DEFAULT_FIG_SETTINGS,
        title="Excitatory grid cells for each direction",
    ).save(DIR + "exc_grid_cells_dir.png")


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
              yticks=True, xticks=True, xlabel="Time (ms)", markersize=1, xlim=(0, RUNTIME)
              ),
        settings=DEFAULT_FIG_SETTINGS,
        title=pop_exc_label,
    ).save(DIR + "exc_grid_cells_pop.png")


# Plot the firing rate of a population at a given time
def plot_population_firing_rate(times, label, spiketrains, pos):
    # plt.style.use('dark_background')
    num_times = len(times)
    fig, axs = plt.subplots(ncols=num_times)
    fig.suptitle(label + 'firing rates')
    num_neurons = N_ROW * N_COL

    for i, ax in enumerate(axs):
        t = times[i]
        ax.set_xlim(0, N_COL - 1)
        ax.set_ylim(0, N_ROW - 1)
        ax.set_title(str(t) + 'ms')
        ax.set_facecolor('k')
        ax.get_xaxis().set_ticks([0, N_COL])
        ax.get_yaxis().set_ticks([0, N_ROW])

        ax.set_aspect('equal')
        firing_rates = util.compute_firing_rates_from_spike_trains(spiketrains, t, num_neurons)
        firing_rate_max = max(firing_rates)

        if firing_rate_max != 0:
            for j, val in enumerate(firing_rates):
                norm_firing_rate = util.normalise(val, 0, firing_rate_max)
                ax.scatter(pos[j][0], pos[j][1], s=10,
                           c=norm_firing_rate, cmap=cmap, norm=plt.Normalize(0, 1))
    # plt.colorbar(cmap)
    fig.tight_layout()
    plt.savefig(DIR + 'pop_exc_gc_firing_rate.png', facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=200)


if __name__ == "__main__":
    DIR = sys.argv[1]
    RUNTIME = int(sys.argv[2])
    N_ROW = int(sys.argv[3])
    N_COL = int(sys.argv[4])
    # main(False, False)
    main(True, True)
