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


def get_valid_moves(moves, position, grid):
    """
    This function takes a dictionary of moves and return only valid moves
    """
    pos = None
    valid_moves = []
    for _, move in moves.items():
        pos = move + position
        # checking row and column bounds and walls, adding valid moves only
        if (
            pos[0] >= 0
            and pos[0] <= 9
            and pos[1] >= 0
            and pos[1] <= 9
            and grid[pos[0], pos[1]] != 1
        ):
            valid_moves.append(move)

    return np.array(valid_moves)


def get_distance(position):
    return position[0] + position[1]


def get_distance_all_valid_moves(valid_moves, position):
    """This function return a dictionary of possible moves
        with their distances as keys
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
