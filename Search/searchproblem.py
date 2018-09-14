from abc import ABCMeta, abstractmethod

# In SearchProblem, we require that all states are hashable.
#
# ints and strings are hashable, as well as most of Python's immutable
# built-in data structures (e.g. tuples, but not lists or dictionaries)


class SearchProblem(metaclass=ABCMeta):
    @abstractmethod
    def get_start_state(self):
        """
        Produces the state from which to search.
        """
        pass

    @abstractmethod
    def is_goal_state(self, state):
        """
        Produces the boolean that the given state is a goal state.
        """
        pass

    @abstractmethod
    def get_successors(self, state):
        """
        Produces a dictionary, whose keys are the states that can be reached
        from the given state, and whose values are the costs of reaching
        each associated key.
        """
        pass
