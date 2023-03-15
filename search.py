import os
from parallelHillClimber import PARALLEL_HILLCLIMBER
from solution import SOLUTION
import numpy as np
import random

os.system("rm brain*.nndf")
os.system('rm body*.urdf')
os.system("rm fitness*.txt")
os.system("rm fitness*.png")

phcs = {}
for i in range(4, 14):
    np.random.seed(i)
    random.seed(i)
    phc = PARALLEL_HILLCLIMBER(i)
    phc.Evolve()
    phc.Save_Fitness_Curve()
    phcs[i] = phc

for i in range(4, 14):
    phcs[i].Save_Best_Fitness_Curve()
    # phc.Show_Best()
