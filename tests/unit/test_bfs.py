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

    def test_get_valid_moves_position_zero_zero(self):
        position = np.array([0, 0])
        expected_moves = np.array([self.d, self.r])
        expected_number_of_moves = len(expected_moves)

        self.__assertTrue(position, expected_moves, expected_number_of_moves)

    def test_get_valid_moves_position_nine_nine(self):
        position = np.array([9, 9])
        expected_moves = np.array([self.u, self.l])
        expected_number_of_moves = len(expected_moves)

        self.__assertTrue(position, expected_moves, expected_number_of_moves)

    def test_get_valid_moves_position_six_six(self):
        position = np.array([6, 6])
        expected_moves = np.array([self.u, self.d, self.r, self.l])
        expected_number_of_moves = len(expected_moves)

        self.__assertTrue(position, expected_moves, expected_number_of_moves)

    def test_walls_position_zero_two(self):
        position = np.array([0, 2])
        expected_moves = np.array([self.r, self.l])
        expected_number_of_moves = len(expected_moves)

        self.__assertTrue(position, expected_moves, expected_number_of_moves)

    def __assertTrue(self, position, expected_moves, exp_num_of_moves):
        test_moves = get_valid_moves(moves, position, grid)
        assert len(test_moves) == exp_num_of_moves
        self.assertTrue(np.array_equal(test_moves, expected_moves))


class TestDistance(unittest.TestCase):
    def setUp(self):
        self.position = np.array([4, 4])
        self.valid_moves = get_valid_moves(moves, self.position, grid)

    def test_position_4_4_should_have_4_valid_moves(self):
        assert len(self.valid_moves) == 4

    def test_position_4_4_should_have_distance_8(self):
        distance = get_distance(self.position)  # return {}
        self.assertEqual(distance, 8)

    def test_position_4_4_at_distance_7_should_have_2_valid_moves(self):
        """ distance dictionary should retrun {7:[[4, 3]. [3, 4]], 9:[[4, 5], [5, 4]]}"""
        ds = get_distance_all_valid_moves(self.valid_moves, self.position)
        self.assertEqual(len(ds), 2)
        self.assertEqual(len(ds[7]), 2)
