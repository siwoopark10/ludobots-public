import os
from parallelHillClimber import PARALLEL_HILLCLIMBER

os.system("rm brain*.nndf")
os.system("rm fitness*.txt")

phc = PARALLEL_HILLCLIMBER()
phc.Evolve()
phc.Show_Best()
