import unittest
import numpy as np
from pathfinding import *
import pdb
from tests.data import wallgrid, grid


class TestBfs(unittest.TestCase):

    def setUp(self):
        position = np.array([0, 0])
        self.goal = 99
        self.bfs = Bfs(position, wallgrid, self.goal)

    def test_move(self):
        """given a wall grid with a position (0, 0)"""

        self.bfs.move()
        assert self.bfs._goal_found == False
        assert np.array_equal(self.bfs._position, np.array([0, 1]))

        assert len(self.bfs._path._not_explored[1]) == 1

        assert len(self.bfs._path._explored) == 2

    def test_goal_position(self):
        """given goal 99 is at position (7 7), bfs position should be set to (7, 7)"""

        while not self.bfs._goal_found:
            self.bfs.move()

        assert np.array_equal(self.bfs._position, np.array([7, 7]))

    def test_goal_found(self):
        "given goal 99 in the grid, it should find the goal"
        while not self.bfs._goal_found:
            self.bfs.move()

        assert self.bfs._goal_found == True

    def test_goal_not_found(self):
        """goal found should be false, after searching the grid for goal"""
        bfs = Bfs(np.array([0, 0]), grid, 99)
        flag = True

        ROW_BOUND = grid.shape[0] - 1
        COL_BOUND = grid.shape[1] - 1

        end_bounds = (ROW_BOUND, COL_BOUND)

        while flag:
            bfs.move()
            if np.array_equal(bfs._position, end_bounds) and not bfs._goal_found:
                flag = False

        assert np.array_equal(bfs._position, (9, 9))
        assert not bfs._goal_found

    def test_position_above_the_goal(self):
        """given position above the goal (6, 7), goal_found should be True"""
        self.bfs._position = np.array([6, 7])
        self.bfs.move()

        assert np.array_equal(self.bfs._position, np.array([7, 7]))
        self.assertTrue(self.bfs._goal_found)


class TestGoalSearch(unittest.TestCase):

    def setUp(self):
        self.bfs_with_goal = Bfs(np.array([0, 0]), grid, 99)
        self.search = GoalSearch(self.bfs_with_goal)

    def test_search_goal_not_found(self):
        bfs_with_goal = Bfs(np.array([0, 0]), grid, 99)
        search = GoalSearch(bfs_with_goal)

        self.assertFalse(search.find())
        self.assertTrue(search._position == (9, 9))

    def test_search_goal_found(self):
        """given a grid with a goal, search finds the goal and returns true"""
        bfs_with_goal = Bfs(np.array([0, 0]), wallgrid, 99)
        search = GoalSearch(bfs_with_goal)

        self.assertTrue(search.find())
        assert search._position == (7, 7)

    def test_grid_bounds(self):
        assert self.search._end_bounds == (9, 9)
