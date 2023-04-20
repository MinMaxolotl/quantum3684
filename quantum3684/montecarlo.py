from functions import BitString
from functions import energy
import numpy as np
import math

def Gibbs(a: BitString, Temperature: int):
    k = 1.38064852 * 10^-23
    E = energy(a)
    exponential = -E/(k*Temperature)
    probability = (math.e)^exponential

    return probability

class IsingHamiltonian:
    def __init__(self, J = list[list[tuple]], mus=np.zeros(1)):
        self.J = J
        self.mus = mus

        # self.points = []
        # self.strength = []

        # for i in range(len(self.J)):
        #     self.points = list(int(np.zeros(len(self.J[i]))))
        #     self.strength = list(np.zeros(len(self.J[i])))
        #     for 



