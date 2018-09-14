import unittest
from tilegameproblem import TileGame
from search import bfs, dfs, ids, astar, bds, tilegame_heuristic


class IOTest(unittest.TestCase):
    """
    Tests IO for search implementations. Contains basic/trivial test cases.

    Each test function instantiates a search problem (TileGame) and tests if the trivial test case
    contains the solution, the start state is in the solution, the end state is in the
    solution and the length of the solutions are the same.
    """

    def _check_algorithm(self, algorithm):
        simple_state = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
        # Construct a TileGame where the start and goal states are the same
        tg = TileGame(3, simple_state, simple_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_state, "Path should start with the start state"
        )
        self.assertEqual(path[-1], simple_state, "Path should end with the end state")
        self.assertEqual(len(path), 1, "Path length should be one")

    def test_bfs(self):
        self._check_algorithm(bfs)

    def test_dfs(self):
        self._check_algorithm(dfs)

    def test_bds(self):
        simple_state = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
        self._check_algorithm(lambda p: bds(p, simple_state))

    def test_ids_output(self):
        self._check_algorithm(ids)

    def test_astar_output(self):
        self._check_algorithm(lambda p: astar(p, lambda s: 0))


if __name__ == "__main__":
    unittest.main()
