import pybullet as p
import numpy as np
import pyrosim.pyrosim as pyrosim

class SENSOR:
    def __init__(self, linkName) -> None:
        self.linkName = linkName
        self.values = np.zeros(1000)

    def Get_Value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

    def Save_Values(self):
        np.save(f"data/{self.linkName}Values.npy",self.values)

