import numpy as np
import pdb
from tests.data import wallgrid as grid

grid = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # Row 0
        [0, 1, 1, 0, 0, 0, 0, 1, 0, 0],  # Row 1
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # Row 2
        [0, 1, 1, 0, 7, 0, 0, 0, 0, 0],  # Row 3
        [0, 1, 1, 7, 0, 9, 0, 0, 0, 0],  # Row 4
        [0, 1, 1, 0, 9, 0, 0, 0, 0, 0],  # Row 5
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # Row 6
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # Row 7
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # Row 8
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
)  # Row 9
# Columns 0  1  2  3  4  5  6  7  8  9
moves = {
    "u": np.array([-1, 0]),
    "d": np.array([1, 0]),
    "r": np.array([0, 1]),
    "l": np.array([0, -1]),
}
# explored = [np.array([0, 0])]


def isin_explored(position, explored):
    flag = False
    for e in explored:
        if np.array_equal(position, e):
            return True
    return flag


def get_valid_moves(moves, position, grid, explored):
    """
    This function takes a dictionary of moves, position, explored positions and returns valid moves

    Parameters
    ----------
    moves : dict
    Dictionary of `moves` with keys u, d, l, r with a numpy array mapped to it.
    y
    Description of parameter `y` (with type not specified)
    """
    ROW_IDX = 0
    COL_IDX = 1
    WALL = 1
    pos = None
    valid_moves = []
    for _, move in moves.items():
        pos = move + position
        # checking row and column bounds and walls, adding valid moves only
        if (
            pos[ROW_IDX] >= 0
            and pos[ROW_IDX] <= 9
            and pos[COL_IDX] >= 0
            and pos[COL_IDX] <= 9
            and grid[pos[ROW_IDX], pos[COL_IDX]] != WALL
            and not isin_explored(pos, explored)
        ):
            valid_moves.append(move)

    return np.array(valid_moves)


def get_distance(position):
    """ returns a distance from position [0, 0]"""
    return position[0] + position[1]


def get_distance_all_valid_moves(valid_moves, position):
    """This function return a dictionary of possible moves
        at a position with their corresponding distance as keys
    """
    temPos = None
    ds = {}
    for move in valid_moves:
        temPos = position + move
        key = get_distance(temPos)
        if key not in ds:
            ds[key] = []
            ds.get(key).append(temPos)
        else:
            ds.get(key).append(temPos)

    return ds


def update_not_explored(main_not_explored, not_explored):
    pass


def move(position, explored, main_not_explored, goal_found, grid):
    # pdb.set_trace()
    v_moves = get_valid_moves(moves, position, grid, explored)
    not_explored = get_distance_all_valid_moves(v_moves, position)


class Bfs:

    def __init__(self, position, explored, goal_found, grid, goal):
        self._position = position
        self._explored = explored
        self._not_explored = dict()
        self._goal_found = goal_found
        self._goal = goal
        self._grid = grid
        self._moves = {
            "u": np.array([-1, 0]),
            "d": np.array([1, 0]),
            "r": np.array([0, 1]),
            "l": np.array([0, -1]),
        }
        # self._valid_moves = []

    def move(self):
        """returns None if all positions are explored and goal is not found"""
        valid_moves = self._get_valid_moves()
        found = self._check_goal(valid_moves)

        if found is not None:
            self._position = found
            return found

        self.set_distance_all_valid_moves(valid_moves)

        min_distance = self._get_min_distance_key()
        if min_distance is None:
            return None
        movs = self._pick_moves_at(min_distance)
        picked_move = self._pick_a_move_from(movs, min_distance)
        self._position = picked_move

    def _pick_a_move_from(self, valid_moves, distance):
        """returns a valid move, also updates not_explored and explored"""
        picked_move = None
        if len(valid_moves) == 1:
            picked_move = self._not_explored.pop(distance).pop()
            self._explored.append(picked_move)
        else:
            picked_move = self._not_explored[distance].pop()
            self._explored.append(picked_move)

        return picked_move

    def _pick_moves_at(self, min_distance):
        """returns a list of move at distance provided"""
        if min_distance not in self._not_explored:
            raise KeyError("key:{min_distance} not in " + self._not_explored)
        return self._not_explored[min_distance]

    def _get_min_distance_key(self):
        """returns None if there are no elments left in not_explored otherwise returns the next key"""
        min_distance = None
        try:
            # pdb.set_trace()
            min_distance = next(iter(sorted(self._not_explored)))
        except StopIteration:
            min_distance = None

        return min_distance

    def _check_goal(self, valid_moves):
        """return the position of the goal if goal found, also sets the goal_found to be True"""
        if self._grid[self._position[0], self._position[1]] == self._goal:
            self._goal_found = True
            return self._position

        temPos = None
        for move in valid_moves:
            temPos = self._position + move

            if self._grid[temPos[0], temPos[1]] == self._goal:
                self._goal_found = True
                return temPos
        return None

    def _get_valid_moves(self):
        """
        This function takes a dictionary of moves, position, explored positions and returns valid moves

        Parameters
        ----------
        moves : dict
        Dictionary of `moves` with keys u, d, l, r with a numpy 2D array mapped [-1, 0], [1, 0], [0, -1], [0, 1].
        y
        Description of parameter `y` (with type not specified)
        """
        ROW_IDX = 0
        COL_IDX = 1
        WALL = 1
        pos = None
        # moves = {
        #     "u": np.array([-1, 0]),
        #     "d": np.array([1, 0]),
        #     "r": np.array([0, 1]),
        #     "l": np.array([0, -1]),
        # }
        valid_moves = []
        for _, move in self._moves.items():
            pos_idx = move + self._position
            # checking row and column bounds and walls, adding valid moves only
            if (
                pos_idx[ROW_IDX] >= 0
                and pos_idx[ROW_IDX] <= 9
                and pos_idx[COL_IDX] >= 0
                and pos_idx[COL_IDX] <= 9
                and grid[pos_idx[ROW_IDX], pos_idx[COL_IDX]] != WALL
                and not self._isin_explored(pos_idx, self._explored)
            ):
                valid_moves.append(move)
        return valid_moves

    def set_distance_all_valid_moves(self, valid_moves_idx):
        """This function return a dictionary of possible moves
            at a position with their corresponding distance as keys

            Parameters
            ----------
            valid_moves_idx : [np.array([])]

        """
        temPos = None
        # ds = {}
        for move in valid_moves_idx:
            temPos = self._position + move
            key = self._get_distance(temPos)
            # pdb.set_trace()
            if key not in self._not_explored:
                self._not_explored[key] = []
                self._not_explored.get(key).append(temPos)
            elif not self._isin_explored(temPos, self._not_explored.get(key)):
                self._not_explored.get(key).append(temPos)

    def _get_distance(self, temPos):
        """ returns a distance from position [0, 0]"""
        return temPos[0] + temPos[1]

    def _isin_explored(self, position, explored):
        flag = False
        for e in explored:
            if np.array_equal(position, e):
                return True
        return flag
