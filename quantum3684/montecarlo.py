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
        print(mag)
        return mag 




class IsingHamiltonian:
    def __init__(self, J = list[list[tuple]], mus=np.zeros(1)):
        self.J = J
        self.mus = mus

    set_int = BitString.int

    def energy(self, conf: BitString):
        """Compute energy of configuration, `bs`

        .. math::
            E = \\left<\\hat{H}\\right>

        Parameters
         ----------
        bs   : Bitstring
        input configuration
         G    : Graph
        input graph defining the Hamiltonian
         Returns
        -------
        energy  : float
        Energy of the input configuration
         """
        Energy = 0.0
        
        conf.config = list(map(int, conf.config))

         # 0 = -1, 1 = 1
        for i in conf.config:
            if i == 0:
                conf.config[conf.config.index(i)] = -1

        print(conf.config)
        #for x in G.edges:
        #    print(x)
    
        #size = config.__len__

        # We calculate energy based of the list of 0's and 1's
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

        print(Energy)
            
        # for j in bs.config:
        #     if j == 1:
        #         MuCoefficient = MuCoefficient + 1
        #     else:
        #         MuCoefficient = MuCoefficient - 1
        
        # print(MuCoefficient)

        Energy = Energy + np.dot(conf.config, self.mus)     

        # Converts -1 back to 0
        for i in conf.config:
            if i == -1:
                conf.config[conf.config.index(i)] = 0

        return Energy
    
    def compute_average_values(self, conf: BitString, Temp: int):
        
        print(conf)
        e = self.energy(conf)
        avg_e = e*self.Gibbs(conf, Temp)
        print(avg_e)
        m = BitString.Magnetization(conf)
        avg_m = m*self.Gibbs(conf, Temp)
        print(avg_m)

        return avg_e, avg_m
    

    def Gibbs(self, conf: BitString, Temperature: int):
        k = 1  #1.38064852 * 10e-23
        eng = self.energy(conf)
        exponential = -eng/(k*Temperature)
        probability = (math.e)**exponential
        return probability
    # Create a loop that does this for each kind of configuration
    # 
    #Compute energy of each congifuration, multiply each of them by gibbs and add
    #divide by sum of gibbs
    #Put my own ising notebook into examples.
    





