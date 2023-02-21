import os
from parallelHillClimber import PARALLEL_HILLCLIMBER
from snake import SNAKE
from solution import SOLUTION

# os.system("rm brain*.nndf")
# os.system("rm fitness*.txt")

# phc = PARALLEL_HILLCLIMBER()
# phc.Evolve()
# phc.Show_Best()

for i in range(5):
    solution = SOLUTION()
    solution.Start_Simulation()
