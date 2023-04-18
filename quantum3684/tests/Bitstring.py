
class BitString:
    """
    Simple class to implement a string of bits
    """
    def __init__(self, string):
        self.string = string

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