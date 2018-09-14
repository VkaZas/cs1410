from searchproblem import SearchProblem
import numpy as np
from pprint import pprint

# The tile game search problem, implemented as a SearchProblem
# States are board configurations.
# Read the assignment handout for details.


class TileGame(SearchProblem):
    def __init__(self, dim, start_state=None, goal_state=None):
        self.__dim = dim
        if start_state == None:
            self.__start_state = TileGame.random_start(dim)
        else:
            self.__start_state = start_state
        if goal_state == None:
            self.goal_state = self.__construct_goal()
        else:
            self.goal_state = goal_state

    ###### SEARCH PROBLEM IMPLEMENTATION ######

    def get_start_state(self):
        return self.__start_state

    def is_goal_state(self, state):
        return state == self.goal_state

    def get_successors(self, state):
        successors = []
        for r in range(self.__dim):
            for c in range(self.__dim):
                if r < self.__dim - 1:
                    successors.append(TileGame.__swap_tiles(state, r, c, r + 1, c))
                if c < self.__dim - 1:
                    successors.append(TileGame.__swap_tiles(state, r, c, r, c + 1))
        costs = [1 for i in range(len(successors))]
        return dict(list(zip(successors, costs)))

    ###### INTERNAL HELPER FUNCTIONS ######

    def __construct_goal(self):
        """
        Given the dimension of the tile game, produces the goal state.
        You should not use this function.
        Instead, use is_goal_state to determine if a given state is the goal.
        """
        dim = self.__dim
        return tuple(
            [
                tuple([j + 1 for j in range(dim * i, dim * (i + 1))])
                for i in range(0, dim)
            ]
        )

    @staticmethod
    def __swap_tiles(board, r1, c1, r2, c2):
        """
        Swaps tile at (r1, c1) with tile at (r2, c2). 0 <= r1,r2,c1,c2 < dim
        """
        aboard = TileGame.tuple_to_list(board)

        temp = aboard[r1][c1]
        aboard[r1][c1] = aboard[r2][c2]
        aboard[r2][c2] = temp
        return TileGame.list_to_tuple(aboard)

    ###### HELPFUL FUNCTIONS FOR YOU ######

    @staticmethod
    def random_start(dim):
        """
        Given the dimension of the tile game, produces a random start state.
        """
        as_list = np.random.permutation(dim ** 2).reshape(dim, dim).tolist()
        increment1 = [[elt + 1 for elt in r] for r in as_list]
        return TileGame.list_to_tuple(increment1)

    @staticmethod
    def list_to_tuple(lstate):
        """
        Converts 2D list to 2D tuple
        """
        return tuple([tuple(r) for r in lstate])

    @staticmethod
    def tuple_to_list(state):
        """
        Converts 2D tuple to 2D list
        """
        return [[elt for elt in r] for r in state]

    @staticmethod
    def board_to_pretty_string(board):
        """
        Takes in a tile game board and outputs a pretty String representation
        of it for printing.
        """
        hbar = "-"
        vbar = "|"
        corner = "+"
        dim = len(board)

        s = corner
        for i in range(2 * dim - 1):
            s += hbar
        s += corner + "\n"

        for r in range(dim):
            s += vbar
            for c in range(dim):
                s += str(board[r][c]) + " "
            s = s[:-1]
            s += vbar
            s += "\n"

        s += corner
        for i in range(2 * dim - 1):
            s += hbar
        s += corner
        return s

    @staticmethod
    def print_pretty_path(board_path):
        """
        Takes in a list of boards, board_path, and prints them out as
        pretty strings, separated by newlines.
        """
        for b in board_path:
            print(TileGame.board_to_pretty_string(b))
