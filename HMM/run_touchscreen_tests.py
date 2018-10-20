from simulation_testing_manager import SimulationTestingManager
from touchscreen import touchscreenHMM

# You can test with any size (smaller size will be easier to see and follow)
# However, we will be running all graded tests using 20x20 screens
student_solution = touchscreenHMM(20, 20)

testing_manager = SimulationTestingManager()

"""
SimulationTestingManager's run_simulation:

FORMAT: name of flag - (type) description. Default = value

width - (int) specify the width of the simluation. Default = 20
height - (int) specify the height of the simluation. Default = 20
frames - (int) specify number of frames to run for simulation. Default = 50
visualization - (bool) specify whether to visualize simulation. Default = True
evaluate - (bool) specify whether to evaluate student solution. Default = False
           If True, the student's touchscreenHMM will automatically be intialized within this testing manager
save (bool) - specify whether to save the current run. Default = True
file_name (string) - specify a filename to save the simulation run to. Default = 'saved_sim.txt'
                     Only used when save flag is true.
frame_length (float) - specify the number of seconds each frame is shown for (lower for faster simulation). Default = 0.5
"""

# Basic simulation run, same functionality as run_visual_simulation.py
testing_manager.run_simulation(
    width=20, height=20, frames=100, visualization=True, evaluate=False
)

# This will evaluate your solution and print your score without visualization
testing_manager.run_simulation(frames=100, visualization=False, evaluate=True)

# This will visualize the simulation and display your distribution at the same time.
# Then it will evaluate your solution and print your score.
testing_manager.run_simulation(
    frames=100, visualization=True, evaluate=True, frame_length=1.0
)

# Will save a simulation to saved_sim.txt. Specify the file_name flag to customize the file name.
# Be careful, running this with an existing file_name will overwrite the last saved run in that file.
testing_manager.run_simulation(frames=100, save=True)

"""
SimulationTestingManager's run_saved_simulation:

To be used when running a simulation that was previously saved to disk.

FORMAT: name of flag - (type) description. Default = value

visualization - (bool) specify whether to visualize simulation. Default = True
evaluate - (bool) specify whether to evaluate student solution. Default = False
           If True, a student_hmm must be passed in
student_hmm - (touchscreenHMM)  if evaluate flag is true, must pass in an instance of touchscreenHMM.
frame_length (float) - specify the number of seconds each frame is shown for (lower for faster simulation). Default = 0.5
"""

# Save a run to simple_text.txt
testing_manager.run_simulation(
    width=20, height=20, frames=10, save=True, file_name="simple_text.txt"
)

# In order to visualize with the saved data in simple_text.txt:
testing_manager.run_saved_simulation(file_name="simple_text.txt", frame_length=0.1)

# Test against the saved data without visualizing
testing_manager.run_saved_simulation(
    file_name="simple_text.txt",
    visualization=False,
    evaluate=True,
    student_hmm=student_solution,
)
