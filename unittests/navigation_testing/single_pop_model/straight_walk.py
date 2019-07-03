from operator import add

speed = 0
head_dir = []
positions = []


def __init__(speed, direction):
    speed = speed
    head_dir = direction
    positions = [[0, 0]]


def next_step():
    position = [0, 0]
    if(head_dir == [0, 1]):
        position = map(add, positions[-1], [0, 1])
    elif(head_dir == [0, -1]):
        position = map(add, positions[-1], [0, -1])
    elif (head_dir == [1, 0]):
        position = map(add, positions[-1], [1, 0])
    elif (head_dir == [-1, 0]):
        position = map(add, positions[-1], [-1, 0])
    positions.append(position)
    return position


def get_velocity():
    return [speed, next_step()]


def get_positions():
    return positions