from operator import add
import math
import numpy as np


# Walk in given direction at a constant speed
class StraightWalk:

    def __init__(self, head_dir):
        self.head_dir = head_dir
        self.positions = [[0, 0]]
        self.step = None

    def next_step(self):
        step = np.multiply(
            [1, 1],
            self.head_dir
        )
        position = np.add(self.positions[-1], step)
        self.positions.append(position)

        return step

    def get_velocity(self):
        return [self.next_step(), self.head_dir]

    def get_positions(self, time, timestep):
        index = int(time / timestep)
        trajectory = [None] * index
        for i in range(index):
            trajectory[i] = [[i * timestep, self.positions[i]]]
        return trajectory
