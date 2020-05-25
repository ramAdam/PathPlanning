import unittest
import numpy as np
from pathfinding import *
import pdb


class TestValidMoves(unittest.TestCase):
    def setUp(self):
        self.u = np.array([-1, 0])  # up
        self.d = np.array([1, 0])  # down
        self.r = np.array([0, 1])  # left
        self.l = np.array([0, -1])  # right
        self.empty_explored = []

    def test_get_valid_moves_position_zero_zero(self):
        explored = [np.array([0, 0])]
        position = np.array([0, 0])
        expected_moves = np.array([self.d, self.r])
        expected_number_of_moves = len(expected_moves)

        self.expectedMovesEqualsValidMoves(position, expected_moves,
                                           expected_number_of_moves, explored)

    def test_position_0_1_with_explored_pos_0_0_should_return_right(self):
        """Should return one expected valid move, right only"""
        explored = [np.array([0, 0])]
        expected_moves = np.array([self.r])

        self.expectedMovesEqualsValidMoves(np.array([0, 1]), expected_moves, len(
            expected_moves), explored)

    def test_get_valid_moves_position_nine_nine(self):
        position = np.array([9, 9])
        expected_moves = np.array([self.u, self.l])
        expected_number_of_moves = len(expected_moves)

        self.expectedMovesEqualsValidMoves(position, expected_moves,
                                           expected_number_of_moves, self.empty_explored)

    def test_get_valid_moves_position_six_six_should_return_4_moves(self):
        position = np.array([6, 6])
        expected_moves = np.array([self.u, self.d, self.r, self.l])
        expected_number_of_moves = len(expected_moves)

        self.expectedMovesEqualsValidMoves(position, expected_moves,
                                           expected_number_of_moves, self.empty_explored)

    def test_walls_position_zero_two_should_return_2_expected_moves(self):
        position = np.array([0, 2])
        expected_moves = np.array([self.r, self.l])
        expected_number_of_moves = len(expected_moves)

        self.expectedMovesEqualsValidMoves(position, expected_moves,
                                           expected_number_of_moves, self.empty_explored)

    def expectedMovesEqualsValidMoves(self, position, expected_moves, exp_num_of_moves, exp):
        test_moves = get_valid_moves(moves, position, grid, exp)
        assert len(test_moves) == exp_num_of_moves
        self.assertTrue(np.array_equal(test_moves, expected_moves))


class TestDistance(unittest.TestCase):
    def setUp(self):
        self.position = np.array([4, 4])
        self.empty_explored = []
        self.valid_moves = get_valid_moves(
            moves, self.position, grid, self.empty_explored)

    def test_position_4_4_should_have_4_valid_moves(self):
        assert len(self.valid_moves) == 4

    def test_position_4_4_should_have_distance_8(self):
        distance = get_distance(self.position)  # return {}
        self.assertEqual(distance, 8)

    def test_position_4_4_at_distance_7_should_have_2_valid_moves(self):
        """ distance dictionary should have {7:[[4, 3]. [3, 4]], 9:[[4, 5], [5, 4]]}"""
        ds = get_distance_all_valid_moves(self.valid_moves, self.position)
        self.assertEqual(len(ds), 2)
        self.assertEqual(len(ds[7]), 2)


class TestIsInExplored(unittest.TestCase):
    def setUp(self):
        self.exp = [np.array([0, 0]), np.array([1, 1])]

    def test_position_exist_in_explored_should_return_true(self):
        position = np.array([0, 0])

        self.assertTrue(isin_explored(position, self.exp))

    def test_position_in_expolored_should_return_false(self):
        position = np.array([2, 1])
        self.assertFalse(isin_explored(position, self.exp))
