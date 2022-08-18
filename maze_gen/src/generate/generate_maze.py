import numpy as np
import random
import time

class MazeGeneration:
    """Generates maze from preset tiles and creates solution path.

    Tiles are selected at random based on contraints that force
    maze to be solvable. Difficulty can be adjusted to include tiles
    with varying attributes.
    """

    def __init__(self):
        """Creates new maze generation object.

        Args:
            grid (ndarray): 2D array containing maze tiles, initialized to zeros
            tiles (dict): Dictionary containing preset maze tiles and attributes (opening tags)
            tile_locations (list):  List specifying starting location for each tile
            rotation_map (dict): Mapping of tile openings before and after ninety-degree rotation
            connection_map (dict): Mapping of opening tags to tags they are able to connect with (top and side)
        """

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
        """Generates new set of opening tags after n rotations.

        Args:
            openings (list of str): Original opening tags
            num_rotations (int): Number of ninety-degree rotations to apply

        Returns:
            openings (list): New list of opening tags after specified number of rotations
        """

        for i in range(num_rotations):
            openings = [self.rotation_map[o] for o in openings]
        return openings

    def get_orientations(self, openings):
        """Generates list of openings possible in every orientation.

        Args:
            openings (list of str): Initial list of openings in default orientation

        Returns:
            tiles (list of list): Lists of openings at every possible tile orientation
        """

        orientations = [openings]
        for i in range(3):
            orientations.append(self.rotate(openings, i+1))
        return orientations

    def generate_tile_pool(self, difficulty):
        """Generates pool of tiles to draw from based on difficulty.

        Args:
            difficulty (int): Difficulty where 0 is easy, 1 is medium, and 2 is hard

        Returns:
            dict: Dictionary containing tiles corresponding to difficulty input
        """

        return self.tiles[difficulty]

    def check_validity(self, pos, tile_list, difficulty):
        """Checks for constraints and connections at specified tile position.

        Args:
            pos (int): Position in maze grid being checked
            tile_list (list): List of tiles that have been selected so far at previous positions
            difficulty (int): Difficulty where 0 is easy, 1 is medium, and 2 is hard

        Returns:
            constraints (list): List of tags that correspond to no opening in adjacent tiles
            connections (dict): Dictionary containing possible connections with adjacent tiles
        """

        constraints = []
        connections = dict(side=[], top=[])

        if pos < 3:
            if difficulty == 0:
                constraints.extend(['t', 'tr', 'tl'])
            if pos > 0:
                if not any('r' in o for o in tile_list[-1][1]):
                    constraints.extend(['l', 'bl', 'tl'])
                connections['side'] = [o for o in tile_list[-1][1] if 'r' in o]
                connections['top'] = []
        elif pos > 5:
            if not any('b' in o for o in tile_list[-3][1]):
                constraints.extend(['t', 'tr', 'tl'])
            connections['top'] = [o for o in tile_list[-3][1] if 'b' in o]
            if pos != 6:
                if not any('r' in o for o in tile_list[-1][1]):
                    constraints.extend(['l', 'bl', 'tl'])
                connections['side'] = [o for o in tile_list[-1][1] if 'r' in o]
            else:
                connections['side'] = []
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
        
        if pos % 3 == 0:
            constraints.extend(['l'])
        elif (pos-2) % 3 == 0:
            constraints.extend(['r'])
            if ['br'] == connections['side']:
                connections['side'] = []

        return constraints, connections

    def generate_maze(self, difficulty):
        """Generates solvable maze of specified difficulty.

        Args:
            difficulty (int): Difficulty where 0 is easy, 1 is medium, and 2 is hard

        Returns:
            grid (ndarray): 2D array containing selected maze tiles
        """

        # Use 71 for testing (longer maze with all features on easy)
        # random.seed(71)
        if difficulty == 2:
            diff_list = ['hard', 'medium', 'easy']
        elif difficulty == 1:
            diff_list = ['medium', 'easy']
        elif difficulty == 0:
            diff_list = ['easy']
        else:
            print('Invalid difficulty. Generating easy maze...')
            diff_list = ['easy']

        possible_connections = list(range(9))

        tiles = {}
        for d in diff_list:
            tiles.update(self.generate_tile_pool(d))

        selected = []
        for i, loc in enumerate(self.tile_locations):
            valid_connection = False
            exhausted = False
            tile_keys = list(tiles.keys())
            while not valid_connection:
                if len(tile_keys) == 0:
                    exhausted = True
                    tile_name = 'filled'
                else:
                    tile_name = tile_keys.pop(random.randint(0, len(tile_keys)-1))
                tile = tiles[tile_name]['tile']
                openings = tiles[tile_name]['openings']
                if len(selected) > 0:
                    constraints, connections = self.check_validity(i, selected, difficulty)
                    time.sleep(1)
                    if (len(connections['side']) + len(connections['top'])) == 0 or exhausted:
                        tile = tiles['filled']['tile']
                        selected.append((tile, tiles['filled']['openings'], 'filled'))
                        possible_connections.remove(i)
                        valid_connection = True
                    else:
                        # if tile_name == 'filled':
                        #     print('Skipped filled.')
                        #     continue
                        orientations = self.get_orientations(openings)
                        orientations = list(zip(range(len(orientations)), orientations))
                        while len(orientations) > 0:
                            orientation = orientations.pop(random.randint(0, len(orientations)-1))

                            side_connections = [[self.connection_map[o]['side']] 
                                                        for o in orientation[1]]

                            top_connections = [[self.connection_map[o]['top']] 
                                                        for o in orientation[1]]

                            if not any(o in constraints for o in orientation[1]) and \
                                    (any(set(c).intersection(set(connections['side'])) for c in side_connections) or \
                                     any(set(c).intersection(set(connections['top'])) for c in top_connections)):
                                    
                                tile = np.rot90(tile, orientation[0], (1, 0))
                                openings = self.rotate(openings, orientation[0])
                                
                                selected.append((tile, openings, tile_name))
                                valid_connection = True
                                break
                            
                else:
                    if tile_name == 'filled':
                        continue
                    selected.append((tile, openings, tile_name))
                    valid_connection = True

        if difficulty != 0:
            print(f'CHECKING DIFFICULTY ({difficulty})')
            for tile in selected:
                remake = False
                if difficulty == 1:
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

        return self.grid

    def check_neighbors(self, y, x, maze):
        """Checks neighbor cell to determine whether it is part of path.

        Args:
            y (int): y-position in maze
            x (int): x-position in maze
            maze (ndarray): 2D array containing selected maze tiles

        Returns:
            str: Direction of next cell in path
            tuple: (y, x) movement needed to move to next cell in path
        """
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
        """Returns appropriate angular velocity for turn type (sharp, gradual).

        Args:
            dir (str): Current direction of movement through maze
            next_dir (str): Direction of movement to next cell along path

        Returns:
            float: The angular velocity appropriate for the turn
        """

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
        """Generates linear and angular velocity commands to navigate through maze.

        Args:
            maze (ndarray): 2D array containing selected maze tiles
            init_position (tuple): Starting position (cell) in maze

        Returns:
            commands (tuple): Set of velocity commands (angular, linear) to navigate maze successfully
        """

        commands = []   # (angular, linear)
        loc = (4, 4)    # location initialized to starting cell
        dir = 'E'       # direction initialized to starting direction

        while True:
            if maze[loc[0]][loc[1]] == 5:
                break

            next_dir, movement = self.check_neighbors(loc[0], loc[1], maze)

            if next_dir == dir:
                commands.append((0, 5/46*2, movement))
            else:
                commands.append((self.get_angular(dir, next_dir)/6, 0, movement))
                commands.append((0, 5/46*2, movement))

            loc = (loc[0]+movement[0], loc[1]+movement[1])
            dir = next_dir

        return commands

    def generate_waypoint(self, current_position, movement):
        """Generates a waypoint from current position and a desired movement.

        Args:
            current_position (tuple): Current position (cell) in maze
            movement (tuple): (y, x) movement to get to desired cell

        Returns:
            waypoint (tuple): Desired (y, x) position based on prev. position and movement
        """
        waypoint = (current_position[0]+(movement[1]*(5/23)), 
                    current_position[1]+(movement[0]*(5/23)))
        return waypoint

    def generate_path(self, selected_tiles):
        """Generates single path through maze using list of selected tiles.

        Args:
            selected_tiles (list): List of chosen tiles that comprise maze

        Returns:
            path (list): Tiles to be included in path (numbered from top L (0) to bottom R (8))
        """

        links = {}
        for i, tile in enumerate(selected_tiles):
            neighbors = [i-1, i+1, i-3, i+3]
            neighbors = [n for n in neighbors if n >= 0 and n < 9]

            connections = []
            for neighbor in neighbors:
                neighbor_tile = selected_tiles[neighbor]
                for conn in neighbor_tile[1]:
                    if any(l in conn for l in ['l', 'r']) and self.connection_map[conn]['side'] in tile[1]:
                        if neighbor not in connections:
                            connections.append(neighbor)
                    if 'b' in conn and self.connection_map[conn]['top'] in tile[1]:
                        if neighbor not in connections:
                            connections.append(neighbor)
            links[i] = connections

        path = []
        path = self.find_link(path, selected_tiles, links, 0)

        return path

    def find_link(self, path, selected_tiles, links, link):
        """Generates path of connected tiles using list of selected tiles.

        Links between tiles are chosen at random.
        TODO: Select longest path through maze.

        Args:
            path (list): Tiles to be included in path (numbered from top L (0) to bottom R (8))
            selected_tiles (list): List of chosen tiles that comprise maze 
            links (dict): Mapping of tile ID/number to other connected tiles
            link (int): ID of current tile to be checked for links

        Returns:
            path (list): Tiles to be included in path (numbered from top L (0) to bottom R (8))
        """

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
            if link == 8:
                return path
            else:
                self.find_link(path, selected_tiles, links, link+1)
        return path

    def print_maze(self):
        """Print current maze in readable format."""
        
        for i in range(self.grid.shape[0]):
            for cell in self.grid[i]:
                if cell == 1:
                    print('0 ', end='')
                else:
                    print('1 ', end='')
            print('')

def main():
    mg = MazeGeneration()
    difficulty = int(input('Enter maze difficulty: '))
    mg.generate_maze(difficulty)
    mg.print_maze()

if __name__ == "__main__":
    main()