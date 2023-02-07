import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c


class SOLUTION:
    def __init__(self, myID) -> None:
        self.weights = np.random.rand(
            c.numSensorNeurons, c.numMotorNeurons) * 2 - 1
        self.myID = myID

    def Set_ID(self, id):
        self.myID = id

    def Start_Simulation(self, directOrGUI="DIRECT"):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python3 simulate.py {directOrGUI} {self.myID} 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = f"fitness{self.myID}.txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        f = open(fitnessFileName, "r")
        self.fitness = float(f.read())
        os.system(f"rm {fitnessFileName}")
        # print(f"fitness of solution {self.myID}: {self.fitness}")

    def Mutate(self):
        randomRow = random.randint(0, 2)
        randomCol = random.randint(0, 1)
        self.weights[randomRow][randomCol] = random.random() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[0, 2, 0.05], size=[
                          8, 1, 0.1], mass=100)
        pyrosim.Send_Cube(name="Box", pos=[0, 3, 0.1], size=[
                          8, 1, .2], mass=100)
        pyrosim.Send_Cube(name="Box", pos=[0, 4, .15], size=[
                          8, 1, .3], mass=100)
        pyrosim.Send_Cube(name="Box", pos=[0, 5, .2], size=[
                          8, 1, .4], mass=100)
        pyrosim.Send_Cube(name="Box", pos=[0, 6, .25], size=[
                          8, 1, .5], mass=100)
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, .5], size=[1, 2, 0.25])

        # Head
        pyrosim.Send_Joint(name="Torso_Head", parent="Torso",
                           child="Head", type="revolute", position=[0, 1, .625], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="Head", pos=[
                          0, 0, .25], size=[0.2, 1, .5], mass=0)

        # Ears
        pyrosim.Send_Joint(name="Head_RightEar", parent="Head",
                           child="RightEar", type="revolute", position=[-.25, -.3, .5], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="RightEar", pos=[
                          0, 0, -.2], size=[0.1, 0.3, .4], mass=0)
        pyrosim.Send_Joint(name="Head_LeftEar", parent="Head",
                           child="LeftEar", type="revolute", position=[.25, -.3, .5], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LeftEar", pos=[
                          0, 0, -.2], size=[0.1, 0.3, .4], mass=0)

        # Tail
        pyrosim.Send_Joint(name="Torso_Tail", parent="Torso",
                           child="Tail", type="revolute", position=[0, -1, .5], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="Tail", pos=[
                          0, -.3, 0], size=[0.2, .6, .2], mass=0)

        # Front Right
        pyrosim.Send_Joint(name="Torso_FrontRightThigh", parent="Torso",
                           child="FrontRightThigh", type="revolute", position=[.5, 1, .5], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontRightThigh", pos=[
                          0, 0, -.25], size=[0.2, .2, .5])

        # Front Left
        pyrosim.Send_Joint(name="Torso_FrontLeftThigh", parent="Torso",
                           child="FrontLeftThigh", type="revolute", position=[.5, -1, .5], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLeftThigh", pos=[
                          0, 0, -.25], size=[0.2, .2, .5])

        # Back Right
        pyrosim.Send_Joint(name="Torso_BackRightThigh", parent="Torso",
                           child="BackRightThigh", type="revolute", position=[-.5, 1, .5], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackRightThigh", pos=[
                          0, 0, -.25], size=[0.2, .2, .5])

        # Back Left
        pyrosim.Send_Joint(name="Torso_BackLeftThigh", parent="Torso",
                           child="BackLeftThigh", type="revolute", position=[-.5, -1, .5], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLeftThigh", pos=[
                          0, 0, -.25], size=[0.2, .2, .5])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        # Sensor Neurons
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="FrontRightThigh")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeftThigh")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="BackRightThigh")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="BackLeftThigh")

        # Motor Neurons
        pyrosim.Send_Motor_Neuron(name=5, jointName="Torso_FrontRightThigh")
        pyrosim.Send_Motor_Neuron(name=6, jointName="Torso_FrontLeftThigh")
        pyrosim.Send_Motor_Neuron(name=7, jointName="Torso_BackRightThigh")
        pyrosim.Send_Motor_Neuron(name=8, jointName="Torso_BackLeftThigh")

        # Synapses
        for i in range(5):
            for j in range(4):
                pyrosim.Send_Synapse(
                    sourceNeuronName=i, targetNeuronName=5+j, weight=self.weights[i][j])

        pyrosim.End()
