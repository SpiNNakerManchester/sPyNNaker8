# Provides helpfer functions for modelling grid cells and plotting results

import math
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

# Colourmaps
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
    """
    Plot the initialisation order of neurons in a population
    :param neuron_positions: positions of neuron on grid
    :param directory: directory to save file to
    """
    for i, pos in enumerate(neuron_positions):
        plt.scatter(pos[0], pos[1],
                    c=i, norm=plt.Normalize(0, 25), cmap="Greys")
    plt.savefig(directory + 'neuron_order.png', bbox_inches='tight', dpi=150)
    plt.clf()


def plot_gc_inh_connections(neuron_ids, neuron_positions, max_weight, connection_list, n_col, n_row, rad, shift,
                            directory):
    """
    Plot strength of neuron connections
    :param neuron_ids: Population IDs of neurons
    :param neuron_positions: (x,y) neuron positions
    :param max_weight: maximum weight value
    :param connection_list: list of connection tuples
    :param n_col: number of columns in grid
    :param n_row: number of rows in grid
    :param rad: radius of connectivity
    :param shift: number of neurons to shift centre by
    :param directory: directory to save file to
    """
    for neuron_id in neuron_ids:
        fig, ax = plt.subplots(ncols=1)

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
                       c=normalise_round(float(connection[2]), 0, max_weight),
                       cmap=cmap_byr, norm=plt.Normalize(0, 1))
        fig.tight_layout()
        plt.savefig(directory + str(neuron_id) + '_neuron_connections.png', facecolor=fig.get_facecolor(),
                    bbox_inches='tight', dpi=150)
        plt.clf()


def get_dir_pref(pos):
    """
    Get directional preference of cell in 2D grid structure
    :param pos: position on grid
    :return: direction vector
    """
    x, y = pos
    if x % 2 == 0 and y % 2 == 0:
        return [-1, 0]  # W
    elif x % 2 != 0 and y % 2 != 0:
        return [1, 0]  # E
    elif x % 2 != 0 and y % 2 == 0:
        return [0, -1]  # S
    elif x % 2 == 0 and y % 2 != 0:
        return [0, 1]  # N


def get_neuron_distance_periodic(grid_w, grid_h, pre_pos, post_pos):
    """
    Compute distance between two neurons on a grid with periodic boundaries
    :param grid_w: width of grid
    :param grid_h: height of grid
    :param pre_pos: presynaptic neuron position
    :param post_pos: postsynaptic neuron position
    :return: Euclidean distance
    """
    x1, y1 = pre_pos
    x2, y2 = post_pos
    delta_x = abs(x1 - x2)
    delta_y = abs(y1 - y2)
    return math.sqrt(math.pow(min(delta_x, grid_w - delta_x), 2) +
                     math.pow(min(delta_y, grid_h - delta_y), 2))


def get_neuron_connections(neuron_id, connections, bidirectional):
    """
    Get the connections for a single neuron
    :param neuron_id: ID of neuron
    :param connections: connection list
    :param bidirectional: Flag determining whether both incoming/outgoing connections are returned
    :return: subset of connections list
    """
    neuron_connections = list()
    for connection in connections:
        if connection[0] == neuron_id or (bidirectional and connection[1] == neuron_id or id == -1):
            neuron_connections.append(connection)
    return neuron_connections


def normalise_round(val, minimum, maximum):
    """
    Normalise a value between two values and round it to nearest integer
    :param val: value to normalise
    :param minimum: minimum boundary
    :param maximum: maximum boundary
    :return: integer value
    """
    return round((val - minimum) / float(maximum - minimum))


def normalise(val, minimum, maximum):
    """
    Normalise a value between two values
    :param val: value to normalise
    :param minimum: minimum boundary
    :param maximum: maximum boundary
    :return: value between 0 and 1
    """
    return (val - minimum) / float(maximum - minimum)


def shift_centre_connectivity(presyn_pos, dir, shift_param, n_row, n_col):
    """
    Shift centre of connectivity in appropriate direction
    :param presyn_pos: position of presynaptic neuron
    :param dir: direction preference
    :param shift_param: number of neurons to shift centre by
    :param n_row: number of rows in grid
    :param n_col: number of columns in grid
    :return:
    """
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


def plot_trajectory_infinite_1d(trajectory, dir, runtime, save):
    """
    Plot 1D trajectory
    :param trajectory: x or y positions
    :param dir: head direction
    :param runtime: simulation runtime
    :param save: flag to save figure
    """
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


# def plot_trajectory_2d_spikes(spiketrain, trajectory, x_lim, y_lim, folderpath):
#     plt.xlabel('x (cm)')
#     plt.xlim(0, x_lim)
#     plt.ylim(0, y_lim)
#     plt.ylabel('y (cm)')
#
#     plt.scatter(trajectory[-1, 0], trajectory[-1, 1], s=50, marker='o', c="b")
#     plt.plot(trajectory[:, 0], trajectory[:, 1], linestyle='-', color='k', linewidth=1)
#
#     plt.tick_params(axis='both', labelsize=9)
#     plt.savefig(folderpath + 'trajectory.png', bbox_inches='tight')


def plot_trajectory_2d(trajectory, x_lim, y_lim, folderpath):
    """
    Plot 2D trajectory in square environment
    :param trajectory: x and y positions
    :param x_lim: x axis boundary
    :param y_lim: y axis boundary
    :param folderpath: path to save figure to
    """
    plt.xlabel('x (cm)')
    plt.xlim(0, x_lim)
    plt.ylim(0, y_lim)
    plt.ylabel('y (cm)')

    plt.scatter(trajectory[0, 0], trajectory[0, 1], s=50, marker='o', c="r")
    plt.scatter(trajectory[-1, 0], trajectory[-1, 1], s=50, marker='o', c="b")
    plt.plot(trajectory[:, 0], trajectory[:, 1], linestyle='-', color='k', linewidth=1)

    plt.tick_params(axis='both', labelsize=9)
    plt.savefig(folderpath + 'trajectory.png', bbox_inches='tight')


def compute_max_firing_rate(spiketrains, runtime):
    """
    Compute maximum firing rate
    :param spiketrains: spike trains of neurins
    :param runtime: simulation runtime
    :return: float
    """
    rates = list()
    for spiketrain in spiketrains:
        rates.append(len(spiketrain) * (1000 / runtime))
    return max(rates)


# Compute the firing rate from spike trains
def compute_firing_rates_from_spike_trains(spike_trains, end_t, time_window):
    """
    Compute the firing rate over an interval
    :param spike_trains: spike trains
    :param end_t: until time
    :param time_window: from time
    :return:
    """
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
    """
    Plot population spike activity
    :param spike_trains: spike trains
    :param neuron_positions: neuron position list
    :param times: times to create plots at
    :param grid_row: rows in grid
    :param grid_col: columns in grid
    :param filepath: path to save figure to
    """
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
    """
    Plot membrane potential at a given time
    :param membrane_potentials: list of membrane potentials
    :param neuron_positions: list of neuron positions
    :param thresh_v: membrane threshold
    :param times: times at which to plot
    :param grid_row: rows in grid
    :param grid_col: columns in grid
    :param filepath: filr path to save figure to
    """
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
            norm = normalise_round(float(val), min_v, thresh_v)
            ax.scatter(x=neuron_positions[j][0], y=neuron_positions[j][1],
                       s=10, c=norm, cmap=cmap_byr, norm=plt.Normalize(0, 1))
    fig.tight_layout()
    if filepath:
        plt.savefig(filepath, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.show()


def dog_weight_connectivity_kernel(x, alpha, gamma, beta):
    """
    Compute difference of gaussian connectivity weight
    :param x: euclidean distance
    :param alpha:
    :param gamma:
    :param beta:
    :return: weight
    """
    mag_x = np.linalg.norm(x)
    return (alpha * math.exp(-gamma * np.square(mag_x))) - (math.exp(-beta * np.square(mag_x)))


def get_max_value_from_pop(neuron_data_array):
    """
    Get maximum value from variable of population
    :param neuron_data_array:
    :return:
    """
    max_val = -1000000
    for neuron_data in neuron_data_array:
        neuron_data = map(float, neuron_data)
        if max(neuron_data) > max_val:
            max_val = max(neuron_data)
    return max_val


def get_min_value_from_pop(neuron_data_array):
    """
    Get minimum value from variable of population
    :param neuron_data_array:
    :return:
    """
    min_val = 1000000
    for neuron_data in neuron_data_array:
        neuron_data = map(float, neuron_data)
        if min(neuron_data) < min_val:
            min_val = min(neuron_data)
    return min_val


def get_avg_gsyn_from_pop(neuron_data_array):
    """
    Get average syn from po;ulation
    :param neuron_data_array:
    :return:
    """
    avg = []
    for neuron_data in neuron_data_array:
        neuron_data = map(float, neuron_data)
        filtered = filter(lambda a: a != 0, neuron_data)
        if len(filtered) > 0:
            avg.append(sum(filtered) / len(filtered))
    return sum(avg) / len(avg)


def get_max_firing_rate(spiketrains):
    """
    Get maximum firing rate
    :param spiketrains:
    :return:
    """
    if spiketrains is None or spiketrains == 0:
        return 0

    max_val = -1000000
    for spiketrain in spiketrains:
        if len(spiketrain) > max_val:
            max_val = len(spiketrain)
    return max_val