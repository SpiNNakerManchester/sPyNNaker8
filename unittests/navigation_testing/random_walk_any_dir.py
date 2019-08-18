import random

import numpy as np


# NOT YEY WORKING
class RandomWalkAny:

    def __init__(self, speed, timestep):
        # Cardinal directions and their weights
        self.directions = {
            (0, 1): 0,
            (1, 0): 0,
            (-1, 0): 0,
            (0, -1): 0,
        }
        self.prev_dir = self.update_head_dir(True)
        self.speed = speed / 10.0  # cm/ms
        self.timestep = timestep  # how often a new step is generated in ms
        self.unit_in_cm = 1  # moving 1 in any direction represents 1cm
        self.step_size = (self.speed * timestep) * self.unit_in_cm
        self.positions = [[0, 0]]
        self.step = None

    def update_head_dir(self, init):
        # Randomly choose whether to keep head direction
        if random.randint(0, 1) == 1 or init:
            # Choose new direction
            r1 = random.random()
            r2 = 1.0 - r1

            rand_ns = random.choice([(0, 1), (0, -1)])
            rand_we = random.choice([(1, 0), (-1, 0)])

            self.directions[rand_ns] = r1
            self.directions[rand_we] = r2
            return [rand_we[0], rand_ns[1]]
        return self.prev_dir

    # Returns change in x and y coordinates
    def next_step(self):
        new_dir = self.update_head_dir(False)
        step = np.multiply(
            [self.step_size, self.step_size],

        )
        position = np.add(self.positions[-1], step)
        self.positions.append(position)

        return step

    # Returns change in x and y coordinates and current head direction
    def get_velocity(self):
        return [self.next_step(), self.head_dir]

    def get_positions(self, time, timestep):
        index = int(time / timestep)
        trajectory = [None]
        for i in range(index):
            trajectory.append([[i * timestep, self.positions[i]]])
        return trajectory
