# A matrix representation of a directed graph.
# This is for your testing.
# Read the assignment handout for details.

from searchproblem import SearchProblem


class DGraph(SearchProblem):
    def __init__(self, matrix, goal_indices, start_state=0):
        """
        matrix - the matrix representation of the directed graph

        goal_indices - a Python set of the indices of the states
                       that are goal states.

        start_state - the index of the start state. 0 by default.
        """
        self.matrix = matrix
        self.goal_indices = goal_indices
        self.start_state = start_state

    def get_start_state(self):
        return self.start_state

    def is_goal_state(self, state):
        return state in self.goal_indices

    def get_successors(self, state):
        row = self.matrix[state]
        successors = {}
        index = 0
        for cost in row:
            if not (cost == None):
                successors[index] = cost
            index += 1
        return successors
