from operator import add
import math

# Walk in given direction at a constant speed


# Direction: direction vector
# Speed: magnitude
class StraightWalk:

    def __init__(self, speed, init_dir):
        self.speed = speed
        self.dir = init_dir
        self.positions = [[0, 0]]

    def next_step(self):
        position = [0, 0]
        if self.head_dir == [0, 1]:
            position = map(add, self.positions[-1], [0, 1 * self.speed])
        elif self.head_dir == [0, -1]:
            position = map(add, self.positions[-1], [0, -1 * self.speed])
        elif self.head_dir == [1, 0]:
            position = map(add, self.positions[-1], [1 * self.speed, 0])
        elif self.head_dir == [-1, 0]:
            position = map(add, self.positions[-1], [-1 * self.speed, 0])
        self.positions.append(position)

    def get_velocity(self):
        self.next_step()
        return [self.speed, self.head_dir]

    def get_positions(self, timestep):
        trajectory = [None] * len(self.positions)
        for i in range(len(self.positions)):
            trajectory[i] = [[i * timestep, self.positions[i]]]
        return trajectory

