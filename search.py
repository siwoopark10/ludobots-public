import os
from parallelHillClimber import PARALLEL_HILLCLIMBER
from solution import SOLUTION
import numpy as np
import random

os.system("rm brain*.nndf")
os.system('rm body*.urdf')
os.system("rm fitness*.txt")
os.system("rm fitness*.png")

for i in range(5):
    np.random.seed(i)
    random.seed(i)
    phc = PARALLEL_HILLCLIMBER(i)
    phc.Evolve()
    phc.Save_Fitness_Curve()
    phc.Show_Best()

# for i in range(1):
#     solution = SOLUTION(i)
#     solution.Start_Simulation("GUI")
#     solution.Wait_For_Simulation_To_End()
