from math import radians


# Initialise neuron directional preference
def init_dir_pref(pos):
    x, y, z = pos.T
    if x % 2 == 0 and y % 2 == 0:
        return radians(0)  # N
    elif x % 2 != 0 and y % 2 != 0:
        return radians(180)  # S
    elif x % 2 != 0 and y % 2 == 0:
        return radians(270)  # W
    elif x % 2 == 0 and y % 2 != 0:
        return radians(90)  # E
