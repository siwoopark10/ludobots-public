from solution import SOLUTION
import constants as c
import copy
from matplotlib import pyplot as plt


class PARALLEL_HILLCLIMBER:
    def __init__(self, id) -> None:
        self.parents = {}
        self.id = id
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        self.x = []
        self.y = []

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            # if currentGeneration == 0:
            self.Save_Best(currentGeneration)
            print('\n\n\nEvolved\n\n\n')
            self.Evolve_For_One_Generation()

    def Evaluate(self, solutions):
        for i in solutions:
            print('run', i)
            solutions[i].Start_Simulation()

        for i in solutions:
            print('wait')
            solutions[i].Wait_For_Simulation_To_End()

    def Evolve_For_One_Generation(self):
        self.Spawn()

        self.Mutate()

        self.Evaluate(self.children)

        self.Select()

        # self.Print()

    def Spawn(self):
        self.children = {}
        for i in self.parents:
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for i in self.children:
            self.children[i].Mutate()

    def Select(self):
        for i in self.parents:
            if self.parents[i].fitness < self.children[i].fitness:
                self.parents[i] = self.children[i]

    def Save_Best(self, curGen):
        bestIndex = 0
        for i in self.parents:
            if self.parents[i].fitness > self.parents[bestIndex].fitness:
                bestIndex = i
        self.x.append(curGen)
        self.y.append(self.parents[bestIndex].fitness)
        print("best fitness: ", self.parents[bestIndex].fitness)

    def Show_Best(self):
        bestIndex = 0
        for i in self.parents:
            if self.parents[i].fitness > self.parents[bestIndex].fitness:
                bestIndex = i
        print("best fitness: ", self.parents[bestIndex].fitness)
        self.parents[bestIndex].Start_Simulation(directOrGUI="GUI")

    def Print(self):
        for i in self.parents:
            print(
                f'parent: {self.parents[i].fitness}, child: {self.children[i].fitness}\n\n')

    def Save_Fitness_Curve(self):
        plt.plot(self.x, self.y, label=f"PHC{self.id}")
        plt.legend()
        plt.xlabel("Generations")
        plt.ylabel("Fitness")
        plt.savefig(f'fitness_curve_{self.id}.png')
