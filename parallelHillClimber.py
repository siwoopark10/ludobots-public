from solution import SOLUTION
import constants as c
import copy
from matplotlib import pyplot as plt
import pickle
from collections import defaultdict
import os


class PARALLEL_HILLCLIMBER:
    def __init__(self, id) -> None:
        self.parents = {}
        self.id = id
        self.nextAvailableID = 0
        self.new_dir = f"results/seed_{id}"
        os.makedirs(self.new_dir, exist_ok=True)
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.parents[i].Initialize_Weights()
            filename = f'Parent{i}_Generation{0}'
            with open(os.path.join(self.new_dir, filename), 'wb') as f:
                pickle.dump(self.parents[i], f)
            self.nextAvailableID += 1
        self.storedGen = [100, 200, 499]
        self.x = []
        self.y = []
        self.ypop = defaultdict(list)
        self.mutations = ['Synapse weight', "Link size", "Limb size", "Link sensor",
                          "Limb sensor", "Add link", "Subtract link", "Generate limbs"]
        self.successfuly_mutations = [0 for i in range(8)]

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            # if currentGeneration == 0:
            self.Save_Best(currentGeneration)
            self.Evolve_For_One_Generation()

    def Evaluate(self, solutions):
        for i in solutions:
            # print('run', i)
            solutions[i].Start_Simulation()

        for i in solutions:
            # print('wait')
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
                self.successfuly_mutations[self.children[i].selected_mutation] += 1
                self.parents[i] = self.children[i]

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

    def Save_Best(self, curGen):
        bestIndex = 0
        if curGen in self.storedGen:
            for i in self.parents:
                filename = f'Parent{i}_Generation{curGen}'
                with open(os.path.join(self.new_dir, filename), 'wb') as f:
                    pickle.dump(self.parents[i], f)
        for i in self.parents:
            self.ypop[i].append(self.parents[i].fitness)
            if self.parents[i].fitness > self.parents[bestIndex].fitness:
                bestIndex = i
        self.x.append(curGen)
        self.y.append(self.parents[bestIndex].fitness)
        print("\n\n\nbest fitness: ",
              self.parents[bestIndex].fitness, '\n\n\n')

    def Save_Fitness_Curve(self):
        plt.figure(1+self.id*2, figsize=(10, 6))
        for i in self.parents:
            plt.plot(self.x, self.ypop[i], label=f'Population {i}')
            plt.legend(loc='lower right')
            plt.title("Fitness of each population over generations")
            plt.xlabel("Generations")
            plt.ylabel("Fitness")
            plt.rc('xtick', labelsize=8)
            plt.rc('legend', fontsize=6)
            plt.savefig(
                f'results/seed_{self.id}/fitness_curve_per_population_{self.id}.png')

        plt.figure(2+self.id*2, figsize=(9, 6))
        plt.plot(self.mutations, self.successfuly_mutations)
        plt.title("Mutations that improved robot's fitness")
        plt.xlabel("Mutations")
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.ylabel("Count")
        plt.savefig(f'results/seed_{self.id}/mutation_count.png')

    def Save_Best_Fitness_Curve(self):
        plt.figure(0, figsize=(9, 6))
        plt.plot(self.x, self.y, label=f"PHC{self.id-4}")
        plt.legend()
        plt.rc('legend', fontsize=6)
        plt.title("Parallel Hill Climber Best Fitness over Generations")
        plt.xlabel("Generations")
        plt.ylabel("Fitness")
        plt.savefig(f'results/phc_fitness_curve.png')
