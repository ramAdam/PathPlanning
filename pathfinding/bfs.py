import copy
import numpy as np
import pdb
import abc
from tests.data import wallgrid as grid
from collections.abc import MutableMapping


class BfsPathDictionary(MutableMapping):
    """a dictionary designed for path finding"""
    __marker = object()
    def __init__(self, *args, **kwargs):

        self._not_explored = dict()
        self._explored = set()
        self.update(dict(*args, **kwargs))

    def __setitem__(self, key, value):
        if not isinstance(value, (np.ndarray,)):
            raise ValueError("value is not instance of numpy array")

        if key not in self._not_explored:
            self._not_explored[key] = set()
            self._not_explored.get(key).add(tuple(value))
        else:
            self._not_explored.get(key).add(tuple(value))

    def __getitem__(self, key):
        return self._not_explored[key]

    def __delitem__(self, key):
        del self._not_explored[key]

    def __iter__(self):
        return iter(self._not_explored)

    def __len__(self):
        return len(self._not_explored)

    def __repr__(self):
        return f"{type(self).__name__}({self._not_explored})"

    def pop(self, key, default=__marker):
        try:
            value = self[key]
            idx = None
            if len(value) == 1:
                del self[key]
                idx = value.pop()
                self._explored.add(idx)
                return idx
            else:
                idx = value.pop()
                self._explored.add(idx)
                return idx
        except KeyError:
            if default is self.__marker:
                raise
            return default

    def keys(self):
        """returns keys in ascending order"""
        return sorted(self._not_explored.keys())


class PathFindingAlgorithm(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return(hasattr(subclass, get_valid_moves) and callable(subclass.get_valid_moves))

    @abc.abstractmethod
    def get_valid_moves(self, position, explored=None):
        raise NotImplementedError


class BfsValidMoves(PathFindingAlgorithm):
    """Valid moves for breath first search"""

    def __init__(self, grid_shape):
        self._grid_shape = grid_shape
        self._moves = [
            np.array([-1, 0]),
            np.array([1, 0]),
            np.array([0, 1]),
            np.array([0, -1]),
        ]
        self._valid_moves = []

    def get_valid_moves(self, position, explored) -> list:
        """
        This function takes position, set of explored positions and returns valid moves

        Parameters
        ----------
        position : np.array
        Dictionary of `moves` with keys u, d, l, r with a numpy 2D array mapped [-1, 0], [1, 0], [0, -1], [0, 1].
        y
        Description of parameter `y` (with type not specified)
        """
        ROW_IDX = 0
        COL_IDX = 1
        WALL = 1
        # grid row end index
        ROW_END_IDX = self._grid_shape[0] - 1
        # grid col end index
        COL_END_IDX = self._grid_shape[1] - 1

        self._valid_moves.clear()
        for move in self._moves:
            pos_idx = move + position
            # checking row and column bounds and walls, adding valid moves only

            if (
                pos_idx[ROW_IDX] >= 0
                and pos_idx[ROW_IDX] <= ROW_END_IDX
                and pos_idx[COL_IDX] >= 0
                and pos_idx[COL_IDX] <= COL_END_IDX
                and grid[pos_idx[ROW_IDX], pos_idx[COL_IDX]] != WALL
                and tuple(pos_idx) not in explored
            ):
                self._valid_moves.append(move)
        return copy.copy(self._valid_moves)


class Bfs:

    def __init__(self, position, grid, goal):
        self._position = position
        self._path = BfsPathDictionary()
        self._path._explored.add(tuple(self._position))
        self._goal_found = False
        self._goal = goal
        self._grid = grid
        self._bfs_moves = BfsValidMoves(self._grid.shape)

    def move(self):
        """changes the position to next valid position until the goal is found or search is exhausted"""
        valid_moves = self._get_valid_moves()

        found = self._check_goal(valid_moves)

        if found is not None:
            self._goal_found = True
            self._position = found
            return

        self.set_distance_all_valid_moves(valid_moves)

        min_distance = self._get_min_distance_key()
        if min_distance is not None:
            movs = self._pick_moves_at(min_distance)
            picked_move = self._pick_a_move_from(movs, min_distance)
            self._position = picked_move

    def _pick_a_move_from(self, valid_moves, distance):
        """returns a valid move, also updates not_explored and explored"""
        picked_move = None
        picked_move = self._path.pop(distance)

        return picked_move

    def _pick_moves_at(self, min_distance):
        """returns a list of move at a given distance"""
        return self._path[min_distance]

    def _get_min_distance_key(self):
        """ returns None if there are no elments left in not_explored otherwise returns the next
            minimum key
        """
        return next(iter(self._path.keys()), None)

    def _check_goal(self, valid_moves):
        """return the position of the goal if goal found, also sets the goal_found to be True"""

        temPos = None
        if self._grid[self._position[0], self._position[1]] == self._goal:
            self._goal_found = True
            temPos = self._position
            return temPos

        for move in valid_moves:
            temPos = self._position + move

            if self._grid[temPos[0], temPos[1]] == self._goal:

                return temPos
        return None

    def _get_valid_moves(self):
        valid_moves = self._bfs_moves.get_valid_moves(
            self._position, self._path._explored)
        return valid_moves

    def set_distance_all_valid_moves(self, valid_moves_idx):
        """This function return a dictionary of possible moves
            at a position with their corresponding distance as keys

            Parameters
            ----------
            valid_moves_idx : [np.array([])]

        """
        temPos = None
        for move in valid_moves_idx:
            temPos = self._position + move
            key = self._get_distance(temPos)

            self._path[key] = temPos

    def _get_distance(self, temPos):
        """ returns a distance from position [0, 0]"""
        return temPos[0] + temPos[1]


class GoalSearch:
    def __init__(self, searchAlgo: Bfs):
        self._searchAlgo = searchAlgo
        self._end_bounds = self._get_grid_bounds(self._searchAlgo._grid.shape)
        self._position = None

    def find(self) -> bool:
        """returns True if the goal is found, false otherwise"""
        flag = True
        while flag:
            self._searchAlgo.move()
            #
            if tuple(self._searchAlgo._position) == self._end_bounds and not self._searchAlgo._goal_found:
                self._position = tuple(self._searchAlgo._position)
                return False
            elif self._searchAlgo._goal_found:
                self._position = tuple(self._searchAlgo._position)
                return True

    def _get_grid_bounds(self, shape: tuple) -> tuple:
        bounds = list()
        for bound in shape:
            bounds.append(bound - 1)
        return tuple(bounds)
