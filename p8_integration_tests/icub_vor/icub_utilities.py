import numpy as np
import pylab as plt
import matplotlib as mlib
import copy

# ensure we use viridis as the default cmap
plt.viridis()

mlib.use('Agg')
# ensure we use the same rc parameters for all matplotlib outputs
mlib.rcParams.update({'font.size': 24})
mlib.rcParams.update({'errorbar.capsize': 5})
mlib.rcParams.update({'figure.autolayout': True})
viridis_cmap = mlib.cm.get_cmap('viridis')

ICUB_VOR_VENV_POP_SIZE = 2
POS_TO_VEL = 2 * np.pi * 0.001


# Examples of get functions for variables
def get_error(icub_vor_env_pop, simulator):
    b_vertex = icub_vor_env_pop._vertex
    error = b_vertex.get_data(
        'error', simulator.no_machine_time_steps, simulator.placements,
        simulator.buffer_manager, simulator.machine_time_step)
    return error.tolist()


def get_l_count(icub_vor_env_pop, simulator):
    b_vertex = icub_vor_env_pop._vertex
    left_count = b_vertex.get_data(
        'l_count', simulator.no_machine_time_steps, simulator.placements,
        simulator.buffer_manager, simulator.machine_time_step)
    return left_count.tolist()


def get_r_count(icub_vor_env_pop, simulator):
    b_vertex = icub_vor_env_pop._vertex
    right_count = b_vertex.get_data(
        'r_count', simulator.no_machine_time_steps, simulator.placements,
        simulator.buffer_manager, simulator.machine_time_step)
    return right_count.tolist()


def get_eye_pos(icub_vor_env_pop, simulator):
    b_vertex = icub_vor_env_pop._vertex
    eye_positions = b_vertex.get_data(
        'eye_pos', simulator.no_machine_time_steps, simulator.placements,
        simulator.buffer_manager, simulator.machine_time_step)
    return eye_positions.tolist()


def get_eye_vel(icub_vor_env_pop, simulator):
    b_vertex = icub_vor_env_pop._vertex
    eye_velocities = b_vertex.get_data(
        'eye_vel', simulator.no_machine_time_steps, simulator.placements,
        simulator.buffer_manager, simulator.machine_time_step)
    return eye_velocities.tolist()


def generate_head_position_and_velocity(time, dt=0.001):
    i = np.arange(0, time, dt)
    pos = -np.sin(i * 2 * np.pi)
    vel = -np.cos(i * 2 * np.pi)
    return pos, vel


def retrieve_and_package_results(icub_vor_env_pop, simulator):
    # Get the data from the ICubVorEnv pop
    errors = np.asarray(get_error(icub_vor_env_pop=icub_vor_env_pop, simulator=simulator)).ravel()
    l_counts = get_l_count(icub_vor_env_pop=icub_vor_env_pop, simulator=simulator)
    r_counts = get_r_count(icub_vor_env_pop=icub_vor_env_pop, simulator=simulator)
    rec_eye_pos = np.asarray(get_eye_pos(
        icub_vor_env_pop=icub_vor_env_pop, simulator=simulator)).ravel()
    rec_eye_vel = np.asarray(get_eye_vel(
        icub_vor_env_pop=icub_vor_env_pop, simulator=simulator)).ravel()
    results = {
        'errors': errors,
        'l_counts': l_counts,
        'r_counts': r_counts,
        'rec_eye_pos': rec_eye_pos,
        'rec_eye_vel': rec_eye_vel,
    }
    return results


def highlight_area(ax, runtime, start_nid, stop_nid):
    ax.fill_between(
        [0, runtime], start_nid, stop_nid,
        color='grey', alpha=0.1,
    )


def plot_results(results_dict, simulation_parameters, name):
    # unpacking results
    errors = results_dict['errors']
    l_counts = results_dict['l_counts']
    r_counts = results_dict['r_counts']
    rec_eye_pos = results_dict['rec_eye_pos']
    rec_eye_vel = results_dict['rec_eye_vel']

    # unpacking simulation params
    runtime = simulation_parameters['runtime']
    error_window_size = simulation_parameters['error_window_size']
    vn_spikes = simulation_parameters['vn_spikes']
    cf_spikes = simulation_parameters['cf_spikes']
    perfect_eye_pos = simulation_parameters['perfect_eye_pos']
    perfect_eye_vel = simulation_parameters['perfect_eye_vel']
    vn_size = simulation_parameters['vn_size']
    cf_size = simulation_parameters['cf_size']

    # plot the data from the ICubVorEnv pop
    x_plot = [(n) for n in range(0, runtime, error_window_size)]
    fig = plt.figure(figsize=(15, 20), dpi=400)
    # Spike raster plot
    ax = plt.subplot(5, 1, 1)
    highlight_area(ax, runtime, vn_size // 2, vn_size)
    first_half_filter = vn_spikes[:, 0] < vn_size // 2
    second_half_filter = ~first_half_filter
    plt.scatter(
        vn_spikes[second_half_filter, 1], vn_spikes[second_half_filter, 0],
        s=1, color=viridis_cmap(.75))
    plt.scatter(
        vn_spikes[first_half_filter, 1], vn_spikes[first_half_filter, 0],
        s=1, color=viridis_cmap(.25))

    plt.xlim([0, runtime])
    plt.ylim([-0.1, vn_size+0.1])
    # L/R counts
    plt.subplot(5, 1, 2)
    plt.plot(x_plot, l_counts, 'o', color=viridis_cmap(.25), label="l_counts")
    plt.plot(x_plot, r_counts, 'o', color=viridis_cmap(.75), label="r_counts")
    plt.legend(loc="best")
    plt.xlim([0, runtime])
    # Positions and velocities
    plt.subplot(5, 1, 3)
    plt.plot(x_plot, rec_eye_pos, label="rec. eye position")
    plt.plot(x_plot, rec_eye_vel, label="rec. eye velocity")
    plt.plot(np.tile(perfect_eye_pos, runtime // 1000), label="eye position", ls=':')
    plt.plot(np.tile(perfect_eye_vel, runtime // 1000), label="eye velocity", ls=':')
    plt.legend(loc="best")
    plt.xlim([0, runtime])
    # Errors
    plt.subplot(5, 1, 4)
    plt.plot(x_plot, errors, label="recorded error")

    eye_pos_diff = np.tile(perfect_eye_pos[::error_window_size], runtime // 1000) - rec_eye_pos.ravel()
    eye_vel_diff = np.tile(perfect_eye_vel[::error_window_size], runtime // 1000) - rec_eye_vel.ravel()
    reconstructed_error = eye_pos_diff + eye_vel_diff

    plt.plot(x_plot, reconstructed_error, color='k', ls=":", label="reconstructed error")
    plt.plot(x_plot, eye_pos_diff,
             label="eye position diff")
    plt.plot(x_plot, eye_vel_diff,
             label="eye velocity diff")
    plt.legend(loc="best")
    plt.xlim([0, runtime])
    # Error spikes
    ax2 = plt.subplot(5, 1, 5)
    highlight_area(ax2, runtime, cf_size // 2, cf_size)
    first_half_filter = cf_spikes[:, 0] < cf_size // 2
    second_half_filter = ~first_half_filter
    plt.scatter(
        cf_spikes[second_half_filter, 1], cf_spikes[second_half_filter, 0],
        s=1, color=viridis_cmap(.75))
    plt.scatter(
        cf_spikes[first_half_filter, 1], cf_spikes[first_half_filter, 0],
        s=1, color=viridis_cmap(.25))
    # plt.legend(loc="best")
    plt.xlim([0, runtime])
    plt.ylim([-0.1, cf_size+0.1])
    plt.xlabel("Time (ms)")
    save_figure(plt, name, extensions=[".png", ])
    plt.close(fig)


def remap_odd_even(original_spikes, size):
    remapped_spikes = copy.deepcopy(original_spikes)
    mapping = np.arange(size)
    mapping[::2] = np.arange(0, size, 2) // 2
    mapping[1::2] = size // 2 + np.arange(size - 1, 0, -2) // 2
    remapped_spikes[:, 0] = mapping[remapped_spikes[:, 0].astype(int)]
    return remapped_spikes


def remap_second_half_descending(original_spikes, size):
    remapped_spikes = copy.deepcopy(original_spikes)
    mapping = np.arange(size)
    mapping[:size // 2] = np.arange(0, size // 2, 1)
    mapping[size // 2:] = np.arange(size, size // 2, -1)
    remapped_spikes[:, 0] = mapping[remapped_spikes[:, 0].astype(int)]
    return remapped_spikes


def color_for_index(index, size, cmap=viridis_cmap):
    return cmap(index / (size + 1))


def write_sep():
    print("=" * 80)


def write_line():
    print("-" * 80)


def write_header(msg):
    write_sep()
    print(msg)
    write_line()


def write_short_msg(msg, value):
    print("{:40}:{:39}".format(msg, str(value)))


def write_value(msg, value):
    print("{:60}:{:19}".format(msg, str(value)))


def save_figure(plt, name, extensions=(".png",), **kwargs):
    for ext in extensions:
        write_short_msg("Plotting", name + ext)
        plt.savefig(name + ext, **kwargs)
