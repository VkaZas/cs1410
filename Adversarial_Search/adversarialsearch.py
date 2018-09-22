from adversarialsearchproblem import AdversarialSearchProblem
from gamedag import GameDAG, DAGState


def minimax(asp):
    """
	Implement the minimax algorithm on ASPs,
	assuming that the given game is both 2-player and constant-sum

	Input: asp - an AdversarialSearchProblem
	Output: an action(an element of asp.get_available_actions(asp.get_start_state()))
	"""
    pass


def alpha_beta(asp):
    """
	Implement the alpha-beta pruning algorithm on ASPs,
	assuming that the given game is both 2-player and constant-sum.

	Input: asp - an AdversarialSearchProblem
	Output: an action(an element of asp.get_available_actions(asp.get_start_state()))
	"""
    pass


def alpha_beta_cutoff(asp, cutoff_ply, eval_func):
    """
	This function should:
	- search through the asp using alpha-beta pruning
	- cut off the search after cutoff_ply moves have been made.

	Inputs:
		asp - an AdversarialSearchProblem
		cutoff_ply- an Integer that determines when to cutoff the search
			and use eval_func.
			For example, when cutoff_ply = 1, use eval_func to evaluate
			states that result from your first move. When cutoff_ply = 2, use
			eval_func to evaluate states that result from your opponent's
			first move. When cutoff_ply = 3 use eval_func to evaluate the
			states that result from your second move.
			You may assume that cutoff_ply > 0.
		eval_func - a function that takes in a GameState and outputs
			a real number indicating how good that state is for the
			player who is using alpha_beta_cutoff to choose their action.
			You do not need to implement this function, as it should be provided by
			whomever is calling alpha_beta_cutoff, however you are welcome to write
			evaluation functions to test your implemention

	Output: an action(an element of asp.get_available_actions(asp.get_start_state()))
	"""
    pass


def general_minimax(asp):
    """
	Implement the generalization of the minimax algorithm that was
	discussed in the handout, making no assumptions about the
	number of players or reward structure of the given game.

	Input: asp - an AdversarialSearchProblem
	Output: an action(an element of asp.get_available_actions(asp.get_start_state()))
	"""
    pass
