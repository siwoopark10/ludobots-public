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
        self.randomLinkNum = random.randint(5, 8)
        self.armIndex = 0
        self.legIndex = 0
        self.limbJoints = []
        self.limbSensors = []
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

        initialHeight = 3.3
        randomSize = np.random.random_sample((3,))+.1
        pyrosim.Send_Cube(name="Link0", pos=[
                          0, 0, initialHeight], size=randomSize, color="Green" if self.linksWithSensors[0] == 1 else "Cyan")

        for i in range(1, self.randomLinkNum):
            if i == 1:
                pyrosim.Send_Joint(name=f"Link{i-1}_Link{i}", parent=f"Link{i-1}",
                                   child=f"Link{i}", type="revolute", position=[0, randomSize[1]/2, initialHeight], jointAxis="0 0 1")
            else:
                pyrosim.Send_Joint(name=f"Link{i-1}_Link{i}", parent=f"Link{i-1}",
                                   child=f"Link{i}", type="revolute", position=[0, randomSize[1], 0], jointAxis="0 0 1")

            randomSize = np.random.random_sample((3,))+.1
            pyrosim.Send_Cube(name=f"Link{i}", pos=[
                              0, randomSize[1]/2, 0], size=randomSize, color="Green" if self.linksWithSensors[i] == 1 else "Cyan")

            self._Create_Limbs(randomSize, i)

        pyrosim.End()

    def _Create_Limbs(self, randomSize, i):
        # create limbs
        randomLimbNum = random.randint(0, 5)

        # right arm
        if randomLimbNum > 0:
            print("right arm")
            pyrosim.Send_Joint(name=f"Link{i}_Arm{self.armIndex}", parent=f"Link{i}",
                               child=f"Arm{self.armIndex}", type="revolute", position=[randomSize[0]/2, randomSize[1]/2, -randomSize[2]/2], jointAxis="0 1 0")

            # store to add motor neurons
            self.limbJoints.append(f"Link{i}_Arm{self.armIndex}")

            randomArmSize = np.random.random_sample((3,))+.1
            randomArmSize = [min(randomArmSize[0], randomSize[0]), min(
                randomArmSize[1], randomSize[1]), randomArmSize[2]]

            isSensorNeuron = self._isSensorIncluded(f'Arm{self.armIndex}')

            pyrosim.Send_Cube(
                name=f"Arm{self.armIndex}", pos=[randomArmSize[0]/2, 0, 0], size=randomArmSize, color="Green" if isSensorNeuron else "Cyan")
            self.armIndex += 1

        # right leg
        if randomLimbNum > 2:
            print("right leg")
            pyrosim.Send_Joint(name=f"Arm{self.armIndex-1}_Leg{self.legIndex}", parent=f"Arm{self.armIndex-1}",
                               child=f"Leg{self.legIndex}", type="revolute", position=[randomArmSize[0]/2, 0, -randomArmSize[2]/2], jointAxis="1 0 0")
            self.limbJoints.append(
                f"Arm{self.armIndex-1}_Leg{self.legIndex}")
            randomLegSize = np.random.random_sample((3,))+.1
            randomLegSize = [min(randomArmSize[0], randomLegSize[0]), min(
                randomArmSize[1], randomLegSize[1]), randomLegSize[2]]

            isSensorNeuron = self._isSensorIncluded(f'Leg{self.legIndex}')

            pyrosim.Send_Cube(
                name=f"Leg{self.legIndex}", pos=[0, 0, -randomLegSize[2]/2], size=randomLegSize,  color="Green" if isSensorNeuron else "Cyan")
            self.legIndex += 1

        # left arm
        if randomLimbNum > 1:
            print("left arm")
            pyrosim.Send_Joint(name=f"Link{i}_Arm{self.armIndex}", parent=f"Link{i}",
                               child=f"Arm{self.armIndex}", type="revolute", position=[-randomSize[0]/2, randomSize[1]/2, -randomSize[2]/2], jointAxis="0 1 0")
            self.limbJoints.append(f"Link{i}_Arm{self.armIndex}")

            isSensorNeuron = self._isSensorIncluded(f'Arm{self.armIndex}')
            # symmetric arm size
            pyrosim.Send_Cube(
                name=f"Arm{self.armIndex}", pos=[-randomArmSize[0]/2, 0, 0], size=randomArmSize, color="Green" if isSensorNeuron else "Cyan")
            self.armIndex += 1

        # left leg
        if randomLimbNum > 3:
            print("left leg")
            pyrosim.Send_Joint(name=f"Arm{self.armIndex-1}_Leg{self.legIndex}", parent=f"Arm{self.armIndex-1}",
                               child=f"Leg{self.legIndex}", type="revolute", position=[-randomArmSize[0]/2, 0, -randomArmSize[2]/2], jointAxis="1 0 0")
            self.limbJoints.append(
                f"Arm{self.armIndex-1}_Leg{self.legIndex}")

            isSensorNeuron = self._isSensorIncluded(f'Leg{self.legIndex}')

            # symmetrical leg size
            pyrosim.Send_Cube(
                name=f"Leg{self.legIndex}", pos=[0, 0, -randomLegSize[2]/2], size=randomLegSize, color="Green" if isSensorNeuron else "Cyan")
            self.legIndex += 1

    def _isSensorIncluded(self, linkName):
        isSensorIncluded = random.randint(0, 1)
        if isSensorIncluded:
            self.limbSensors.append(linkName)
        return isSensorIncluded

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain.nndf")

        # Sensor Neurons
        sensorCount = 0
        for i in self.linksWithSensors:
            if i == 1:
                pyrosim.Send_Sensor_Neuron(
                    name=sensorCount, linkName=f"Link{i}")
                print('sensor neuron: ', sensorCount)
                sensorCount += 1

        # Sensor Neurons for limbs:
        for linkName in self.limbSensors:
            pyrosim.Send_Sensor_Neuron(
                name=sensorCount, linkName=linkName)
            print('sensor neuron for limb: ', sensorCount)
            sensorCount += 1

        # Motor Neurons
        for i in range(self.randomLinkNum-1):
            pyrosim.Send_Motor_Neuron(
                name=sensorCount+i, jointName=f"Link{i}_Link{i+1}")
            print('motor neuron: ', sensorCount+i)

        for i, limbJoint in enumerate(self.limbJoints):
            pyrosim.Send_Motor_Neuron(
                name=sensorCount+self.randomLinkNum-1+i, jointName=limbJoint)
            print('motor neuron for limbs: ',
                  sensorCount-1+self.randomLinkNum+i)

        # Synapses
        for i in range(sensorCount):
            for j in range(self.randomLinkNum-1):
                pyrosim.Send_Synapse(
                    sourceNeuronName=i, targetNeuronName=sensorCount+j, weight=random.random()*2-1)

        pyrosim.End()
