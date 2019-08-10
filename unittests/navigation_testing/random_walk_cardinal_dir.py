import random
import numpy as np


class Step:
    """
    Represents a step taken by the agent.
    Contains the change in x and y coordinates and head direction
    """

    def __init__(self, change_x, change_y, head_dir):
        self.change_x = change_x
        self.change_y = change_y
        self.head_dir = head_dir

    def print_step(self):
        """
        Print the current step's details to console
        """
        print "Change in x coordinate: " + str(self.change_x) + "m"
        print "Change in y coordinate: " + str(self.change_y) + "m"
        print "Head direction: " + str(self.head_dir)


class RandomWalkCardinal:
    """
    Simulate a random walk in any of the 4 cardinal directions
    """

    def __init__(self, head_dir, speed, timestep):
        self.dirs = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        self.head_dir = head_dir
        self.speed = speed / 10.0  # cm/ms
        self.timestep = timestep  # how often a new step is generated (ms)
        self.unit_in_cm = 1  # distance per unit change in coordinates
        self.step_size = (self.speed * timestep) * self.unit_in_cm  # how many units to move every timestep
        self.positions = [[0, 0]] # initialise position to origin
        self.step = None

    def next_step(self):
        """
        Simulate a single step

        Choose a random cardinal direction and move step_size units
        :return: [list] the change in x and y coordinates
        """
        new_head_dir = random.choice(self.dirs)
        self.head_dir = new_head_dir

        change_xy = np.multiply(
            [self.step_size, self.step_size],
            new_head_dir
        )

        # Update position
        position = np.add(self.positions[-1], change_xy)
        self.positions.append(list(position))

        return change_xy

    def get_velocity(self):
        """
        Create a new Step instance with the change in x,y coordinates and head direction

        :return: Step object
        """
        next_step = self.next_step()
        return Step(next_step[0], next_step[1], self.head_dir)

    def get_trajectory(self, until_time):
        """
        Get the trajectory of the random walk up until a specific time

        :param until_time: end time of trajectory
        :return: [nested list] containing timestamp and the position
        """
        to_index = (until_time * 1000) / self.timestep
        trajectory = []
        for i in range(to_index + 1):
            trajectory.append([i * timestep, self.positions[i]])
        return trajectory


if __name__ == "__main__":
    timestep = 1000  # ms
    runtime = 6  # seconds

    # Direction: North
    # Speed: 2m/s
    # Timestep: 1000ms (generating movement every Xms)
    walk = RandomWalkCardinal([0, 1], 2, timestep)

    # Simulate random walk
    for i in range((runtime * 1000) / timestep):
        step = walk.get_velocity()
        step.print_step()

    # Output trajectory
    trajectory = walk.get_trajectory(runtime)
    print "\nTrajectory: "
    for time, pos in trajectory:
        print "Time=" + str(time) + ", pos=" + str(pos)

