ICUB_VOR_VENV_POP_SIZE = 2

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
        'L_count', simulator.no_machine_time_steps, simulator.placements,
        simulator.buffer_manager, simulator.machine_time_step)
    return left_count.tolist()


def get_r_count(icub_vor_env_pop, simulator):
    b_vertex = icub_vor_env_pop._vertex
    right_count = b_vertex.get_data(
        'R_count', simulator.no_machine_time_steps, simulator.placements,
        simulator.buffer_manager, simulator.machine_time_step)
    return right_count.tolist()


def get_head_pos(icub_vor_env_pop, simulator):
    b_vertex = icub_vor_env_pop._vertex
    head_positions = b_vertex.get_data(
        'head_pos', simulator.no_machine_time_steps, simulator.placements,
        simulator.buffer_manager, simulator.machine_time_step)
    return head_positions.tolist()


def get_head_vel(icub_vor_env_pop, simulator):
    b_vertex = icub_vor_env_pop._vertex
    head_velocities = b_vertex.get_data(
        'head_vel', simulator.no_machine_time_steps, simulator.placements,
        simulator.buffer_manager, simulator.machine_time_step)
    return head_velocities.tolist()
