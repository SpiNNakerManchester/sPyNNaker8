from operator import add
import math
import numpy as np
import random_walk_step as RandomWalkStep

# Walk in given direction at a constant speed
class StraightWalk:

    def __init__(self, head_dir):
        self.head_dir = head_dir
        self.positions = [[0, 0]]
        self.step = None

    def next_step(self):
        change_xy = np.multiply(
            [1, 1],
            self.head_dir
        )
        position = np.add(self.positions[-1], change_xy)
        self.positions.append(position)

        return change_xy

    def get_velocity(self):
        next_step = self.next_step()
        return RandomWalkStep.Step(next_step[0], next_step[1], self.head_dir)

    def get_trajectory(self, time, timestep):
        to_index = (time * 1000) / timestep
        trajectory = []
        for i in range(to_index + 1):
            trajectory.append([i * timestep, self.positions[i]])
        return trajectory
