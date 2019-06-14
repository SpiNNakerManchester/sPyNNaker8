# Initialise neuron directional preference
def get_dir_pref(pos):
    x, y, z = pos.T
    if x % 2 == 0 and y % 2 == 0:
        return [0, 1]  # N
    elif x % 2 != 0 and y % 2 != 0:
        return [0, -1]  # S
    elif x % 2 != 0 and y % 2 == 0:
        return [-1, 0]  # W
    elif x % 2 == 0 and y % 2 != 0:
        return [1, 0]  # E
