import os
from parallelHillClimber import PARALLEL_HILLCLIMBER
from solution import SOLUTION

os.system("rm brain*.nndf")
os.system("rm fitness*.txt")

phc = PARALLEL_HILLCLIMBER()
phc.Evolve()
phc.Show_Best()

# for i in range(1):
#     solution = SOLUTION(i)
#     solution.Start_Simulation("GUI")
#     solution.Wait_For_Simulation_To_End()
