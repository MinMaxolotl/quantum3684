import numpy as np
import math
import networkx as nx

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

    # def flip(self, index):
    #     if self.config[index] == 0:
    #         self.string[index] = 1
    #     else: 
    #         self.string[index] = 0

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
        binary = '{0:b}'.format(integer)
        self.config = list(binary)
        if digits != None:
            for x in range(0, digits - len(self.config)): 
                self.config = ['0'] + self.config
        self.config = list(map(int, self.config))
        #self.config = "".join(self.config)

    def Magnetization(self):
        mag = 0
        list_1 = self.config
        for i in list_1:
            if i == 1:
               mag += 1
            else:
                mag -= 1
        return mag 




class IsingHamiltonian:
    def __init__(self, J =[[()]], mus=0):
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
            if conf.config[i] == conf.config[i+1]:
                Energy = Energy + 1
            else:
                Energy = Energy - 1
        
        if conf.config[0] == conf.config[-1]:
            Energy = Energy + 1
        else:
            Energy = Energy - 1

        Energy = Energy + np.dot(conf.config, self.mus)     

        # # Converts -1 back to 0
        for i in conf.config:
            if i == -1:
                conf.config[conf.config.index(i)] = 0
    


        return Energy

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
        Gibbs_sum = 0

        for i in range(conf.n_dim):
            conf.set_int_config(i, digits=6)
            e = self.energy(conf)
            Gibbs = np.exp(-e/Temp)
            print("This is the config: " + str(conf.config))
            print("This is the energy: " + str(e))
            print("This is the Gibbs: " + str(Gibbs))
            E += e*Gibbs
            print("This is the current E: " + str(E))
            m = BitString.Magnetization(conf)
            M += m*Gibbs
            Gibbs_sum += Gibbs
            
        E = E/Gibbs_sum
        M = M/Gibbs_sum
        HC = 0
        MS = 0

        print(Gibbs_sum)
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
    





