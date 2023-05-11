import numpy as np
import math
import networkx as nx
import matplotlib as mpl
from matplotlib import pyplot as plt
import random
import scipy
import copy

class BitString:
    """
    Simple class to implement a string of bits
    """
    def __init__(self, N=10):
        self.config = np.zeros(N, dtype=int)
        self.N = N
        self.n_dim = 2**self.N
        
    def __str__(self):
        value = ""
        for val in self.config:
            value += str(val)
        return value 

    def flip(self, index):
        if self.config[index] == -1:
            self.config[index] = 1
        else: 
            self.config[index] = -1

    def set_config(self, conf):
        if (len(conf) == self.N):
            self.config = np.array(conf)
        else:
            return "spin configuration not set propperly"
    
    def set_int_config(self, integer):
        binary = '{0:b}'.format(integer)
        self.config = list(binary)
        for x in range(0, self.N - len(self.config)): 
            self.config = ['0'] + self.config
        self.config = list(map(int, self.config))

    def Magnetization(self):
        mag = 0
        list_1 = self.config
        for i in list_1:
            if i == 1:
               mag += 1
            else:
                mag -= 1
        return mag 
    
    def initialize(self, M):
        self.M = M
        self.config = np.zeros(self.N, dtype=int)

        s = -1

        for i in range(len(self.config)):
            if i < M:
                self.config[i] = 1
            else:
                self.config[i] = s
                s = s*-1
        
        return self.config
       

class IsingHamiltonian:
    def __init__(self, J: nx.Graph, mus=0.1):
        self.J = J
        self.mus = mus

    def energy(self, conf: BitString):

        Energy = 0.0
        
        conf.config = list(map(int, conf.config))

        # # 0 = -1, 1 = 1
        for i in conf.config:
            if i == 0:
                conf.config[conf.config.index(i)] = -1

        # # We calculate energy based of the list of 0's and 1's
        #for i in range(config.N):
        for i in range(len(conf.config)-1):  
            for j in self.J[i]: 
                if j[0] > i:    
                    if conf.config[i] == conf.config[j[0]]:
                        Energy += j[1]
                    else:
                        Energy -= j[1]

        Energy += np.dot(self.mus, conf.config)
        
        return Energy   

    def compute_average_values(self, conf: BitString, Temp: int):
       
        E = 0
        M = 0
        E_2 = 0
        M_2 = 0
        Gibbs_sum = 0

        for i in range(conf.n_dim):
            conf.set_int_config(i)
            eng = self.energy(conf)
            Gibbs = np.exp(-(eng/Temp))
            E += eng*Gibbs
            E_2 += eng*eng*Gibbs
            m = BitString.Magnetization(conf)
            M += m*Gibbs
            M_2 += m*m*Gibbs
            Gibbs_sum += Gibbs
        
        E = E/Gibbs_sum
        HC_1 = E_2/Gibbs_sum
        EE = E*E
        M = M/Gibbs_sum
        MS_1 = M_2/Gibbs_sum
        MM = M*M
        HC = (HC_1 - EE)/(Temp**2)
        MS = (MS_1 - MM)/(Temp)


        return E, M, HC, MS
    
    def Gibbs(self, energy, Temperature: int):
        k = 1  #1.38064852 * 10e-23
        probability = np.exp(-energy/(k*Temperature))
        return probability

    def metropolis_montecarlo(self, conf: BitString, T=2, nsweep=8000, nburn=2000):
        conf = self.metropolis_sweep(conf, T, nburn)
        E_array = np.zeros(nsweep)
        M_array = np.zeros(nsweep)
        EE_array = np.zeros(nsweep)
        MM_array = np.zeros(nsweep)

        for i in range(1, nsweep):
            conf = self.metropolis_sweep(conf, T, nburn=1)
            E_i = self.energy(conf)
            M_i = BitString.Magnetization(conf)

            E_array[i] = (E_array[i-1] * i + E_i) / (i+1)
            EE_array[i] = (EE_array[i-1] * i + (E_i**2)) / (i+1)
            
            M_array[i] = (M_array[i-1] * i + M_i) / (i+1)
            MM_array[i] = (MM_array[i-1] * i + (M_i**2)) / (i+1)

        return E_array, M_array, EE_array, MM_array

    def e_flip(self, i: int, config: BitString):
        de = 0.0
        test = copy.deepcopy(config) 
        test.flip(i)    
        de = self.energy(test) - self.energy(config)

        return de

    def metropolis_sweep(self, config: BitString, Temp:float, nburn):
        for i in range(nburn):
            for j in range(config.N):
                de = self.e_flip(j, config)
                Wa_b = np.exp(-de/Temp)
                accept = True

                if (de > 0):
                    r = random.random()

                    if r > Wa_b:
                        accept = False

                if (accept == True):
                    config.flip(j)

                else:
                    pass    

        return config



