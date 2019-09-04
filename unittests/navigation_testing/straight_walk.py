import numpy as np
import random_walk_step as RandomWalkStep

class StraightWalk:
    """
    Simulate an agent moving in a straight line in a given direction at a constant speed
    """

    def __init__(self, head_dir):
        self.head_dir = head_dir
        self.positions = [[0, 0]]
        self.step = None

    def next_step(self):
        """
        Generate change in x and y positions
        :return: change in x and y positions
        """
        change_xy = np.multiply(
            [1, 1],
            self.head_dir
        )
        position = np.add(self.positions[-1], change_xy)
        self.positions.append(position)

        return change_xy

    def get_velocity(self):
        """
        Get change in position and direction
        :return: Step object
        """
        next_step = self.next_step()
        return RandomWalkStep.Step(next_step[0], next_step[1], self.head_dir)

    def get_trajectory(self, time, timestep):
        """
        Get list of changes in position as a trajectory
        :param time: end time
        :param timestep: timestep between each step in trajectory
        :return: list of positions
        """
        to_index = (time * 1000) / timestep
        trajectory = []
        for i in range(to_index + 1):
            trajectory.append([i * timestep, self.positions[i]])
        return trajectory
