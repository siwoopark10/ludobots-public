import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c


class SOLUTION:
    def __init__(self) -> None:
        # self.weights = np.random.rand(
        #     c.numSensorNeurons, c.numMotorNeurons) * 2 - 1
        # self.myID = myID
        self.randomLinkNum = random.randint(4, 8)
        self.armIndex = 0
        self.legIndex = 0
        self.linksWithSensors = np.random.randint(2, size=self.randomLinkNum)

    # def Set_ID(self, id):
    #     self.myID = id

    def Start_Simulation(self, directOrGUI="DIRECT"):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python3 simulate.py GUI")

    # def Wait_For_Simulation_To_End(self):
    #     fitnessFileName = f"fitness{self.myID}.txt"
    #     while not os.path.exists(fitnessFileName):
    #         time.sleep(0.01)
    #     f = open(fitnessFileName, "r")
    #     self.fitness = float(f.read())
    #     os.system(f"rm {fitnessFileName}")
        # print(f"fitness of solution {self.myID}: {self.fitness}")

    # def Mutate(self):
    #     randomRow = random.randint(0, 2)
    #     randomCol = random.randint(0, 1)
    #     self.weights[randomRow][randomCol] = random.random() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        randomSize = np.random.random_sample((3,))+.1
        pyrosim.Send_Cube(name="Link0", pos=[
                          0, 0, 4], size=randomSize, color="Green" if self.linksWithSensors[0] == 1 else "Cyan")

        for i in range(1, self.randomLinkNum):
            if i == 1:
                pyrosim.Send_Joint(name=f"Link{i-1}_Link{i}", parent=f"Link{i-1}",
                                   child=f"Link{i}", type="revolute", position=[0, randomSize[1]/2, 4], jointAxis="0 0 1")
            else:
                pyrosim.Send_Joint(name=f"Link{i-1}_Link{i}", parent=f"Link{i-1}",
                                   child=f"Link{i}", type="revolute", position=[0, randomSize[1], 0], jointAxis="0 0 1")

            randomSize = np.random.random_sample((3,))+.1
            pyrosim.Send_Cube(name=f"Link{i}", pos=[
                              0, randomSize[1]/2, 0], size=randomSize, color="Green" if self.linksWithSensors[i] == 1 else "Cyan")

            # create arms
            randomLimbNum = random.randint(0, 4)
            # right arm
            if randomLimbNum > 0:
                print("right arm")
                pyrosim.Send_Joint(name=f"Link{i}_Arm{self.armIndex}", parent=f"Link{i}",
                                   child=f"Arm{self.armIndex}", type="revolute", position=[randomSize[0]/2, randomSize[1]/2, -randomSize[2]/2], jointAxis="0 0 1")
                randomArmSize = np.random.random_sample((3,))+.1
                randomArmSize = [min(randomArmSize[0], randomSize[0]), min(
                    randomArmSize[1], randomSize[1]), randomArmSize[2]]
                pyrosim.Send_Cube(
                    name=f"Arm{self.armIndex}", pos=[randomArmSize[0]/2, 0, -randomArmSize[2]/2], size=randomArmSize)
                self.armIndex += 1

            # right leg
            if randomLimbNum > 2:
                print("right leg")
                pyrosim.Send_Joint(name=f"Arm{self.armIndex-1}_Leg{self.legIndex}", parent=f"Arm{self.armIndex-1}",
                                   child=f"Leg{self.legIndex}", type="revolute", position=[randomArmSize[0]/2, 0, -randomArmSize[2]], jointAxis="0 0 1")
                randomLegSize = np.random.random_sample((3,))+.1
                randomLegSize = [min(randomArmSize[0], randomLegSize[0]), min(
                    randomArmSize[1], randomLegSize[1]), randomLegSize[2]]
                pyrosim.Send_Cube(
                    name=f"Leg{self.legIndex}", pos=[0, 0, -randomLegSize[2]/2], size=randomLegSize)
                self.legIndex += 1

            # left arm
            if randomLimbNum > 1:
                print("left arm")
                pyrosim.Send_Joint(name=f"Link{i}_Arm{self.armIndex}", parent=f"Link{i}",
                                   child=f"Arm{self.armIndex}", type="revolute", position=[-randomSize[0]/2, randomSize[1]/2, -randomSize[2]/2], jointAxis="0 0 1")
                pyrosim.Send_Cube(
                    name=f"Arm{self.armIndex}", pos=[-randomArmSize[0]/2, 0, -randomArmSize[2]/2], size=randomArmSize)
                self.armIndex += 1

            # left leg
            if randomLimbNum > 3:
                print("left leg")
                pyrosim.Send_Joint(name=f"Arm{self.armIndex-1}_Leg{self.legIndex}", parent=f"Arm{self.armIndex-1}",
                                   child=f"Leg{self.legIndex}", type="revolute", position=[-randomArmSize[0]/2, 0, -randomArmSize[2]], jointAxis="0 0 1")
                # randomLegSize = np.random.random_sample((3,))+.1
                # randomLegSize = [min(randomArmSize[0], randomLegSize[0]), min(
                #     randomArmSize[1], randomLegSize[1]), randomLegSize[2]]
                pyrosim.Send_Cube(
                    name=f"Leg{self.legIndex}", pos=[0, 0, -randomLegSize[2]/2], size=randomLegSize)
                self.legIndex += 1
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain.nndf")

        # Sensor Neurons
        sensorCount = 0
        for i in self.linksWithSensors:
            if i == 1:
                pyrosim.Send_Sensor_Neuron(
                    name=sensorCount, linkName=f"Link{i}")
                sensorCount += 1

        # Motor Neurons
        for i in range(self.randomLinkNum-1):
            pyrosim.Send_Motor_Neuron(
                name=sensorCount+i, jointName=f"Link{i}_Link{i+1}")

        # Synapses
        for i in range(sensorCount):
            for j in range(self.randomLinkNum-1):
                pyrosim.Send_Synapse(
                    sourceNeuronName=i, targetNeuronName=sensorCount+j, weight=random.random()*2-1)

        pyrosim.End()
