import time
from tttproblem import TTTProblem
import adversarialsearch as MyImplementation


def run_game(asp, bots, visualizer=None, delay=0.2):
    """
	Inputs:
		- asp: a game to play, represented as an adversarial search problem
		- bots: a list in which the i'th element is adversarial search
		        algorithm that player i will use.
		        The algorithm must take in an ASP only and output an action.
		- visualizer (optional): a void function that takes in a game state
		  and prints a visualization of it to the terminal.
		  If no visualizer argument is passed, run_game will not visualize games.

		- delay: the amount of time to wait in between displaying game states
		         (if visualizing)

	Output:
		- the evaluation of the terminal state.
	"""
    state = asp.get_start_state()
    if not visualizer == None:
        visualizer(state)
        time.sleep(delay)

    while not (asp.is_terminal_state(state)):
        decision = bots[state.player_to_move()](asp)

        available_actions = asp.get_available_actions(state)

        # if the bot tries to make an invalid action,
        # returns the first valid action
        if not decision in available_actions:
            decision = list(available_actions)[0]

        result_state = asp.transition(state, decision)
        asp.set_start_state(result_state)

        state = result_state
        if not visualizer == None:
            visualizer(state)
            time.sleep(delay)

    return asp.evaluate_state(asp.get_start_state())


def main():
    game = TTTProblem()
    bots = [MyImplementation.minimax, MyImplementation.minimax]

    # runs game and prints final scores
    print(run_game(game, bots, TTTProblem.visualize_state))


if __name__ == "__main__":
    main()
