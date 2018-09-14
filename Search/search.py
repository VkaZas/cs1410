# NOTE TO STUDENT: Please read the handout before continuing.

from tilegameproblem import TileGame
from dgraph import DGraph
from queue import Queue, LifoQueue, PriorityQueue


def bfs(problem):
    """
    Implement breadth-first search.

    Input:
        problem - the problem on which the search is conducted, a SearchProblem

    Output: a list of states representing the path of the solution

    """
    pass


def dfs(problem):
    """
    Implement depth-first search.

    Input:
        problem - the problem on which the search is conducted, a SearchProblem

    Output: a list of states representing the path of the solution

    """
    pass


def ids(problem):
    """
    Implement iterative deepening search.

    Input:
        problem - the problem on which the search is conducted, a SearchProblem

    Output: a list of states representing the path of the solution

    """
    pass


def bds(problem, goal):
    """
    Implement bi-directional search.

    The input 'goal' is a goal state (not a search problem, just a state)
    from which to begin the search toward the start state.

    Assume that the input search problem can be thought of as
    an undirected graph. That is, all actions in the search problem
    are reversible.

    Input:
        problem - the problem on which the search is conducted, a SearchProblem

    Output: a list of states representing the path of the solution

    """
    pass


def astar(problem, heur):
    """
    Implement A* search.

    The given heuristic function will take in a state of the search problem
    and produce a real number

    Your implementation should be able to work with any heuristic, heur
    that is for the given search problem (but, of course, without a
    guarantee of optimality if heur is not admissible).

    Input:
        problem - the problem on which the search is conducted, a SearchProblem

    Output: a list of states representing the path of the solution

    """
    pass


### SPECIFIC TO THE TILEGAME PROBLEM


def tilegame_heuristic(state):
    """
    Produces a real number for the given tile game state representing
    an estimate of the cost to get to the goal state.

    Input:
        state - the tilegame state to evaluate. Consult handout for how the tilegame state is represented

    Output: an integer

    """
    pass


### YOUR SANDBOX ###


def main():
    """
    Do whatever you want in here; this is for you.
    An example below shows how your functions might be used.
    """
    # initialize a random 3x3 TileGame problem
    tg = TileGame(3)
    print(TileGame.board_to_pretty_string(tg.get_start_state()))
    # compute path
    path = bfs(tg)
    # display path
    TileGame.print_pretty_path(path)

    # an example with DGraphs:
    small_dgraph = DGraph([[None, 1], [1, None]], {1})
    print(bfs(small_graph))


if __name__ == "__main__":
    main()
