import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import math

cmap = mcolors.LinearSegmentedColormap.from_list("",
                                                 [(0, "black"),
                                                  (0.5, "yellow"),
                                                  (1, "red")], N=256)
# cmap=plt.get_cmap('YlOrRd')

# Initialise neuron directional preference
def get_dir_pref(pos):
    x, y, _ = pos.T
    if x % 2 == 0 and y % 2 == 0:
        return [0, 1]  # N
    elif x % 2 != 0 and y % 2 != 0:
        return [0, -1]  # S
    elif x % 2 != 0 and y % 2 == 0:
        return [-1, 0]  # W
    elif x % 2 == 0 and y % 2 != 0:
        return [1, 0]  # E


# Compute Euclidean distance of two neurons lying on periodic network grid
def get_neuron_distance_periodic(grid_w, grid_h, pre_pos, post_pos):
    x1, y1, _ = pre_pos.T
    x2, y2, _ = post_pos.T
    delta_x = abs(x1 - x2)
    delta_y = abs(y1 - y2)
    return math.sqrt(math.pow(min(delta_x, grid_w - delta_x), 2) +
                     math.pow(min(delta_y, grid_h - delta_y), 2))


# Get the synapses for a given neuron
def get_neuron_connections(neuron_id, connections):
    neuron_connections = list()
    for connection in connections:
        if connection[0] == neuron_id or connection[1] == neuron_id or id == -1:
            neuron_connections.append(connection)
    return neuron_connections


# Normalise a value to min and max
def normalise(val, minimum, maximum):
    return (val - minimum) / float(maximum - minimum)


# Shift centre of connectivity in appropriate direction
def shift_centre_connectivity(presyn_pos, dir, shift_param, n_row, n_col):
    centre = np.copy(presyn_pos[:3])

    # If N or S
    if np.all(dir == [0, 1]) or np.all(dir == [0, -1]):
        centre[1] -= dir[1] * shift_param
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


# Compute the firing rate from spike trains
def compute_firing_rates_from_spike_trains(spike_trains, t, num_neurons):
    firing_rates = [None] * num_neurons
    for i, spike_train in enumerate(spike_trains):
        spike_train = [x for x in spike_train if x <= t]
        if len(spike_train) == 0:
            firing_rates[i] = 0
        else:
            firing_rates[i] = len(spike_train) * (1000.0 / t)
    return firing_rates


# Plot the firing rate of a population at a given time
def plot_population_firing_rate(spike_trains, neuron_positions, times, grid_row, grid_col, filepath):
    # plt.style.use('dark_background')
    num_times = len(times)
    fig, axs = plt.subplots(ncols=num_times)
    fig.suptitle('Population firing rates')
    num_neurons = grid_col * grid_row

    for i, ax in enumerate(axs):
        t = times[i]
        ax.set_xlim(0, grid_col - 1)
        ax.set_ylim(0, grid_row - 1)
        ax.set_title(str(t) + 'ms')
        ax.set_facecolor('k')
        # ax.get_xaxis().set_ticks([])
        # ax.get_yaxis().set_ticks([])

        ax.set_aspect('equal')
        firing_rates = compute_firing_rates_from_spike_trains(spike_trains, t, num_neurons)
        firing_rate_max = max(firing_rates)

        if firing_rate_max != 0:
            for j, val in enumerate(firing_rates):
                norm_firing_rate = normalise(val, 0, firing_rate_max)
                ax.scatter(neuron_positions[j][0], neuron_positions[j][1], s=10,
                           c=norm_firing_rate, cmap=cmap, norm=plt.Normalize(0, 1))
    # plt.colorbar(cmap)
    fig.tight_layout()
    if filepath:
        plt.savefig(filepath + '.png', facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.show()


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
                       s=10, c=norm, cmap=cmap, norm=plt.Normalize(0, 1))
    # plt.colorbar(cmap)
    fig.tight_layout()
    if filepath:
        plt.savefig(filepath, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.show()
