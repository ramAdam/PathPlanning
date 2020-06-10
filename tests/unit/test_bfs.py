import unittest
import numpy as np
from pathfinding import *
import pdb
from tests.data import grid, wallgrid
from random import randint


class TestBfs(unittest.TestCase):
    def setUp(self):
        self.position = np.array([0, 0])
        self.goal = 99
        self.bfs = Bfs(self.position, wallgrid, self.goal)

    def test_min_distance_dictionary(self):
        self.bfs.move()
        assert len(self.bfs._not_explored) == 1

        self.assertEqual(self.bfs._get_min_distance_key(), 1)

    def test_min_distance_empty_error(self):
        """min distance should return zero if the not_explored dictionary is empty"""
        assert len(self.bfs._not_explored) == 0
        self.assertEqual(self.bfs._get_min_distance_key(), None)

    def test_pick_moves_at_a_given_distance(self):
        """pick min moves should return 2 valid moves at a distance 1"""
        self.bfs._not_explored = {1: [np.array([1, 0]), np.array([0, 1])]}

        assert len(self.bfs._not_explored[1]) == 2
        MIN_DISTANCE = self.bfs._get_min_distance_key()

        assert MIN_DISTANCE == 1

        moves = self.bfs._pick_moves_at(MIN_DISTANCE)
        assert len(moves) == 2

    def test_pick_a_move_from(self):
        """ given distance at 1 has only one move left,
            function should decrease the size of not_explored by 1 and increase
            the size of explored by 1
        """

        # given distance at 1 should have only one move left
        s = set()
        s.add(tuple(np.array([1, 0])))
        self.bfs._not_explored = {1: s}
        DISTANCE_ONE = 1
        ZERO = 0
        TWO = 2

        valid_moves = self.bfs._pick_moves_at(DISTANCE_ONE)
        min_distance = self.bfs._get_min_distance_key()
        assert len(valid_moves) == 1

        self.assertTrue(np.array_equal(self.bfs._pick_a_move_from(
            valid_moves, min_distance), np.array([1, 0])))

        LENGTH_OF_NOT_EXPLORED = len(self.bfs._not_explored)
        LENGTH_OF_EXPLORED = len(self.bfs._explored)

        assert LENGTH_OF_NOT_EXPLORED == ZERO
        # pdb.set_trace()
        assert LENGTH_OF_EXPLORED == TWO

    def test_valid_moves(self):
        self.bfs._position = np.array([0, 0])
        assert len(self.bfs._get_valid_moves()) == 2

    def test_goal_not_found(self):
        self.bfs._position = np.array([0, 0])
        self.assertFalse(self.bfs._check_goal(self.bfs._get_valid_moves()))

    def test_check_goal_position_below(self):
        """given a position above the goal, check goal should return goal position"""
        self.bfs._position = np.array([6, 7])
        goal_position = self.bfs._check_goal(self.bfs._get_valid_moves())

        self.assertTrue(np.array_equal(goal_position, np.array([7, 7])))

    def test_check_goal(self):
        """given position is a goal, check goal should return the position"""

        self.bfs._position = np.array([7, 7])
        goal_position = self.bfs._check_goal(self.bfs._get_valid_moves())

        self.assertTrue(np.array_equal(goal_position, self.bfs._position))


class TestBfsValidMoves(unittest.TestCase):
    def setUp(self):
        self.position = np.array([0, 0])
        self.goal = 99
        self.bfs = Bfs(self.position, wallgrid, self.goal)
        self.bfs_algo = BfsValidMoves(self.bfs._grid.shape)

    def test_bfs_get_valid_moves(self):
        valid_moves = self.bfs_algo.get_valid_moves(
            self.bfs._position, self.bfs._explored)

        assert len(valid_moves) == 2


class TestPathNotExploredDictionary(unittest.TestCase):
    def setUp(self):
        # takes a list of tuple
        self.path = PathDictionary({2: (np.array([1, 1]))})

    def test_set_item(self):
        assert len(self.path) == 1
        assert len(self.path[2]) == 1
        assert isinstance(self.path[2], (set))

        self.path[2] = np.array([2, 2])

        assert len(self.path[2]) == 2

    def test_key_not_in_dictionary(self):
        """should add the key with a value, if the key
            does not exist"""
        self.path[3] = np.array([2, 1])

        assert len(self.path[3]) == 1

    def test_get_sorted_keys(self):
        key1 = randint(1, 10)
        key2 = randint(4, 10)
        self.path[key1] = np.array([4, 1])
        self.path[key2] = np.array([5, 1])

        keys = self.path.keys()
        # assert len(keys) == 3

        assert keys[0] < keys[1]
        assert keys[-1] > keys[0]

    def test_pop_last_item(self):
        # pdb.set_trace()
        key = 4
        self.path[key] = np.array([2, 2])
        value = self.path.pop(4)
        assert np.array_equal(value, (2, 2))

        assert key not in self.path

    def test_pop_item(self):
        key = 5
        self.path[key] = np.array([4, 1])
        self.path[key] = np.array([1, 4])
        assert len(self.path[key]) == 2
        value = self.path.pop(key)
        assert len(self.path[key]) == 1

        assert np.array_equal(value, (4, 1))

        # self.path.pop(key)

    def test_pop_item_in_explored(self):
        key = 6
        self.path[key] = np.array([5, 1])

        self.path.pop(key)
        assert key not in self.path

        assert len(self.path._explored) == 1

    def test_pop_key_error(self):
        """raises keyError exception if the key is not in path"""
        key = 12
        self.assertRaises(KeyError, self.path.pop, key)

    def test_pop_default_returns(self):
        key = 12
        assert self.path.pop(key, 'finish') == 'finish'
        assert self.path.pop(key, None) == None
