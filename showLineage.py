import pickle
import os

seed = 6
i = 5
storedGenerations = [0, 100, 200, 499]
directory = f"results/seed_{seed}"
print(directory, 'Parent ', i)
for gen in storedGenerations:
    print(f"Generation {gen}")
    file = f'Parent{i}_Generation{gen}'
    with open(os.path.join(directory, file), "rb") as f:
        solution = pickle.load(f)
        solution.Start_Simulation("GUI")
