import unittest
import numpy as np
from pathfinding import *
import pdb
from tests.data import wallgrid


class TestBfs(unittest.TestCase):

    def setUp(self):
        self.position = np.array([0, 0])
        self.explored = [np.array([0, 0])]
        # self.not_explored = {}
        self.goal_found = False
        self.goal = 99
        self.bfs = Bfs(self.position, wallgrid, self.goal)

    def test_move(self):
        """given a wall grid with a position (0, 0)"""
        # pdb.set_trace()
        self.bfs.move()
        assert self.bfs._goal_found == False
        assert np.array_equal(self.bfs._position, np.array([0, 1]))
        # at distance one there should be only one position left
        assert len(self.bfs._not_explored[1]) == 1
        # at distance 1 there should be 2 explored positions
        assert len(self.bfs._explored) == 2

    def test_goal_position(self):
        """given goal 99 is at position (7 7), bfs position should be set to (7, 7)"""

        while not self.bfs._goal_found:
            self.bfs.move()

        assert np.array_equal(self.bfs._position, np.array([7, 7]))

    def test_goal_found(self):
        "given goal 99 in the grid, it should find the goal"
        while not self.bfs._goal_found:
            # pdb.set_trace()
            self.bfs.move()

        assert self.bfs._goal_found == True

    def test_goal_not_found(self):
        pass

    def test_position_above_the_goal(self):
        """given position above the goal (6, 7), goal_found should be True"""
        self.bfs._position = np.array([6, 7])
        # pdb.set_trace()
        assert np.array_equal(self.bfs.move(), np.array([7, 7]))
        self.assertTrue(self.bfs._goal_found)
