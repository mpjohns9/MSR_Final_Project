from lib2to3.pytree import generate_matches
import numpy as np
import random
import time

from pyrfc3339 import generate

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
            'tl':dict(top='bl', side='tr'),
            't':dict(top='b', side='N/A'),
            'tr':dict(top='br', side='tl'),
            'r':dict(top='N/A', side='l'),
            'br':dict(top='tr', side='bl'),
            'b':dict(top='t', side='N/A'),
            'bl':dict(top='tl', side='br'),
            'l':dict(top='N/A', side='r')
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

    def check_validity(self, pos, tile_list, difficulty, possible_connections):
        constraints = []
        connections = dict(side=[], top=[])

        # print('Pos', pos)
        # print('Tile list', tile_list)
        if pos < 3:
            if difficulty == 0:
                constraints.extend(['t', 'tr', 'tl'])
            if pos > 0:
                if not any('r' in o for o in tile_list[-1][1]):
                    constraints.extend(['l', 'bl', 'tl'])
                connections['side'] = [o for o in tile_list[-1][1] if 'r' in o]
                connections['top'] = []
                print('CONNECTIONS:', connections)
        elif pos > 5:
            # if (pos - 3) not in possible_connections:
            #     return constraints, connections
            # constraints.append('b')
            if not any('b' in o for o in tile_list[-3][1]):
                constraints.extend(['t', 'tr', 'tl'])
            connections['top'] = [o for o in tile_list[-3][1] if 'b' in o]
            if pos != 6:
                if not any('r' in o for o in tile_list[-1][1]):
                    constraints.extend(['l', 'bl', 'tl'])
                connections['side'] = [o for o in tile_list[-1][1] if 'r' in o]
            else:
                connections['side'] = []
            print('CONNECTIONS:', connections)
        else:
            if not any('b' in o for o in tile_list[-3][1]):
                constraints.extend(['t', 'tr', 'tl'])
            connections['top'] = [o for o in tile_list[-3][1] if 'b' in o]
            if pos != 3:
                if not any('r' in o for o in tile_list[-1][1]):
                    constraints.extend(['l', 'bl', 'tl'])
                connections['side'] = [o for o in tile_list[-1][1] if 'r' in o]
            else:
                connections['side'] = []
            print('CONNECTIONS:', connections)
        
        if pos % 3 == 0:
            constraints.extend(['l'])
        elif (pos-2) % 3 == 0:
            constraints.extend(['r'])
            if ['br'] == connections['side']:
                connections['side'] = []
        print('FINAL CONNECTIONS:', connections)
        # print(connections)
        # print(constraints)
        return constraints, connections

    def generate_maze(self, difficulty):
        # random.seed(23)
        if difficulty == 2:
            diff_list = ['hard', 'medium', 'easy']
        elif difficulty == 1:
            diff_list = ['medium', 'easy']
        else:
            diff_list = ['easy']

        path = []
        possible_connections = list(range(9))

        tiles = {}
        for d in diff_list:
            tiles.update(self.generate_tile_pool(d))

        selected = []
        for i, loc in enumerate(self.tile_locations):
            print('Tile', i)
            valid_connection = False
            exhausted = False
            tile_keys = list(tiles.keys())
            while not valid_connection:
                if len(tile_keys) == 0:
                    exhausted = True
                    tile_name = 'filled'
                else:
                    tile_name = tile_keys.pop(random.randint(0, len(tile_keys)-1))
                print(tile_name)
                tile = tiles[tile_name]['tile']
                openings = tiles[tile_name]['openings']
                if len(selected) > 0:
                    print('SELECTED:', selected)
                    constraints, connections = self.check_validity(i, selected, difficulty, 
                                                                    possible_connections)
                    print('Constraints:', constraints)
                    print('Connections:', connections)
                    time.sleep(1)
                    if (len(connections['side']) + len(connections['top'])) == 0 or exhausted:
                        tile = tiles['filled']['tile']
                        selected.append((tile, tiles['filled']['openings'], 'filled'))
                        print('Conenction 0 Append')
                        possible_connections.remove(i)
                        valid_connection = True
                    else:
                        if tile_name == 'filled':
                            print('Skipped filled.')
                            continue
                        orientations = self.get_orientations(openings)
                        orientations = list(zip(range(len(orientations)), orientations))
                        print('Possible orientations:', orientations)
                        while len(orientations) > 0:
                            orientation = orientations.pop(random.randint(0, len(orientations)-1))
                            print('Orientation', orientation)

                            side_connections = [[self.connection_map[o]['side']] 
                                                        for o in orientation[1]]

                            top_connections = [[self.connection_map[o]['top']] 
                                                        for o in orientation[1]]

                            print('Side connections:', side_connections)
                            print('Top connections:', top_connections)
                            print(not any(o in constraints for o in orientation[1]))
                            print(any(set(c).intersection(set(connections['side'])) for c in side_connections))
                            print(any(set(c).intersection(set(connections['top'])) for c in top_connections))

                            if not any(o in constraints for o in orientation[1]) and \
                                    (any(set(c).intersection(set(connections['side'])) for c in side_connections) or \
                                     any(set(c).intersection(set(connections['top'])) for c in top_connections)):
                                    
                                tile = np.rot90(tile, orientation[0], (1, 0))
                                openings = self.rotate(openings, orientation[0])

                                if self.check_path(i, possible_connections):
                                    path.append(i)
                                # else:
                                #     tile = np.vectorize(lambda x: 0 if x == 2 else x)(tile)
                                selected.append((tile, openings, tile_name))
                                print('Normal append.')
                                valid_connection = True
                                break
                            
                else:
                    if tile_name == 'filled':
                        continue
                    selected.append((tile, openings, tile_name))
                    print('First append.')
                    valid_connection = True
                    path.append(i)
                # y2 = loc[0] + tile.shape[0]
                # x2 = loc[1] + tile.shape[1]
                # self.grid[loc[0]:y2, loc[1]:x2] = tile
        print(difficulty == 0)
        if difficulty != 0:
            print(f'CHECKING DIFFICULTY ({difficulty})')
            remake = False
            for tile in selected:
                if difficulty == 1:
                    print(tile[2])
                    if 'angle' in tile[2]:
                        break
                    
                elif difficulty == 2:
                    if tile[2] in ('t', 'open'):
                        break

                remake = True

            if remake:
                print('DIFFICULTY REQUIREMENTS NOT MET. REGENERATING MAZE.')
                self.grid = self.generate_maze(difficulty)

        path = self.generate_path(selected)
        for i, loc in enumerate(self.tile_locations):
            y2 = loc[0] + 7
            x2 = loc[1] + 7
            if i in path:
                tile = selected[i][0]
            else:
                tile = np.vectorize(lambda x: 0 if x == 2 else x)(selected[i][0])
            
            self.grid[loc[0]:y2, loc[1]:x2] = tile

        # print(self.generate_path(selected))
        return self.grid

    def check_neighbors(self, y, x, maze):
        if maze[y][x+1] in (2, 5):
            return 'E', (0, 1)
        elif maze[y+1][x+1] in (2, 5):
            return 'SE', (1, 1)
        elif maze[y+1][x] in (2, 5):
            return 'S', (1, 0)
        elif maze[y+1][x-1] in (2, 5):
            return 'SW', (1, -1)
        elif maze[y][x-1] in (2, 5):
            return 'W', (0, -1)
        elif maze[y-1][x-1] in (2, 5):
            return 'NW', (-1, -1)
        elif maze[y-1][x] in (2, 5):
            return 'N', (-1, 0)
        elif maze[y-1][x+1] in (2, 5):
            return 'NE', (-1, 1)

    def get_angular(self, dir, next_dir):
        if dir == 'S':
            if next_dir == 'E':
                return -np.pi/2
            elif next_dir == 'W':
                return np.pi/2
            elif next_dir == 'SE':
                return -np.pi/4
            elif next_dir == 'SW':
                return np.pi/4

        if dir == 'SE':
            if next_dir == 'NE':
                return -np.pi/2
            elif next_dir == 'SW':
                return np.pi/2
            elif next_dir == 'E':
                return -np.pi/4
            elif next_dir == 'S':
                return np.pi/4

        if dir == 'E':
            if next_dir == 'N':
                return -np.pi/2
            elif next_dir == 'S':
                return np.pi/2
            elif next_dir == 'NE':
                return -np.pi/4
            elif next_dir == 'SE':
                return np.pi/4

        if dir == 'NE':
            if next_dir == 'NW':
                return -np.pi/2
            elif next_dir == 'SE':
                return np.pi/2
            elif next_dir == 'N':
                return -np.pi/4
            elif next_dir == 'E':
                return np.pi/4

        if dir == 'N':
            if next_dir == 'W':
                return -np.pi/2
            elif next_dir == 'E':
                return np.pi/2
            elif next_dir == 'NW':
                return -np.pi/4
            elif next_dir == 'NE':
                return np.pi/4

        if dir == 'NW':
            if next_dir == 'SW':
                return -np.pi/2
            elif next_dir == 'NE':
                return np.pi/2
            elif next_dir == 'W':
                return -np.pi/4
            elif next_dir == 'N':
                return np.pi/4

        if dir == 'W':
            if next_dir == 'S':
                return -np.pi/2
            elif next_dir == 'N':
                return np.pi/2
            elif next_dir == 'SW':
                return -np.pi/4
            elif next_dir == 'NW':
                return np.pi/4
        
        if dir == 'SW':
            if next_dir == 'SE':
                return -np.pi/2
            elif next_dir == 'NW':
                return np.pi/2
            elif next_dir == 'S':
                return -np.pi/4
            elif next_dir == 'W':
                return np.pi/4

    def solve_maze(self, maze, init_position):
        # (angular, linear)
        commands = []
        loc = (4, 4)
        dir = 'E'
        waypoint = (init_position[0], init_position[1], 0)

        while True:
            # print(maze)
            # print('Current Cell Value:', maze[loc[0]][loc[1]])
            # print('Coordinates:', loc)
            if maze[loc[0]][loc[1]] == 5:
                break

            next_dir, movement = self.check_neighbors(loc[0], loc[1], maze)
            
            # print('Direction:', dir)
            # print('Next Dir:', next_dir)
            # print('Movement:', movement)

            if next_dir == dir:
                commands.append((0, 5/46, movement))
            else:
                commands.append((self.get_angular(dir, next_dir)/6, 0, movement))
                commands.append((0, 5/46, movement))

            loc = (loc[0]+movement[0], loc[1]+movement[1])
            dir = next_dir
            # print(commands)

        return commands

    def generate_waypoint(self, current_position, movement):
        waypoint = (current_position[0]+(movement[1]*(5/23)), 
                    current_position[1]+(movement[0]*(5/23)))
        return waypoint

    def generate_path(self, selected_tiles):
        ## TODO: Top row only looks for connections in same row.
        ## Results in early termination even if continuation below
        ## is possible. Need to keep iterating through tiles beyond
        ## this condition.

        links = {}
        for i, tile in enumerate(selected_tiles):
            print('TILE', i)
            neighbors = [i-1, i+1, i-3, i+3]
            neighbors = [n for n in neighbors if n >= 0 and n < 9]

            connections = []
            for j, neighbor in enumerate(neighbors):
                print('NEIGHBOR', neighbor)
                neighbor_tile = selected_tiles[neighbor]
                print('TILE CONNECTIONS:', tile[1])
                print('NEIGHBOR CONNECTIONS:', neighbor_tile[1])
                for conn in neighbor_tile[1]:
                    if j < 3:
                        if self.connection_map[conn]['side'] in tile[1]:
                            connections.append(neighbor)
                            break
                    else:
                        if self.connection_map[conn]['top'] in tile[1]:
                            connections.append(neighbor)
                            break

            links[i] = connections
        path = []
        path = self.find_link(path, selected_tiles, links, 0)

        return path

    def find_link(self, path, selected_tiles, links, link):
        print('Link', link)
        print('Path:', path)
        print('Options:', links[link])
        path.append(link)
        links[link] = [l for l in links[link] if l not in path]
        if len(links[link]) == 1:
            link = links[link][0]
            if link in path:
                return path
            self.find_link(path, selected_tiles, links, link)
        elif len(links[link]) > 1:
            link = links[link][random.randint(0, len(links[link])-1)]
            if link in path:
                return path
            self.find_link(path, selected_tiles, links, link)
        else:
            return path
        return path



    def check_path(self, i, possible_connections):
        if i < 3:
            possible_connections.remove(i-1)
            return possible_connections
        elif i >= 3 and i < 6:
            if i == 3:
                if 0 in possible_connections:
                    possible_connections.remove(0)
                    return possible_connections
                else:
                    possible_connections.remove(i)
                    return False
            else:
                if (i - 1) in possible_connections:
                    possible_connections.remove(i-1)
                    return possible_connections
                elif (i - 3) in possible_connections:
                    possible_connections.remove(i-3)
                    return possible_connections
                else:
                    possible_connections.remove(i)
                    return False
        else:
            if i == 6:
                if 3 in possible_connections:
                    possible_connections.remove(3)
                    return possible_connections
                else:
                    possible_connections.remove(i)
                    return False
            else:
                if (i - 1) in possible_connections:
                    possible_connections.remove(i-1)
                    return possible_connections
                elif (i - 3) in possible_connections:
                    possible_connections.remove(i-3)
                    return possible_connections
                else:
                    possible_connections.remove(i)
                    return False


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
    print(mg.generate_maze('easy'))

if __name__ == "__main__":
    main()