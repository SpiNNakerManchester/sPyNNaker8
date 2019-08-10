import random
import numpy as np

class Step:
    def __init__(self, change_x, change_y, head_dir):
        self.change_x = change_x
        self.change_y = change_y
        self.head_dir = head_dir

    def print_step(self):
        print "Change in x coordinate: " + str(self.change_x) + "m"
        print "Change in y coordinate: " + str(self.change_y) + "m"
        print "Head direction: " + str(self.head_dir)


class RandomWalkCardinal:

    def __init__(self, head_dir, speed, timestep):
        self.dirs = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        self.head_dir = head_dir
        self.speed = speed / 10.0  # cm/ms
        self.timestep = timestep  # how often a new step is generated in ms
        self.unit_in_cm = 1  # moving 1 in any direction represents 1cm
        self.step_size = (self.speed * timestep) * self.unit_in_cm
        self.positions = [[0, 0]]
        self.step = None

    # Returns change in x and y coordinates
    def next_step(self):
        new_head_dir = random.choice(self.dirs)
        self.head_dir = new_head_dir

        change_xy = np.multiply(
            [self.step_size, self.step_size],
            new_head_dir
        )
        position = np.add(self.positions[-1], change_xy)
        self.positions.append(list(position))

        return change_xy

    # Returns change in x and y coordinates and current head direction
    def get_velocity(self):
        next_step = self.next_step()
        return Step(next_step[0], next_step[1], self.head_dir)
        # return [self.next_step(), self.head_dir]

    def get_positions(self, until_time):
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

    for i in range((runtime * 1000) / timestep):
        step = walk.get_velocity()
        step.print_step()

    trajectory = walk.get_positions(runtime)
    print "\nTrajectory: "
    for time, pos in trajectory:
        print "Time=" + str(time) + ", pos=" + str(pos)

