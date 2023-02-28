from motor import MOTOR
from sensor import SENSOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c


class ROBOT:
    def __init__(self, id):
        self.robotId = p.loadURDF(f"body{id}.urdf")
        self.id = id
        self.nn = NEURAL_NETWORK(f"brain{id}.nndf")
        os.system(f"rm brain{id}.nndf")
        os.system(f"rm body{id}.urdf")

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for sensor in self.sensors.values():
            sensor.Get_Value(t)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(
                    neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)

    def Save_Values(self):
        for motor in self.motors.values():
            motor.Save_Values()

    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self):
        # stateOfLinkZero = p.getLinkState(self.robotId, 0)
        basePositionAndOrientation = p.getBasePositionAndOrientation(
            self.robotId)
        # positionOfLinkZero = stateOfLinkZero[0]
        basePosition = basePositionAndOrientation[0]
        # xCoordinateOfLinkZero = positionOfLinkZero[0]
        xCoordinateOfLinkZero = basePosition[1]
        f = open(f"tmp{self.id}.txt", "w")
        f.write(str(xCoordinateOfLinkZero))
        f.close()
        os.system(f"mv tmp{self.id}.txt fitness{self.id}.txt")

        exit()
