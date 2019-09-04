import random

import numpy as np
import random_walk_step as RandomWalkStep
import utilities as util


class RandomWalkCardinal:
    """
    Simulate a random walk in any of the 4 cardinal directions
    """

    def __init__(self, speed, timestep, grid_x, grid_y):
        self.dirs = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        self.head_dir = self.update_head_dir(True)
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
        if init:
            self.head_dir = random.choice(self.dirs)
        elif random.randint(0, 1) == 1:
            other_dirs = list(self.dirs)
            other_dirs.remove(self.head_dir)
            self.head_dir = random.choice(other_dirs)
        return self.head_dir

    def next_step(self):
        """
        Simulate a single step

        Choose a random cardinal direction and move step_size units
        :return: [list] the change in x and y coordinates
        """
        while True:
            new_head_dir = self.update_head_dir(False)
            change_xy = np.multiply(
                [self.step_size, self.step_size],
                new_head_dir
            )
            position = np.add(self.positions[-1], change_xy)

            # Check if within boundaries
            if self.within_boundary(position):
                self.head_dir = new_head_dir
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

    def get_velocity(self):
        """
        Create a new Step instance with the change in x,y coordinates and head direction

        :return: Step object
        """
        next_step = self.next_step()
        return RandomWalkStep.Step(next_step[0], next_step[1], self.head_dir)

    def get_trajectory(self, until_time):
        """
        Get the trajectory of the random walk up until a specific time

        :param until_time: end time of trajectory
        :return: [nested list] containing timestamp and the position
        """
        to_index = (until_time) / self.timestep
        trajectory = []
        for i in range(to_index + 1):
            pos = self.positions[i]
            trajectory.append([pos[0], pos[1]])
        return trajectory


if __name__ == "__main__":
    timestep = 1  # ms
    runtime = 1000  # ms
    x_lim = 200  # cm
    y_lim = 200  # cm

    # Direction: North
    # Speed: 2m/s
    # Timestep: 1000ms (generating movement every Xms)
    walk = RandomWalkCardinal(2, timestep, x_lim, y_lim)

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
