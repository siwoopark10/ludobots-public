import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c


class SOLUTION:
    def __init__(self, myID) -> None:
        # self.weights = np.random.rand(
        #     c.numSensorNeurons, c.numMotorNeurons) * 2 - 1
        self.myID = myID
        self.randomLinkNum = random.randint(2, 4)
        self.linkRandomSizes = []
        self.linkLimbsRandomSizes = []
        self.armIndex = 0
        self.legIndex = 0
        self.limbJoints = []
        self.limbSensors = []
        self.linkLimbsWithSensors = []
        self.linksWithSensors = np.random.randint(2, size=self.randomLinkNum)

    def Set_ID(self, id):
        self.myID = id

    def Initialize_Weights(self):
        # Generate random sizes for all links
        linkSize = self._Generate_Random_Sizes(1, 1, 0.3)
        self.linkRandomSizes.append(linkSize)
        sensorProbability = 0.7
        for i in range(self.randomLinkNum-1):

            linkSize = self._Generate_Random_Sizes(1, 1, 0.3)
            self.linkRandomSizes.append(linkSize)
            randomLimbNum = random.randint(0, 2) * 2
            if randomLimbNum == 2:
                self.linkLimbsRandomSizes.append(
                    self._Generate_Random_Sizes(linkSize[0], linkSize[1], 0.5, 1))
            elif randomLimbNum > 2:
                self.linkLimbsRandomSizes.append(
                    self._Generate_Random_Sizes(linkSize[0], linkSize[1], 0.5, 2))
            else:
                self.linkLimbsRandomSizes.append([])

            # Random sensor placement
            self.linkLimbsWithSensors.append(
                [random.random() < sensorProbability for i in range(randomLimbNum)])

        # Synapse Weights
        sensorCount = np.count_nonzero(
            self.linksWithSensors) + sum(element == 1 for row in self.linkLimbsWithSensors for element in row)
        jointCount = self.randomLinkNum + \
            sum(len(row)*2 for row in self.linkLimbsRandomSizes) - 1
        self.weights = np.array(
            [[random.random() * 2-1 for j in range(jointCount)] for i in range(sensorCount)])

    def Start_Simulation(self, directOrGUI="DIRECT"):
        self.armIndex = 0
        self.legIndex = 0
        self.limbJoints = []
        self.limbSensors = []
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python3 simulate.py {directOrGUI} {self.myID} ")

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = f"fitness{self.myID}.txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        f = open(fitnessFileName, "r")
        self.fitness = float(f.read())
        os.system(f"rm {fitnessFileName}")
        print(f"fitness of solution {self.myID}: {self.fitness}")

    def Mutate(self):
        choose_mutation = random.randint(0, 7)
        self.selected_mutation = choose_mutation
        if choose_mutation == 0:
            print('synapse weight')
            try:
                # Change synapse weight
                row, col = tuple(np.random.randint(0, size)
                                 for size in self.weights.shape)
                # print(f'synapse weights from {self.weights[row][col]}')
                self.weights[row][col] = random.random() * 2 - 1
            except:
                print(self.linkRandomSizes)
                print(self.linkLimbsRandomSizes)
                print(self.randomLinkNum)
                print(self.linksWithSensors)
        # print(f'to {self.weights[row][col]}')

        if choose_mutation == 1:
            # change link size
            print('change link size')
            i = random.randint(0, len(self.linkLimbsRandomSizes)-1)
            self.linkRandomSizes[i] = self._Generate_Random_Sizes(1, 1, 0.3)
        if choose_mutation == 2:
            print('change limb size')
            i = random.randint(0, len(self.linkLimbsRandomSizes)-1)
            # print(f'from limb {self.linkLimbsRandomSizes[i]}')
            linkSize = self.linkRandomSizes[i]
            for j in range(len(self.linkLimbsRandomSizes[i])):
                self.linkLimbsRandomSizes[i][j] = self._Generate_Random_Sizes(
                    linkSize[0], linkSize[1], 0.5)
            # print(f'to limb {self.linkLimbsRandomSizes[i]}')

        if choose_mutation == 3:
            # Change Sensor Placement
            print("change link sensor placement")
            i = random.randint(0, len(self.linksWithSensors)-1)

            self.linksWithSensors[i] = random.choices(
                [True, False], [0.7, 0.3])[0]
            self.Calculate_Synapse_Weights()
        if choose_mutation == 4:
            print('changing limb sensor')
            row = random.randint(0, len(self.linkLimbsWithSensors)-1)
            if self.linkLimbsWithSensors[row]:
                col = random.randint(0, len(self.linkLimbsWithSensors[row])-1)
                self.linkLimbsWithSensors[row][col] = random.choices(
                    [True, False], [0.7, 0.3])[0]
            self.Calculate_Synapse_Weights()

        if choose_mutation == 5 and self.randomLinkNum < 6:
            # add link
            print('add link')
            self.randomLinkNum += 1
            self.linkRandomSizes.append(self._Generate_Random_Sizes(1, 1, 0.3))
            self.linksWithSensors = np.append(
                self.linksWithSensors, random.randint(0, 1))
            self.linkLimbsRandomSizes.append([])
            self.linkLimbsWithSensors.append([])
            self.Calculate_Synapse_Weights()
        if choose_mutation == 6 and self.randomLinkNum > 2:
            print('remove link')
            self.randomLinkNum -= 1
            self.linkRandomSizes = self.linkRandomSizes[:-1]
            self.linkLimbsRandomSizes = self.linkLimbsRandomSizes[:-1]
            self.linksWithSensors = self.linksWithSensors[:-1]
            self.linkLimbsWithSensors = self.linkLimbsWithSensors[:-1]
            self.Calculate_Synapse_Weights()

        if choose_mutation == 7:
            # Generate more or fewer limbs
            print('generate limbs')
            i = random.randint(0, len(self.linkLimbsRandomSizes)-1)
            # print(f'from limb {self.linkLimbsRandomSizes[i]}')
            linkSize = self.linkRandomSizes[i-1]
            randomLimbNum = random.randint(0, 2) * 2
            if randomLimbNum == 2:
                self.linkLimbsRandomSizes[i] = self._Generate_Random_Sizes(
                    linkSize[0], linkSize[1], 0.5, 1)
            elif randomLimbNum > 2:
                self.linkLimbsRandomSizes[i] = self._Generate_Random_Sizes(
                    linkSize[0], linkSize[1], 0.5, 2)
            else:
                self.linkLimbsRandomSizes[i] = []
            self.linkLimbsWithSensors[i] = [
                random.random() < 0.75 for i in range(randomLimbNum)]
            # print(f'to {self.linkLimbsRandomSizes[i]}')
            self.Calculate_Synapse_Weights()

    def Calculate_Synapse_Weights(self):
        sensorCount = np.count_nonzero(
            self.linksWithSensors) + sum(element == 1 for row in self.linkLimbsWithSensors for element in row)
        jointCount = self.randomLinkNum + \
            sum(len(row)*2 for row in self.linkLimbsRandomSizes) - 1
        print()
        self.weights = np.array(
            [[random.random() * 2-1 for j in range(jointCount)] for i in range(sensorCount)])

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF(f"body{self.myID}.urdf")

        initialHeight = 2
        randomSize = self.linkRandomSizes[0]
        pyrosim.Send_Cube(name="Link0", pos=[
                          0, 0, initialHeight], size=randomSize, color="Green" if self.linksWithSensors[0] == 1 else "Cyan")
        
        for i in range(1, self.randomLinkNum):
            randomSize = self.linkRandomSizes[i-1]
            if i == 1:
                pyrosim.Send_Joint(name=f"Link{i-1}_Link{i}", parent=f"Link{i-1}",
                                   child=f"Link{i}", type="revolute", position=[0, randomSize[1]/2, initialHeight], jointAxis="1 0 0")
            else:
                pyrosim.Send_Joint(name=f"Link{i-1}_Link{i}", parent=f"Link{i-1}",
                                   child=f"Link{i}", type="revolute", position=[0, randomSize[1], 0], jointAxis="1 0 0")

            randomSize = self.linkRandomSizes[i]
            pyrosim.Send_Cube(name=f"Link{i}", pos=[
                              0, randomSize[1]/2, 0], size=randomSize, color="Green" if self.linksWithSensors[i] == 1 else "Cyan")

            self._Create_Limbs(randomSize, i)
        pyrosim.End()

    def Create_Brain(self):

        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        # Sensor Neurons
        sensorCount = 0
        for i in self.linksWithSensors:
            if i == 1:
                pyrosim.Send_Sensor_Neuron(
                    name=sensorCount, linkName=f"Link{i}")
                sensorCount += 1

        # Sensor Neurons for limbs:
        for linkName in self.limbSensors:
            pyrosim.Send_Sensor_Neuron(
                name=sensorCount, linkName=linkName)
            sensorCount += 1

        # Motor Neurons
        for i in range(self.randomLinkNum-1):
            pyrosim.Send_Motor_Neuron(
                name=sensorCount+i, jointName=f"Link{i}_Link{i+1}")

        for i, limbJoint in enumerate(self.limbJoints):
            pyrosim.Send_Motor_Neuron(
                name=sensorCount+self.randomLinkNum-1+i, jointName=limbJoint)

        # initialize weights
        self.sensorCount = sensorCount

        # Synapses
        # print('compre')
        # print(sensorCount, self.randomLinkNum-1 + len(self.limbJoints))
        # print(self.weights.shape)
        for i in range(sensorCount):
            for j in range(self.randomLinkNum-1 + len(self.limbJoints)):
                pyrosim.Send_Synapse(
                    sourceNeuronName=i, targetNeuronName=sensorCount+j, weight=self.weights[i][j])

        pyrosim.End()

    def _Generate_Random_Sizes(self, x, y, z, length=0):
        if length == 0:
            return [random.random()*x, random.random()*y, random.random()*z]
        else:
            temp = []
            for i in range(length):
                temp.append(
                    [random.random()*x, random.random()*y, random.random()*z])
            return temp

    def _Create_Limbs(self, randomSize, i):
        randomLimbNum = len(self.linkLimbsRandomSizes[i-1]) * 2
        # right arm
        if randomLimbNum > 0:
            # print("right arm")
            pyrosim.Send_Joint(name=f"Link{i}_Arm{self.armIndex}", parent=f"Link{i}",
                               child=f"Arm{self.armIndex}", type="revolute", position=[randomSize[0]/2, randomSize[1]/2, -randomSize[2]/2], jointAxis="1 0 0")

            # store to add motor neurons
            self.limbJoints.append(f"Link{i}_Arm{self.armIndex}")

            randomArmSize = self.linkLimbsRandomSizes[i-1][0]

            isSensorNeuron = self._isSensorIncluded(
                f'Arm{self.armIndex}', i, 0)

            pyrosim.Send_Cube(
                name=f"Arm{self.armIndex}", pos=[randomArmSize[0]/2, 0, 0], size=randomArmSize, color="Green" if isSensorNeuron else "Cyan")
            self.armIndex += 1

        # right leg
        if randomLimbNum > 2:
            # print("right leg")
            pyrosim.Send_Joint(name=f"Arm{self.armIndex-1}_Leg{self.legIndex}", parent=f"Arm{self.armIndex-1}",
                               child=f"Leg{self.legIndex}", type="revolute", position=[randomArmSize[0]/2, 0, -randomArmSize[2]/2], jointAxis="1 0 0")
            self.limbJoints.append(
                f"Arm{self.armIndex-1}_Leg{self.legIndex}")
            randomLegSize = self.linkLimbsRandomSizes[i-1][1]

            isSensorNeuron = self._isSensorIncluded(
                f'Leg{self.legIndex}', i, 2)

            pyrosim.Send_Cube(
                name=f"Leg{self.legIndex}", pos=[0, 0, -randomLegSize[2]/2], size=randomLegSize,  color="Green" if isSensorNeuron else "Cyan")
            self.legIndex += 1

        # left arm
        if randomLimbNum > 1:
            # print("left arm")
            pyrosim.Send_Joint(name=f"Link{i}_Arm{self.armIndex}", parent=f"Link{i}",
                               child=f"Arm{self.armIndex}", type="revolute", position=[-randomSize[0]/2, randomSize[1]/2, -randomSize[2]/2], jointAxis="1 0 0")
            self.limbJoints.append(f"Link{i}_Arm{self.armIndex}")

            isSensorNeuron = self._isSensorIncluded(
                f'Arm{self.armIndex}', i, 1)
            # symmetric arm size
            pyrosim.Send_Cube(
                name=f"Arm{self.armIndex}", pos=[-randomArmSize[0]/2, 0, 0], size=randomArmSize, color="Green" if isSensorNeuron else "Cyan")
            self.armIndex += 1

        # left leg
        if randomLimbNum > 3:
            # print("left leg")
            pyrosim.Send_Joint(name=f"Arm{self.armIndex-1}_Leg{self.legIndex}", parent=f"Arm{self.armIndex-1}",
                               child=f"Leg{self.legIndex}", type="revolute", position=[-randomArmSize[0]/2, 0, -randomArmSize[2]/2], jointAxis="1 0 0")
            self.limbJoints.append(
                f"Arm{self.armIndex-1}_Leg{self.legIndex}")

            isSensorNeuron = self._isSensorIncluded(
                f'Leg{self.legIndex}', i, 3)

            # symmetrical leg size
            pyrosim.Send_Cube(
                name=f"Leg{self.legIndex}", pos=[0, 0, -randomLegSize[2]/2], size=randomLegSize, color="Green" if isSensorNeuron else "Cyan")
            self.legIndex += 1

    def _isSensorIncluded(self, linkName, i, j):
        isSensorIncluded = self.linkLimbsWithSensors[i-1][j]
        if isSensorIncluded:
            self.limbSensors.append(linkName)
        return isSensorIncluded
