import random

import numpy as np
import random_walk_step
import utilities as util


class RandomWalkAny:
    """
    Simulate a random walk in any direction represented as a weighting list of the 4 cardinal directions
    """

    def __init__(self, speed, timestep, grid_x, grid_y):
        # Cardinal directions and their weights
        self.directions = {
            (0, 1): 0,
            (1, 0): 0,
            (-1, 0): 0,
            (0, -1): 0,
        }
        self.curr_dir = self.update_head_dir(True)
        self.speed = speed / 10.0  # cm/ms
        self.timestep = timestep  # how often a new step is generated (ms)
        self.unit_in_cm = 1  # distance per unit change in coordinates
        self.step_size = (self.speed * timestep) * self.unit_in_cm  # how many units to move every timestep
        self.positions = [[random.randint(0, grid_x),
                           random.randint(0, grid_y)]]  # initialise position to origin
        self.step = None
        self.max_x = grid_x  # maximum x coordinate in cm
        self.max_y = grid_y  # maximum y coordinate in cm

    def update_head_dir(self, init):
        """
               Randomly choose whether to keep the head direction
               :param init: flag for initial setup
               :return: head direction vector
               """
        # Randomly choose whether to keep head direction
        if random.randint(0, 1) == 1 or init:
            # Choose new direction
            r1 = random.random()
            r2 = 1.0 - r1

            rand_ns = random.choice([(0, 1), (0, -1)])
            rand_we = random.choice([(1, 0), (-1, 0)])

            self.directions = self.directions.fromkeys(self.directions, 0)  # clear weights
            self.directions[rand_ns] = r1
            self.directions[rand_we] = r2
            return [rand_ns, rand_we]
        return self.curr_dir

    def next_step(self):
        """
        Simulate a single step

        Choose a random cardinal direction and move step_size units
        :return: [list] the change in x and y coordinates
        """
        while True:
            new_directions = self.update_head_dir(False)
            change_y = np.multiply(self.step_size *
                                   self.directions.get(new_directions[0]), new_directions[0])
            change_x = np.multiply(self.step_size *
                                   self.directions.get(new_directions[1]), new_directions[1])

            change_xy = [change_x[0], change_y[1]]
            position = np.add(self.positions[-1], change_xy)

            # Check if within boundaries
            if self.within_boundary(position):
                self.curr_dir = new_directions
                self.positions.append(list(position))
                return change_xy

    def within_boundary(self, new_pos):
        """
                Check whether new position is within the boundaries
                :param new_pos: position
                :return: boolean
                """
        if (new_pos[0] <= self.max_x and new_pos[0] >= 0) and \
                (new_pos[1] <= self.max_y and new_pos[1] >= 0):
            return True
        return False

    # Returns change in x and y coordinates and current head direction
    def get_velocity(self):
        next_step = self.next_step()
        return random_walk_step.Step(next_step[0], next_step[1], self.curr_dir)

    def get_trajectory(self, until_time):
        """
        Get the trajectory of the random walk up until a specific time

        :param until_time: end time of trajectory
        :return: [nested list] containing timestamp and the position
        """
        to_index = until_time / self.timestep
        trajectory = []
        for i in range(to_index + 1):
            pos = self.positions[i]
            trajectory.append([pos[0], pos[1]])
        return trajectory

    def get_stepsize(self):
        return self.step_size


if __name__ == "__main__":
    timestep = 1  # ms
    runtime = 60000  # ms
    x_lim = 200  # cm
    y_lim = 200  # cm

    # Direction: North
    # Speed: 2m/s
    # Timestep: 1000ms (generating movement every Xms)
    walk = RandomWalkAny(2, timestep, x_lim, y_lim)

    # Simulate random walk
    for i in range(runtime / timestep):
        step = walk.get_velocity()
        step.print_step()

    # Output trajectory
    trajectory = walk.get_trajectory(runtime)
    util.plot_trajectory_2d(np.array(trajectory), x_lim, y_lim, "/home/nickybu/Desktop/")
    print
    "\nTrajectory: "
    for index, pos in enumerate(trajectory):
        print
        "Time=" + str(index * timestep) + ", pos=" + str(pos)
