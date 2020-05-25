import numpy as np
import pdb

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
    return position[0] + position[1]


def get_distance_all_valid_moves(valid_moves, position):
    """This function return a dictionary of possible moves
        with their corresponding distance as keys
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
