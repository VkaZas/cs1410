import unittest
from adversarialsearchproblem import AdversarialSearchProblem
from gamedag import GameDAG, DAGState
from adversarialsearch import minimax, alpha_beta, alpha_beta_cutoff, general_minimax


class IOTest(unittest.TestCase):
    """
    Tests IO for adversarial search implementations.
    Contains basic/trivial test cases.

    Each test function instantiates an adversarial search problem (DAG) and tests
    that the algorithm returns a valid action.

    It does NOT test whether the action is the "correct" action to take
    """

    def _get_test_dag(self):
        """
    	An example of an implemented GameDAG from the gamedag class.
    	Look at handout in section 3.3 to see visualization of the tree.

        Output: GameDAG to be used for testing
    	"""
        matrix = [
            [False, True, True, False, False, False, False],
            [False, False, False, True, True, False, False],
            [False, False, False, False, False, True, True],
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False],
        ]
        start_state = DAGState(0, 0)
        terminal_indices = set([3, 4, 5, 6])
        evaluations_at_terminal = {3: [-1, 1], 4: [-2, 2], 5: [-3, 3], 6: [-4, 4]}
        turns = [0, 1, 1, 0, 0, 0, 0]
        dag = GameDAG(
            matrix, start_state, terminal_indices, evaluations_at_terminal, turns
        )
        return dag

    def _check_result(self, result, dag):
        """
            Tests whether the result is one of the possible actions
            of the dag.
            Input:
                result- the return value of an adversarial search problem.
                    This should be an action
                dag- the GameDAG that was used to test the algorithm
        """
        self.assertIsNotNone(result, "Output should not be None")
        start_state = dag.get_start_state()
        potentialActions = dag.get_available_actions(start_state)
        self.assertTrue(
            result in potentialActions, "Output should be an available action"
        )

    def _general_check_algorithm(self, algorithm):
        """
            instantiates an adversarial search problem (DAG), and
            checks that the result is an action
            Input:
                algorithm- a function that takes in an asp and returns an
                action
        """
        dag = self._get_test_dag()
        result = algorithm(dag)
        self._check_result(result, dag)

    def _dummy_eval_func(self, gameState):
        return 0

    def test_minimax(self):
        self._general_check_algorithm(minimax)
        print("minimax passes basic I/O specifications")

    def test_alpha_beta(self):
        self._general_check_algorithm(alpha_beta)
        print("alpha-beta passes basic I/O specifications")

    def test_alpha_beta_cutoff(self):
        dag = self._get_test_dag()
        cutoff = 1
        result = alpha_beta_cutoff(dag, cutoff, self._dummy_eval_func)
        self._check_result(result, dag)
        print("alpha-beta cutoff passes basic I/O specifications")

    def test_general_minimax(self):
        self._general_check_algorithm(general_minimax)
        print("general minimax passes basic I/O specifications")


if __name__ == "__main__":
    unittest.main()
