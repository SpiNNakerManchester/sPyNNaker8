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
