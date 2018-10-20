from .simulator import *


def create_simulations(size=20, frames=100):
    """
    Creates a simulator and selects all frames. This can be useful when you are trying to better understand the
    behaviour of the touchscreen simulator
    :param size: The size of the screen
    :param frames: The number of frames to generate over
    :return: A list of tuples, with each index representing a timestep. Each tuple contains the actual screen, and the
    noisy screen, with each screen represented as a numpy array.
    """
    sim_data = []
    sim = touchscreenSimulator(width=size, height=size, frames=frames)
    sim.run_simulation()
    for frame in range(frames):
        sim_data.append(sim.get_frame(actual_position=True))

    return sim_data
