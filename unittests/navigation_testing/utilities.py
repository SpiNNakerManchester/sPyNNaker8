import math

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

cmap_byr = mcolors.LinearSegmentedColormap.from_list("",
                                                     [(0, "black"),
                                                      (0.5, "yellow"),
                                                      (1, "red")], N=256)

cmap_bcgyor = mcolors.LinearSegmentedColormap.from_list("",
                                                        [(0, "#001aff"),  # blue
                                                         (0.2, "#00ffea"),  # cyan
                                                         (0.4, "#00ff2f"),  # green
                                                         (0.6, "#fff700"),  # yellow
                                                         (0.8, "#ff8000"),  # orange
                                                         (1, "#ff0000")], N=256)  # red


def plot_neuron_init_order(neuron_positions, directory):
    for i, pos in enumerate(neuron_positions):
        plt.scatter(pos[0], pos[1],
                    c=i, norm=plt.Normalize(0, 25), cmap="Greys")
    plt.savefig(directory + 'neuron_order.png', bbox_inches='tight', dpi=150)
    plt.clf()


def plot_gc_inh_connections(neuron_ids, neuron_positions, max_weight, connection_list, n_col, n_row, rad, shift,
                            directory):
    for neuron_id in neuron_ids:
        fig, ax = plt.subplots(ncols=1)
        # fig.suptitle('Grid Cell Synapses')

        connections = get_neuron_connections(neuron_id, connection_list, False)
        ax.set_xlim(0, n_col - 1)
        ax.set_ylim(0, n_row - 1)
        ax.set_title("Neuron " + str(neuron_id))
        ax.get_xaxis().set_ticks([0, 10, 20, 30, 40, 50])
        ax.get_yaxis().set_ticks([0, 10, 20, 30, 40, 50])
        ax.set_aspect('equal')

        pos_x = (neuron_positions[neuron_id])[0]
        pos_y = (neuron_positions[neuron_id])[1]

        ax.scatter(pos_x, pos_y, s=50, marker='x', c="k")

        circle_args = {
            "edgecolor": 'k',
            "facecolor": None,
            "fill": False,
            "linestyle": '--'
        }
        orig_radius = plt.Circle(
            (pos_x, pos_y), rad, **circle_args
        )
        ax.add_patch(orig_radius)

        circle_args = {
            "edgecolor": 'r',
            "facecolor": None,
            "fill": False,
            "linestyle": '--'
        }
        shift_by = np.multiply(get_dir_pref((pos_x, pos_y)), shift)
        new_pos = [pos_x + shift_by[0], pos_y + shift_by[1]]
        new_radius = plt.Circle(
            (new_pos[0], new_pos[1]), rad, **circle_args
        )
        ax.add_patch(new_radius)

        ax.scatter(new_pos[0], new_pos[1], s=50, marker='x', c="r")

        for connection in connections:
            ax.scatter((neuron_positions[connection[1]])[0],
                       (neuron_positions[connection[1]])[1], marker='o', s=4,
                       c=normalise(float(connection[2]), 0, max_weight),
                       cmap=cmap_byr, norm=plt.Normalize(0, 1))
        fig.tight_layout()
        # fig.colorbar(plt, ax=axs.ravel().tolist())
        # scalebar = ScaleBar(0.29586, 'neurons', fixed_value=5)
        # plt.gca().add_artist(scalebar)
        plt.savefig(directory + str(neuron_id) + '_neuron_connections.png', facecolor=fig.get_facecolor(),
                    bbox_inches='tight', dpi=150)
        plt.clf()


# Initialise neuron directional preference
def get_dir_pref(pos):
    x, y = pos
    if x % 2 == 0 and y % 2 == 0:
        return [-1, 0]  # W
    elif x % 2 != 0 and y % 2 != 0:
        return [1, 0]  # E
    elif x % 2 != 0 and y % 2 == 0:
        return [0, -1]  # S
    elif x % 2 == 0 and y % 2 != 0:
        return [0, 1]  # N


# Compute Euclidean distance of two neurons lying on periodic network grid
def get_neuron_distance_periodic(grid_w, grid_h, pre_pos, post_pos):
    x1, y1 = pre_pos
    x2, y2 = post_pos
    delta_x = abs(x1 - x2)
    delta_y = abs(y1 - y2)
    return math.sqrt(math.pow(min(delta_x, grid_w - delta_x), 2) +
                     math.pow(min(delta_y, grid_h - delta_y), 2))


# Get the synapses for a given neuron
def get_neuron_connections(neuron_id, connections, bidirectional):
    neuron_connections = list()
    for connection in connections:
        if connection[0] == neuron_id or (bidirectional and connection[1] == neuron_id or id == -1):
            neuron_connections.append(connection)
    return neuron_connections


# Normalise a value to min and max
def normalise(val, minimum, maximum):
    return (val - minimum) / float(maximum - minimum)


# Shift centre of connectivity in appropriate direction
def shift_centre_connectivity(presyn_pos, dir, shift_param, n_row, n_col):
    centre = np.copy(presyn_pos)

    # If N or S
    if np.all(dir == [0, 1]) or np.all(dir == [0, -1]):
        centre[1] += dir[1] * shift_param
        # Check if within network boundary
        if centre[1] < 0:
            centre[1] += n_row
        elif centre[1] >= n_row:
            centre[1] -= n_row
    # If E or W
    elif np.all(dir == [1, 0]) or np.all(dir == [-1, 0]):
        centre[0] += dir[0] * shift_param
        # Check if within network boundary
        if centre[0] < 0:
            centre[0] += n_col
        elif centre[0] >= n_col:
            centre[0] -= n_col
    return centre


# Plot the agent 1D trajectory
def plot_trajectory_infinite_1d(trajectory, dir, runtime, save):
    fig, ax = plt.subplots()
    ax.set_title('Agent trajectory')
    ax.set_xlabel('Time (ms)')
    ax.set_xlim(0, runtime)
    ax.set_ylabel('Distance (m) in ' + str(dir) + ' direction')

    step_coordinate = 0
    if dir[0] == 0:
        step_coordinate = 1

    x = []
    y = []
    for step in trajectory:
        x.append(step[0][0])
        y.append((step[0][1])[step_coordinate])
    ax.plot(x, y, 'k-', linewidth=1)

    fig.tight_layout()
    plt.show()
    if save:
        plt.savefig('trajectory.png', bbox_inches='tight')


def compute_max_firing_rate(spiketrains, runtime):
    rates = list()
    for spiketrain in spiketrains:
        rates.append(len(spiketrain) * (1000 / runtime))
    return max(rates)


# Compute the firing rate from spike trains
def compute_firing_rates_from_spike_trains(spike_trains, end_t, time_window):
    if time_window is None:
        start_t = 0
    else:
        start_t = max(0, end_t - time_window)
    firing_rates = [None] * len(spike_trains)
    for i, spike_train in enumerate(spike_trains):
        spikes = [x for x in spike_train if start_t <= x <= end_t]
        if len(spikes) == 0:
            firing_rates[i] = 0
        else:
            firing_rates[i] = len(spikes) * (1000.0 / (end_t - start_t))
    return firing_rates


# Plot spike train activity at a given time
def plot_population_spike_activity(spike_trains, neuron_positions, times, grid_row, grid_col, filepath):
    num_times = len(times)
    fig, axs = plt.subplots(ncols=num_times)
    fig.suptitle('Spike train population activity')

    for i, ax in enumerate(axs):
        t = times[i]
        ax.set_xlim(0, grid_col - 1)
        ax.set_ylim(0, grid_row - 1)
        ax.set_title(str(t) + 'ms')
        ax.set_facecolor('k')
        ax.get_xaxis().set_ticks([0, grid_col])
        ax.get_yaxis().set_ticks([0, grid_row])
        ax.set_aspect('equal')
        for neuron_id in range(0, len(spike_trains)):
            if t in spike_trains[neuron_id]:
                pos = neuron_positions[neuron_id]
                ax.scatter(pos[0], pos[1], color="White")

    fig.tight_layout()
    if filepath:
        plt.savefig(filepath, facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=150)
    plt.show()


# Plot membrane potential activity at a given time
def plot_population_membrane_potential_activity(membrane_potentials, neuron_positions, thresh_v, times,
                                                grid_row, grid_col, filepath):
    num_times = len(times)
    fig, axs = plt.subplots(ncols=num_times)
    fig.suptitle('Population membrane potential activity')

    for i, ax in enumerate(axs):
        t = times[i]
        ax.set_xlim(0, grid_col - 1)
        ax.set_ylim(0, grid_row - 1)
        ax.set_title(str(t) + 'ms')
        ax.set_facecolor('k')
        # ax.get_xaxis().set_ticks([])
        # ax.get_yaxis().set_ticks([])
        ax.set_aspect('equal')
        pop_v = membrane_potentials[t]
        min_v = float(min(pop_v))
        for j, val in enumerate(pop_v):
            norm = normalise(float(val), min_v, thresh_v)
            ax.scatter(x=neuron_positions[j][0], y=neuron_positions[j][1],
                       s=10, c=norm, cmap=cmap_byr, norm=plt.Normalize(0, 1))
    # plt.colorbar(cmap)
    fig.tight_layout()
    if filepath:
        plt.savefig(filepath, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.show()


def dog_weight_connectivity_kernel(x, alpha, gamma, beta):
    return (alpha * math.exp(-gamma * np.square(abs(x)))) - (math.exp(-beta * np.square(abs(x))))


def get_max_value_from_pop(neuron_data_array):
    max_val = -1000000
    for neuron_data in neuron_data_array:
        if max(neuron_data) > max_val:
            max_val = max(neuron_data)
    return max_val


def get_max_firing_rate(spiketrains):
    if spiketrains is None or spiketrains == 0:
        return 0

    max_val = -1000000
    for spiketrain in spiketrains:
        if len(spiketrain) > max_val:
            max_val = len(spiketrain)
    return max_val

# Returns the probability of creating an inhibitory connection between two grid cells
# def connect_two_gc_neurons():
