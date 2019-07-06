import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math


# Initialise neuron directional preference
def get_dir_pref(pos):
    x, y = pos.T
    if x % 2 == 0 and y % 2 == 0:
        return [0, 1]  # N
    elif x % 2 != 0 and y % 2 != 0:
        return [0, -1]  # S
    elif x % 2 != 0 and y % 2 == 0:
        return [-1, 0]  # W
    elif x % 2 == 0 and y % 2 != 0:
        return [1, 0]  # E


# Compute Euclidean distance of two neurons lying on periodic network grid
def get_neuron_distance_periodic(grid_w, grid_h, pos1, pos2):
    x1, y1 = pos1.T
    x2, y2 = pos2.T
    delta_x = abs(x1 - x2)
    delta_y = abs(y1 - y2)
    return math.sqrt(math.pow(min(delta_x, grid_w - delta_x), 2) +
                     math.pow(min(delta_y, grid_h - delta_y), 2))


# Get the synapses for a given neuron
def get_neuron_connections(neuron_id, connections):
    neuron_connections = list()
    for connection in connections:
        if connection[0] == neuron_id or connection[1] == neuron_id:
            neuron_connections.append(connection)
    return neuron_connections


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

"""
# Compute the firing rate
def compute_firing_rates_from_spike_trains(spike_trains, t, num_neurons):
    firing_rates = [None] * num_neurons
    for i in range(num_neurons):
        firing_rates[i] = len(spike_trains[i]) * (1000 / t)
    return firing_rates


# Plot the firing rate of a population at a given time
def plot_population_firing_rate(spike_trains, neuron_positions, t, grid_row, grid_col, save):
    fig = plt.figure()
    fig.suptitle('Normalised firing rate population activity at time ' + str(t) + 'ms')
    plt.xticks([0,grid_col])
    plt.yticks([0, grid_row])
    num_neurons = len(spike_trains)
    firing_rates = compute_firing_rates_from_spike_trains(spike_trains, t, num_neurons)

    norm_firing_rates = [None] * num_neurons
    firing_rate_min = min(firing_rates)
    firing_rate_max = max(firing_rates)

    for i, val in enumerate(firing_rates):
        norm_firing_rates[i] = (val - firing_rate_min) / float((firing_rate_max - firing_rate_min))  # Normalise firing rates
        plt.scatter(x=neuron_positions[i][0], y=neuron_positions[i][1],
                    s=10, c=norm_firing_rates[i], cmap=plt.get_cmap('RdGy'))
    plt.colorbar()
    plt.show()

# Plot spike train activity at a given time
def plot_population_spike_activity(grid_row, grid_col, spike_trains, neuron_positions, times):
    num_times = len(times)
    fig, axs = plt.subplots(num_times)
    fig.suptitle('Spike train population activity')
    plt.ylim(0, grid_row)
    plt.xlim(0, grid_col)

    for i in range(0, num_times):
        t = times[i]

        for neuron_id in range(0, len(spike_trains)):
            if t in spike_trains[neuron_id]:
                pos = neuron_positions[neuron_id]
                axs[i].scatter(pos[0], pos[1])

    plt.show()


# Plot membrane potential activity at a given time
def plot_population_membrane_potential_activity(grid_row, grid_col, membrane_potentials, neuron_positions, times):
    num_times = len(times)
    fig, axs = plt.subplots(num_times)
    fig.suptitle('Membrane potential population activity')
    plt.ylim(0, grid_row)
    plt.xlim(0, grid_col)

    for i in range(0, num_times):
        t = times[i]

        # for neuron_id in range(0, len(spike_trains)):
        #     if t in spike_trains[neuron_id]:
        #         pos = neuron_positions[neuron_id]
        #         axs[i].scatter(pos[0], pos[1])

# TODO: function to take trajectory and spike trains and superimpose

# def plot_neuron_fire_heatmap(spiketrains):
#     spike_freq = np.zeros(len(spiketrains))
#     fig, ax = plt.subplots()
#     im = ax.imshow(spike_freq)
#
#     ax.set_title("Harvest of local farmers (in tons/year)")
#     fig.tight_layout()
#     plt.show()
#
#
#
#     len(pop_exc.get_data('spikes').segments[0].spiketrains[4])
"""
