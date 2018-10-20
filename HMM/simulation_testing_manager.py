import numpy as np
from touchscreen_helpers.simulator import touchscreenSimulator
from touchscreen_helpers.simulation_evaluator import touchscreenEvaluator
from touchscreen import touchscreenHMM


class SimulationTestingManager:
    def __init__(self):
        pass

    def run_simulation(
        self,
        width=20,
        height=20,
        frames=50,
        visualization=True,
        evaluate=False,
        save=True,
        file_name="saved_sim.txt",
        frame_length=0.5,
    ):
        if not visualization and not evaluate and not save:
            print(
                "ERROR: visualization, evaluate, and save flags are all false. Exiting..."
            )
            return
        self.simulation_instance = touchscreenSimulator(
            width=width, height=height, frames=frames
        )
        print("Running simulation.")
        self.simulation_instance.run_simulation()
        if save:
            print("Saving simulation to " + file_name)
            f = open(file_name, "a")
            f.truncate(0)
            f.write("%d %d %d\n" % (width, height, frames))
            temp_frame = self.simulation_instance.get_frame(actual_position=True)
            while temp_frame is not None:
                noisy_loc = np.asarray(np.where(temp_frame[0] == 1)).T.tolist()[0]
                actual_loc = np.asarray(np.where(temp_frame[1] == 1)).T.tolist()[0]
                to_print = noisy_loc + actual_loc
                np.savetxt(f, to_print, fmt="%i", newline=" ")
                f.write("\n")
                temp_frame = self.simulation_instance.get_frame(actual_position=True)
            f.close()
            # print("Simulation saved to saved_sim.txt")
            self.simulation_instance.timestamp = 0
        if evaluate:
            student_hmm = touchscreenHMM(width, height)
            if visualization:
                self.simulation_instance.visualize_results(
                    student_hmm=student_hmm, frame_length=frame_length
                )
            evaluator = touchscreenEvaluator()
            score = evaluator.evaluate_touchscreen_hmm(
                student_hmm, self.simulation_instance
            )
            print("Score: ", score)
        else:
            if visualization:
                self.simulation_instance.visualize_simulation(frame_length=frame_length)

    def run_saved_simulation(
        self,
        file_name="saved_sim.txt",
        visualization=True,
        evaluate=False,
        student_hmm=None,
        frame_length=0.5,
    ):
        if not visualization and not evaluate:
            # both false, whats the point
            print("ERROR: visualization and evaluate flags are both false. Exiting...")
            return

        print("Reading saved simulation from " + file_name)
        f = open(file_name, "r")
        first_line = [int(x) for x in f.readline().strip().split(" ")]
        width, height, frames = first_line[0], first_line[1], first_line[2]
        # print(width,height,frames)
        data = np.loadtxt(f, dtype="int", skiprows=0)
        # print(data)
        f.close()

        self.simulation_instance = touchscreenSimulator(
            width=width, height=height, frames=frames
        )
        self.simulation_instance.load_simulation(data)
        if evaluate:
            student_hmm = touchscreenHMM(width, height)
            if visualization:
                self.simulation_instance.visualize_results(
                    student_hmm=student_hmm, frame_length=frame_length
                )
            evaluator = touchscreenEvaluator()
            score = evaluator.evaluate_touchscreen_hmm(
                student_hmm, self.simulation_instance
            )
            print("Score: ", score)
        else:
            if visualization:
                self.simulation_instance.visualize_simulation(frame_length=frame_length)
