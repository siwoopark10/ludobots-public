from solution import SOLUTION
import constants as c
import copy


class PARALLEL_HILLCLIMBER:
    def __init__(self) -> None:
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(2):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            # if currentGeneration == 0:
            #     self.Show_Best()
            print('here')
            self.Evolve_For_One_Generation()

    def Evaluate(self, solutions):
        for i in solutions:
            print('run')
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
            if self.parents[i].fitness > self.children[i].fitness:
                self.parents[i] = self.children[i]

    def Show_Best(self):
        bestIndex = 0
        for i in self.parents:
            if self.parents[i].fitness < self.parents[bestIndex].fitness:
                bestIndex = i
        print("best fitness: ", self.parents[bestIndex].fitness)
        self.parents[bestIndex].Start_Simulation(directOrGUI="GUI")

    def Print(self):
        for i in self.parents:
            print(
                f'parent: {self.parents[i].fitness}, child: {self.children[i].fitness}\n\n')
