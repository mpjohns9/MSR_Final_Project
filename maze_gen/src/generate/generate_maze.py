import numpy as np
import random

class MazeGeneration:

    def __init__(self):

        self.grid = np.zeros((23, 23))
        self.grid[0] = [1 for c in range(self.grid.shape[0])]
        self.grid[-1] = [1 for c in range(self.grid.shape[0])]

        self.grid[:, 0] = [1 for c in range(self.grid.shape[1])]
        self.grid[:, -1] = [1 for c in range(self.grid.shape[1])]

        self.tiles = {
            'easy':
            {   'ninety_turn':
                dict(
                tile=np.array([
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 2, 2, 2, 2],
                [1, 1, 0, 2, 0, 0, 0],
                [1, 1, 0, 2, 0, 1, 1],
                [1, 1, 0, 2, 0, 1, 1]]),
                openings=['r', 'b']),
                'straight': 
                dict(
                tile=np.array([
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0],
                [2, 2, 2, 2, 2, 2, 2],
                [0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1]]),
                openings=['r', 'l']),
                'filled':
                dict(
                tile=np.ones(shape=(7, 7)),
                openings=[])
            },
            'medium':
            {
                'straight_angle':
                dict(
                tile=np.array([
                [1, 1, 1, 1, 0, 0, 2],
                [1, 1, 1, 0, 0, 2, 0],
                [1, 1, 0, 0, 2, 0, 0],
                [1, 0, 0, 2, 0, 0, 1],
                [0, 0, 2, 0, 0, 1, 1],
                [0, 2, 0, 0, 1, 1, 1],
                [2, 0, 0, 1, 1, 1, 1]]),
                openings=['tr', 'bl']),
                'angle_turn':
                dict(
                tile=np.array([
                [1, 1, 1, 1, 0, 0, 2],
                [1, 1, 1, 0, 0, 2, 0],
                [1, 1, 0, 0, 2, 0, 0],
                [1, 1, 0, 2, 0, 0, 1],
                [1, 1, 0, 2, 0, 1, 1],
                [1, 1, 0, 2, 0, 1, 1],
                [1, 1, 0, 2, 0, 1, 1]]),  
                openings=['tr', 'b'])
            },
            'hard':
            {
                't':
                dict(
                tile=np.array([
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0],
                [2, 2, 2, 2, 2, 2, 2],
                [0, 0, 0, 2, 0, 0, 0],
                [1, 1, 0, 2, 0, 1, 1],
                [1, 1, 0, 2, 0, 1, 1]]),
                openings=['l', 'r', 'b']),
                'open':
                dict(
                tile=np.array([
                [0, 0, 0, 2, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0],
                [2, 2, 2, 2, 2, 2, 2],
                [0, 0, 0, 2, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0]]),  
                openings=['tl', 't', 'tr', 'r', 'br', 'b', 'bl', 'l']) 
            },
        }

        self.tile_locations = [
            (1, 1), 
            (1, 8),
            (1, 15),
            (8, 1),
            (8, 8),
            (8, 15),
            (15, 1),
            (15, 8),
            (15, 15)
        ]

        self.rotation_map = {
            'tl':'tr',
            't':'r',
            'tr':'br',
            'r':'b',
            'br':'bl',
            'b':'l',
            'bl':'tl',
            'l':'t'
        }

        self.connection_map = {
            'tl':'tr',
            't':'b',
            'tr':'tl',
            'r':'l',
            'br':'bl',
            'b':'t',
            'bl':'br',
            'l':'r'
        }

    def rotate(self, openings, num_rotations):
        for i in range(num_rotations):
            openings = [self.rotation_map[o] for o in openings]
        return openings

    def get_orientations(self, openings):
        orientations = [openings]
        for i in range(3):
            orientations.append(self.rotate(openings, i+1))
        return orientations

    def generate_tile_pool(self, difficulty):
        return self.tiles[difficulty]

    # def mark(x, y, grid, frontier):
    #     grid[x, y] = 1
    #     if (grid[x-1, y] == 0) and (x-1 > 0):
    #         if (x-1, y) not in frontier:
    #             frontier.append((x-1, y))
    #     if (grid[x+1, y] == 0) and (x+1 < grid.shape[1]-1):
    #         if (x+1, y) not in frontier:
    #             frontier.append((x+1, y))
    #     if (grid[x, y-1] == 0) and (y-1 > 0):
    #         if (x, y-1) not in frontier:
    #             frontier.append((x, y-1))
    #     if (grid[x, y+1] == 0) and (y+1 < grid.shape[0]-1):
    #         if (x, y+1) not in frontier:
    #             frontier.append((x, y+1))
    #     return grid, frontier

    # def neighbors(x, y, grid):
    #     n = []

    #     if (x > 0) and (grid[x-1, y] == 1):
    #         n.append((x-1, y))
    #     if (x < grid.shape[0]-1) and (grid[x+1, y] == 1):
    #         n.append((x+1, y))
    #     if (y > 0) and (grid[x, y-1] == 1):
    #         n.append((x, y-1))
    #     if (y < grid.shape[1]-1) and (grid[x, y+1] == 1):
    #         n.append((x, y+1))

    #     return n      

    def check_validity(self, pos, tile_list):
        constraints = []
        connections = []
        # print('Pos', pos)
        # print('Tile list', tile_list)
        if pos < 3:
            constraints.append('t')
            if pos > 0:
                if not any('r' in o for o in tile_list[-1][1]):
                    constraints.append('l')
                connections = [o for o in tile_list[-1][1] if 'r' in o]
        elif pos > 5:
            # constraints.append('b')
            if not any('b' in o for o in tile_list[-3][1]):
                constraints.append('t')
            connections += [o for o in tile_list[-3][1] if 'b' in o]
            if pos != 6:
                if not any('r' in o for o in tile_list[-1][1]):
                    constraints.append('l')
                connections += [o for o in tile_list[-1][1] if 'r' in o]
        else:
            if not any('b' in o for o in tile_list[-3][1]):
                constraints.append('t')
            connections += [o for o in tile_list[-3][1] if 'b' in o]
            if pos != 3:
                if not any('r' in o for o in tile_list[-1][1]):
                    constraints.append('l')
                connections += [o for o in tile_list[-1][1] if 'r' in o]
        
        if pos % 3 == 0:
            constraints.append('l')
        elif (pos-2) % 3 == 0:
            constraints.append('r')
        # print(connections)
        # print(constraints)
        return constraints, connections

    def generate_maze(self, difficulty):
        # random.seed(42)
        if difficulty == 'hard':
            diff_list = ['hard', 'medium', 'easy']
        elif difficulty == 'medium':
            diff_list = ['medium', 'easy']
        else:
            diff_list = ['easy']

        tiles = {}
        for d in diff_list:
            tiles.update(self.generate_tile_pool(d))

        selected = []
        for i, loc in enumerate(self.tile_locations):
            # print('Tile', i)
            valid_connection = False
            while not valid_connection:
                tile_name = list(tiles.keys())[random.randint(0, len(tiles)-1)]
                # print(tile_name)
                tile = tiles[tile_name]['tile']
                openings = tiles[tile_name]['openings']
                if len(selected) > 0:
                    # print('SELECTED:', selected)
                    constraints, connections = self.check_validity(i, selected)
                    if len(connections) == 0:
                        tile = tiles['filled']['tile']
                        selected.append((tile, tiles['filled']['openings']))
                        # print('Conenction 0 Append')
                        valid_connection = True
                    else:
                        if tile_name == 'filled':
                            # print('Skipped filled.')
                            continue
                        orientations = self.get_orientations(openings)
                        orientations = list(zip(range(len(orientations)), orientations))
                        # print(orientations)
                        while len(orientations) > 0:
                            orientation = orientations.pop(random.randint(0, len(orientations)-1))
                            # print('Orientation', orientation)
                            if not any(e in constraints for e in orientation[1]) \
                                and any(self.connection_map[e] in connections for e in orientation[1]):

                                tile = np.rot90(tile, orientation[0], (1, 0))
                                openings = self.rotate(openings, orientation[0])
                                selected.append((tile, openings))
                                # print('Normal append.')
                                valid_connection = True
                                break
                            
                else:
                    if tile_name == 'filled':
                        continue
                    selected.append((tile, openings))
                    # print('First append.')
                    valid_connection = True
                y2 = loc[0] + tile.shape[0]
                x2 = loc[1] + tile.shape[1]
                self.grid[loc[0]:y2, loc[1]:x2] = tile
        # print(self.grid)
        return self.grid
        

    def print_maze(grid):
        for i in range(grid.shape[0]):
            for each in grid[i]:
                if each == 1:
                    print('0', end='')
                else:
                    print('1', end='')
            print('')

    # print(generate_maze('easy'))

def main():
    mg = MazeGeneration()
    print(mg.generate_maze('hard'))

if __name__ == "__main__":
    main()