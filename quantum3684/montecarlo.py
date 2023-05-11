import numpy as np
import networkx as nx
import random
import copy

class BitString:
    """
    Simple class to implement a string of bits
    """
    def __init__(self, N=10):
        """
        Initializes a BitString type. Creates an array of zeros, size N and size of dimensions n_dim
        """
        self.config = np.zeros(N, dtype=int)
        self.N = N
        self.n_dim = 2**self.N

    def flip(self, index):
        """
        Flips a value at a specified index within the Bitstring
        """
        if self.config[index] == -1:
            self.config[index] = 1
        else: 
            self.config[index] = -1

    def set_config(self, conf):
        """
        Transforms a BitString into an array
        """
        if (len(conf) == self.N):
            self.config = np.array(conf)
        else:
            return "spin configuration not set propperly"
    
    def set_int_config(self, integer):
        """
        Given an integer input, it is transformed into an array of size N that represents the binary representation
        """
        binary = '{0:b}'.format(integer)
        self.config = list(binary)
        for x in range(0, self.N - len(self.config)): 
            self.config = ['0'] + self.config
        self.config = list(map(int, self.config))

    def Magnetization(self):
        """
        Solves for the magnetization value of a BitString. Adds 1 for a value of 1 in the array and subtracts 1 for all other cases
        """
        mag = 0
        list_1 = self.config
        for i in list_1:
            if i == 1:
               mag += 1
            else:
                mag -= 1
        return mag 
    
    def initialize(self, M):
        """
        Creates a BitString that has the inputted magnetization value M
        """
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
    """
    Class that performs numerical calculations on BitStrings to determine characteristics such as energy and its average value
    across all configurations
    """
    def __init__(self, J: nx.Graph, mus=0.1):
        """
        Initializes and object of IsingHamiltonian type. 
        Creates a J value, which represents the graphical values from an nx.graph function
        Also creates a mus value from an input mus array that can be called later
        """
        self.J = J
        self.mus = mus

    def energy(self, conf: BitString):
        """
        Calculates the energy value of a Bitstring array by looking at each particle in an array and its neighbors
            -If a value is 1, 1 is added. If a value is not 1, 1 is subtracted. 

            -If a particle has a neighbor in the next index that has the same configuration/value, 1 is added, if they
            are different, 1 is subtracted
            
        Inputs: conf, BitString, Array of particles and their configurations (up/down) that we are observing

        Outputs: Energy, float, Energy value of a particular Bitstring Configuration
        """

        Energy = 0.0
        
        conf.config = list(map(int, conf.config))

        # # 0 = -1, 1 = 1
        for i in conf.config:
            if i == 0:
                conf.config[conf.config.index(i)] = -1

        # We calculate energy based of the list of-1's and 1's
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
        """
        Computes the average value of energy, magnetism, heat capacity, and magnetic susceptibility for
        every configuration of a Bitstring of size N at temperature Temp

        Inputs: conf, BitString, tha array we are evaluating
                Temp, int, the temperature we are observing the Bitstring at

        Outputs: E, Energy, float
                 M, Magnetism, float
                 HC, Heat Capacitym, float
                 MS, Magnetic Susceptibility, float
        """
       
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
        """
        Calculates the probability of observing a BitString at a certain energy/configuration
        Inputs: energy, float, the energy of the configuration we are observing
                Temperature, int, the temperature we are observing the probability at

        Outputs: Probability, float, probability of observing the particular configuration/energy state
        """
        k = 1  #1.38064852 * 10e-23
        probability = np.exp(-energy/(k*Temperature))
        return probability

    def metropolis_montecarlo(self, conf: BitString, T=2, nsweep=8000, nburn=2000):
        """
        Algorithm that is able to efficiently observe and record the values of energy, magnetism, heat capacity, and 
        magnetic susceptability at different temperatures and different accuracies. 

        Inputs: conf, Bitstring, input particle configuration array
                T, int, temperature we are observing particles at
                nsweep, int, number of values we are sweeping over
                nburn, int, number of values we test for

        Outputs: E_array, array, list of all energy values across nsweep and nburn values at temperature T
                M_array, array, list of all magnetism values across nsweep and nburn values at temperature T
                EE_array, array, list of all heat capacity values values across nsweep and nburn values at temperature T
                MM_array, array, list of all magnetic susceptability values across nsweep and nburn values at temperature T
        """
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
        """
        Function that calculates the energy difference between a test case and our input configuration

        Inputs: i, int, the index we are flipping to test a new configuration
                config, Bitstring, initial Bitstring that we compare a new one to

        Outputs: de, float, the difference between the new test configuration and the original inputted one
        """
        de = 0.0
        test = copy.deepcopy(config) 
        test.flip(i)    
        de = self.energy(test) - self.energy(config)

        return de

    def metropolis_sweep(self, config: BitString, Temp:float, nburn):
        """
        Function that checks for energy differences across individual particles for every value of nburn, effectively finding the next
        outcomes and how the configuration effects it

        Inputs: config, Bitstring, input partical configuration array
                Temp, float, temperature we are observing the BitString at
                nburn, int, number of values we sweep over  

        Outputs: config, New particle configuration we observe after sweeping over and finding the energy difference of each configuration
        """
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



