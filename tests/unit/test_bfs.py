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


class TestMove(unittest.TestCase):
    def setUp(self):
        self.position = np.array([0, 0])
        self.explored = [np.array([0, 0])]
        self.not_explored = {}
        self.goal_found = False
        self.goal = 99
        self.bfs = Bfs(self.position, self.explored,
                       self.not_explored, self.goal_found, grid, self.goal)

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
        pdb.set_trace()
        # given distance at 1 should have only one move left
        self.bfs._not_explored = {1: [np.array([1, 0])]}
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
        assert LENGTH_OF_EXPLORED == TWO

    def test_valid_moves(self):
        self.bfs._position = np.array([0, 0])
        assert len(self.bfs._get_valid_moves()) == 2

    def test_goal_not_found(self):
        self.bfs._position = np.array([0, 0])
        self.assertFalse(self.bfs._check_goal(self.bfs._get_valid_moves()))

    def test_goal_found(self):
        """given a position above the goal, move should return goal found"""
