import matplotlib.pyplot as plt
import random
import numpy as np

steps = 100
speed = 1  # m/s
timestep_sec = 1000/1000  # how often (ms) a new step is taken
# x_constraint = 10  # metres
# y_constraint = 10  # metres
positions = list()
head_dir = 0  # direction in degrees. North is 0, clockwise
positions.append((0, 0))  # origin

for i in range(steps):
    # 50% chance to change direction
    if random.random() >= 0.5:
        head_dir = random.randint(0, 360)
    # change_x =





