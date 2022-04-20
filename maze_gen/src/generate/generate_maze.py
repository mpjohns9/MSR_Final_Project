import numpy as np
import random

def generate_array(difficulty):
    if difficulty == 'hard':
        grid = np.zeros(shape=(100, 100), dtype=np.int8)
    if difficulty == 'medium':
        grid = np.zeros(shape=(50, 50), dtype=np.int8)
    if difficulty == 'easy':
        grid = np.zeros(shape=(10, 10), dtype=np.int8)
    return grid

def mark(x, y, grid, frontier):
    grid[x, y] = 1
    if (grid[x-1, y] == 0) and (x-1 > 0):
        if (x-1, y) not in frontier:
            frontier.append((x-1, y))
    if (grid[x+1, y] == 0) and (x+1 < grid.shape[1]-1):
        if (x+1, y) not in frontier:
            frontier.append((x+1, y))
    if (grid[x, y-1] == 0) and (y-1 > 0):
        if (x, y-1) not in frontier:
            frontier.append((x, y-1))
    if (grid[x, y+1] == 0) and (y+1 < grid.shape[0]-1):
        if (x, y+1) not in frontier:
            frontier.append((x, y+1))
    return grid, frontier

def neighbors(x, y, grid):
    n = []

    if (x > 0) and (grid[x-1, y] == 1):
        n.append((x-1, y))
    if (x < grid.shape[0]-1) and (grid[x+1, y] == 1):
        n.append((x+1, y))
    if (y > 0) and (grid[x, y-1] == 1):
        n.append((x, y-1))
    if (y < grid.shape[1]-1) and (grid[x, y+1] == 1):
        n.append((x, y+1))

    return n

def generate_maze(difficulty):
    grid = generate_array(difficulty)

    start = (random.randint(1, grid.shape[0]-2), random.randint(1, (grid.shape[0]-2)))

    frontier = []

    grid, frontier = mark(start[0], start[1], grid, frontier)

    while len(frontier) > 0:

        x, y = frontier.pop(random.randint(0, (len(frontier)-1)))
        neighbor_list = neighbors(x, y, grid)
        if len(neighbor_list) == 1:
            grid, frontier = mark(x, y, grid, frontier)

    found = False
    while found == False:
        start = (1, random.randint(1, grid.shape[1]-2))
        end = (8, random.randint(1, grid.shape[0]-2))
        if (grid[start[0], start[1]]) == 0 and (grid[end[0], end[1]] == 0):
            found = True

    grid[start[0], start[1]] = 8
    grid[end[0], end[1]] = 9
    return grid

def print_maze(grid):
    for i in range(grid.shape[0]):
        for each in grid[i]:
            if each == 1:
                print('0', end='')
            else:
                print('1', end='')
        print('')

# print(generate_maze('easy'))
