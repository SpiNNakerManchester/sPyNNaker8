import matplotlib.pyplot as plt
import random
import numpy as np
from operator import add
import time

positions = []
head_dir = []
speed = 3
running = True


def constant_direction(speed, direction):
    speed = speed
    head_dir = direction
    positions.append([0, 0])

    while(running):
        if(direction == [0, 1]):
            positions.append(map(add, positions[-1], [0, 1]))
        elif(direction == [0, -1]):
            positions.append(map(add, positions[-1], [0, -1]))
        elif (direction == [1, 0]):
            positions.append(map(add, positions[-1], [1, 0]))
        elif (direction == [-1, 0]):
            positions.append(map(add, positions[-1], [-1, 0]))
        print positions[-1]

# def one_dim_walk_vertical(length):
#     directions = [(0, 1), (0, -1)]
#     start = random.randint(1, length+1)
#     head_dir = random.choice(directions)
#     positions.append((0, start))
#
#     while(running):
#         step = next_step(directions, length)
#         head_dir = step
#         positions.append(positions[-1] + step)
#         print positions[-1]
#
#
# def one_dim_walk_horizontal(length):
#     directions = [(1, 0), (-1, 0)]
#     start = random.randint(1, length+1)
#     head_dir = random.choice(directions)
#     positions.append([start, 0])
#
#     while(running):
#         step = next_step(directions, length)
#         head_dir = step
#         positions.append(positions[-1] + step)


# def next_step(directions, length):
#     while(True):
#         step = random.choice(directions)
#         if(1 <= positions[-1] + step <= length):
#             return step


def stop():
    running = False


def get_speed():
    return speed


def get_head_dir():
    return head_dir


def get_trajectory():
    return positions

def plot_trajectory():
    plt.plot(positions)
    plt.show()


constant_direction(2, [0,1])
time.sleep(2)
running = False