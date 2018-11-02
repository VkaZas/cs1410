import os
import numpy as np

if os.path.isfile("policy_taxi_sarsa_grading.npy") and os.path.isfile(
    "qvalues_taxi_sarsa_grading.npy"
):
    taxi_sarsa_policy = np.load("policy_taxi_sarsa_grading.npy")
    qvalues_taxi_sarsa = np.load("qvalues_taxi_sarsa_grading.npy")

if os.path.isfile("policy_taxi_sarsa_lambda_grading.npy") and os.path.isfile(
    "qvalues_taxi_sarsa_lambda_grading.npy"
):
    taxi_sarsa_policy_lambda = np.load("policy_taxi_sarsa_lambda_grading.npy")
    qvalues_taxi_sarsa_lambda = np.load("qvalues_taxi_sarsa_lambda_grading.npy")

if os.path.isfile("mountain_car_saved_weights_grading.npy"):
    try:
        from mountain_car_sarsa_fourier import create_multipliers, phi

        mountain_car_weights = np.load("mountain_car_saved_weights_grading.npy")
        mountain_car_create_mults = create_multipliers
        mountain_car_phi = phi
    except Exception as e:
        print("Unable to load mountain car")
        print(e)
