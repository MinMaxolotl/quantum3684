Author: Maxwell Kawada
Last Updated: 5-10-2023
Topic File : montecarlo.py

Classes:
  - BitString
    - The BitString class contains all of the funcions used to modify and configure an array of integers that repesent the orientaton of a set of particles.
    - As it is initialized, it creates three pieces of data: 
        1) Initial configuration: an array of zeros of specified length
        2) N: The number of particles in the array
        3) N_dim: The dimensional size of the initialized array, used to create arrays of other configurations
    - Functions: 
        flip: Swaps a -1 to a 1 at a certain index of a BitString array
        set_config: Creates a numpy array of the BitString configuration
        set_int_config: Creates a numpy array from a specified integer input
        Magnetization: Determines the magnetization of the Bitstring, +1 for a index that is 1, -1 for else. Sums these values
        initialize: Returns a configuration of a Bitstring that has the magnetism specified with the input M

  - IsingHamiltonian
    - The IsingHamiltonian class contains the more computationally heavy functions that allow us to analyze a set of particles given by the BitString class
    - As it is initialized, it creates two pieces of data:
      1) J: Represents the nx.graph value produced and is a list of tuples that contain the interactions between the particles
      2) mus: These are the mu values that help define the energy of a system and are representitive of the spin/configuration of the particles.
    - Functions:

        energy: Calculates the energy value of a BitString by analyzing the relationships and postions between each particle and the mu values
        compute_average_values: Takes in a bitstring and a temperature value and calculates the average values of a BitString of size N at a certain temperature
                                (Temp). Calulates average energy, magnetization, heat capacity, and magnetic susceptibility. 
        Gibbs: An unused function that calculates the probablilty of a certain configuration from occuring by taking in an energy and temperature input
        metropolis_montecarlo: Performs an algorith that efficiently determines values calculated in "compute_average_values" across many steps given a Bitstring
                               temperature, nsweep, and nburn value. 
        metropolis_sweep: "Sweeps" over every nburn value for each particle to quickly and psuedo-randomly select each following configuration and energy
                          Has a Bitstring, temperature, and nburn input.
        e_flip: Determines the difference in energy between a test case Bitstring and the inputted Bitstring

Purpose: This is used to efficiently use sorting algotithms that can determine the quantum relationships between particles over different configurations, 
         temperatures, weights, and system sizes. 