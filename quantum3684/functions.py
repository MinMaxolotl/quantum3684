import numpy as np
import networkx as nx

"""Provide the primary functions."""

def canvas(with_attribution=True):
    """
    Placeholder function to show example docstring (NumPy format).

    Replace this function and doc string for your own project.

    Parameters
    ----------
    with_attribution : bool, Optional, default: True
        Set whether or not to display who the quote is from.

    Returns
    -------
    quote : str
        Compiled string including quote and optional attribution.
    """

    quote = "The code is but a canvas to our imagination."
    if with_attribution:
        quote += "\n\t- Adapted from Henry David Thoreau"
    return quote


if __name__ == "__main__":
    # Do something if this file is invoked on its own
    print(canvas())

def zen(with_attribution=True):
    quote = """Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!"""

    if with_attribution:
      quote += "\n\tTim Peters"

    return quote



class BitString:
    """
    Simple class to implement a string of bits
    """
    def __init__(self, N=10):
        self.config = np.zeros(N, dtype=int)
        self.N = N


    def __str__(self):
        value = ""
        for val in self.string:
            value += str(val)
        return value 

    def flip(self, index):
        if self.string[index] == 0:
            self.string[index] = 1
        else: 
            self.string[index] = 0

    def __len__(self):
        x = len(self.string)
        return x

    def set_string(self, newstring):
        self.string = newstring

    def on(self):
        z = sum(self.string)
        return z

    def off(self):
        w = sum(self.string)
        zeros = len(self.string) - w
        return zeros

    def int(self):
        sum = 0
        for i in range(len(self.string)):
            if self.string[len(self.string)-1-i] == 1:
                sum += 2**i
            if self.string[len(self.string)-1-i] == '1':
                sum += 2**i
        return sum

    def set_int(self, integer, digits=None):
        binary = '{0:b}'.format(integer)
        self.string = list(binary)
        if digits != None:
            for x in range(0, digits - len(self.string)): 
                self.string = ['0'] + self.string
        self.string = list(map(int, self.string))
        #self.string = "".join(self.string)

    def __eq__(self, other):
        if isinstance(other, BitString):


            if self.string == other.string:
                print("These are the same")

            else:
                print("These are not the same")




def energy(bs: BitString, G: nx.Graph):
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
    Energy = 0
    bs.string = list(map(int, bs.string))

    # 0 = -1, 1 = 1
    for i in bs.string:
        if i == 0:
            bs.string[bs.string.index(i)] = -1

    #print(bs.string)

    
    
    orientation = bs.string  #Says whether it is up or down, list of node values

    #for x in G.edges:
    #    print(x)
    
    #size = bs.__len__

    # We want to multiply the interacting nodes together
    for e in G.edges:
        i_idx = e[0]
        j_idx = e[1]
        si = orientation[i_idx]
        sj = orientation[j_idx]

        sisj = si*sj
        Energy += sisj*(G.edges[e]['weight']) 

    # Converts -1 back to 0
    for i in bs.string:
        if i == -1:
            bs.string[bs.string.index(i)] = 0

    return Energy


# THIS IS AN OLD FILE THAT CONTAINED OLDER VERSIONS OF FUNCTIONS
# USED IN PREVIOUS ASSIGNMENTS