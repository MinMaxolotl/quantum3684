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

    # def __len__(self):
    #     x = len(self.string)
    #     return x

    # def set_string(self, newstring):
    #     self.string = newstring

    # def on(self):
    #     z = sum(self.string)
    #     return z

    # def off(self):
    #     w = sum(self.string)
    #     zeros = len(self.string) - w
    #     return zeros

    def int(self):
        sum = 0
        for i in range(len(self.config)):
            if self.config[len(self.config)-1-i] == 1:
                sum += 2**i
            if self.config[len(self.config)-1-i] == '1':
                sum += 2**i
        return sum

    def set_int(self, integer, digits=None):
        binary = '{0:b}'.format(integer)
        self.config = list(binary)
        if digits != None:
            for x in range(0, digits - len(self.config)): 
                self.config = ['0'] + self.config
        self.config = list(map(int, self.config))
        #self.config = "".join(self.config)

    def __eq__(self, other):
        if isinstance(other, BitString):


            if self.config == other.config:
                print("These are the same")

            else:
                print("These are not the same")

    def set_config(self, conf):
        if (len(conf) == self.N):
            self.config = np.array(conf)
        else:
            return "spin configuration not set propperly"
    
    def set_int_config(self, integer, digits=None):
        # binary = '{0:b}'.format(integer)
        # self.config = list(binary)
        # if digits != None:
        #     for x in range(0, digits - len(self.config)): 
        #         self.config = ['0'] + self.config
        # self.config = list(map(int, self.config))
        # #self.config = "".join(self.config)
        self.config = np.array([int(i) for i in np.binary_repr(integer, width=self.N)])
        

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
        MagArray = np.zeros(self.N, dtype=int)

        s = -1

        for i in range(len(MagArray)):
            if i < M:
                MagArray[i] = 1
            else:
                MagArray[i] = s
                s = s*-1
        
        print(MagArray)

                



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

        # if conf.config[0] == conf.config[-1]:
        #     Energy += self.J[-1]
        # else:
        #     Energy -= self.J[-1]
        Energy += np.dot(self.mus, conf.config)
        
        return Energy   

        # # # Converts -1 back to 0
        # for i in conf.config:
        #     if i == -1:
        #         conf.config[conf.config.index(i)] = 0
    


        # return Energy

        # Energy = 0
        # for i in range(conf.N):
        #     for j in self.J[i]:
        #         if j[0] < 1:
        #             continue
        #         if conf.config[i] == conf.config[j[0]]:
        #             Energy = Energy + j[1]
        #         else:
        #             Energy = Energy - j[1]

        # Energy += np.dot(self.mus, 2*conf.config-1)

        # return Energy
        

        # Energy = 0
        # BitString.string = list(map(int, BitString.string))

        #  # 0 = -1, 1 = 1
        # for i in BitString.string:
        #     if i == 0:
        #         BitString.string[BitString.string.index(i)] = -1

        # #print(BitString.string)

    
    
        # orientation = BitString.string  #Says whether it is up or down, list of node values

        # #for x in G.edges:
        # #    print(x)
        
        # #size = BitString.__len__

        # # We want to multiply the interacting nodes together
        # for e in G.edges:
        #     i_idx = e[0]
        #     j_idx = e[1]
        #     si = orientation[i_idx]
        #     sj = orientation[j_idx]

        #     sisj = si*sj
        #     Energy += sisj*(G.edges[e]['weight']) 

        # # Converts -1 back to 0
        # for i in BitString.string:
        #     if i == -1:
        #         BitString.string[BitString.string.index(i)] = 0

        # return Energy + np.dot(conf.config, self.mus)


    
    def compute_average_values(self, conf: BitString, Temp: int):
       
        # E  = 0.0
        # M  = 0.0
        # Z  = 0.0
        # EE = 0.0
        # MM = 0.0

        # for i in range(conf.n_dim):
        #     conf.set_int_config(i, digits=6)
        #     Ei = self.energy(conf)
        #     Zi = np.exp(-Ei/Temp)
        #     E += Ei*Zi
        #     EE += Ei*Ei*Zi
        #     Mi = BitString.Magnetization(conf)
        #     M += Mi*Zi
        #     MM += Mi*Mi*Zi
        #     Z += Zi
        
        # E = E/Z
        # M = M/Z
        # EE = EE/Z
        # MM = MM/Z
        
        # HC = (EE - E*E)/(Temp*Temp)
        # MS = (MM - M*M)/Temp
        # return E, M, HC, MS
       
       
        E = 0
        M = 0
        E_2 = 0
        M_2 = 0
        Gibbs_sum = 0

        for i in range(conf.n_dim):
            conf.set_int_config(i)
            eng = self.energy(conf)
            Gibbs = np.exp(-(eng/Temp))
            print("This is the config: " + str(conf.config))
            print("This is the energy: " + str(eng))
            print("This is the Gibbs: " + str(Gibbs))
            E += eng*Gibbs
            E_2 += eng*eng*Gibbs
            #print("This is the current E: " + str(E))
            m = BitString.Magnetization(conf)
            #print("spin sum: " + str(m))
            #print("Gibbs at i: " + str(Gibbs))
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

        #print(M)

        return E, M, HC, MS
    

    def Gibbs(self, energy, Temperature: int):
        k = 1  #1.38064852 * 10e-23
        probability = np.exp(-energy/(k*Temperature))
        return probability


    # Create a loop that does this for each kind of configuration
    # 
    #Compute energy of each congifuration, multiply each of them by gibbs and add
    #divide by sum of gibbs
    #Put my own ising notebook into examples.

    def metropolis_montecarlo(ham, conf: BitString, T=2, nsweep=8000, nburn=2000):
        conf = ham.metropolis_sweep(conf, T, nburn)
        E_array = M_array = EE_array = MM_array = np.zeros(nsweep)
         
        for i in range(nsweep):
            ham.metropolis_sweep(conf, T, nburn)
            E_i = ham.energy(conf)
            E_array[i] = (E_array[i-1] * i + E_i) / (i+1)
            EE_array[i] = (EE_array[i-1] * i + (E_i**2)) / (i+1)
            M_i = BitString.Magnetization(conf)
            M_array[i] = (M_array[i-1] * i + M_i) / (i+1)
            MM_array[i] = (MM_array[i-1] * i + (M_i**2)) / (i+1)

        # ham.metropolis_sweep(conf, T nburn)
        # Energy = ham.energy(conf)
        # Magnetization = BitString.Magnetization(conf)
        # E_array[0] = Energy
        # M_array[0] = Magnetization
        # EE_array[0] = Energy*Energy
        # MM_array[0] = Magnetization*Magnetization

        # for i in range(1, nsweep):
        #     ham.metropolis_sweep(conf, T, nburn)
        #     Energy = ham.energy(conf)
        #     Magnetization = BitString.Magnetization(conf)
        #     E_array[i] = ((E_array[i-1]*i) + Energy)/(i+1)
        #     EE_array[i] = ((EE_array[i-1]*i) + Energy*Energy)/(i+1)
        #     M_array[i] = ((M_array[i-1]*i) + Magnetization)/(i+1)
        #     MM_array[i] = ((MM_array[i-1]*i) + Magnetization*Magnetization)/(i+1)
    
        return E_array, M_array, EE_array, MM_array


    def e_flip(self, i: int, config: BitString):
        test = copy.deepcopy(config)
        test.flip(i)
        de = self.energy(test) - self.energy(config)

        return test, de

    def metropolis_sweep(self, config: BitString, Temp:float, nburn):
        for i in range(nburn):
            for j in range(config.N):
                de = self.e_flip(j, config)[1]
                Wa_b = np.exp(-(de/Temp))
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



