import numpy as np

"""
Basic Class data type demo

    A simple recreation of the VPython Vector datatype

"""


class Vector:  # Data type name
    def __init__(self, x_pos=0, y_pos=0, z_pos=0):  # default parameters
        self.x = x_pos
        self.y = y_pos
        self.z = z_pos

    def __str__(self):      # overload print function
        return '<' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + '>'

    def __add__(self, other):       # overload addition
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):       # overload multiplication
        if type(other) is type(self):   # check if types are equivelent
            return self.x*other.x + self.y*other.y + self.z*other.z     # default to dot product
        elif 'int' in str(type(other)) or 'float' in str(type(other)):
            return Vector(self.x*other, self.y*other, self.z*other)     # if scalar scalar multiply

    def __sub__(self, other):       # Overload subtraction
        return Vector(self.x-other.x, self.y-other.y, self.z-other.z)

    def __radd__(self, other):      # Overload reverse addtion
        return self + other

    def __rmul__(self, other):      # overload reverse multiplication
        return self*other

    def __rsub__(self, other):      # overload reverse subtraction
        return self-other

    def __abs__(self):              # overload absolute value
        return np.sqrt((self.x**2) + (self.y**2) + (self.z**2))

    def cx(self): return float(self.x)      # get x coord

    def cy(self): return float(self.y)      # get y coord

    def cz(self): return float(self.z)      # get z coord

    def __eq__(self, other):                # overload equality test
        if isinstance(other, self.__class__):       # check is types are equivilent
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):                # overload inequality test
        return not self.__eq__(other)

    def cross(self, other):     # Corss product
        return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y-other.x)

    def dot(self, other):       # dot product
        return self.x*other.x + self.y*other.y + self.z*other.z

if __name__=='__main__':
    a = Vector(3, 4, 5)
    b = Vector(1, 2, 3)
    c = Vector(1, 2, 3)
    print a, b
    print a+b
    print a-b
    print b*a
    print b*6
    print abs(b)
    print a.cx()
    print a == b
    print a != b
    print c == b
    print c != b
    print a.cross(b)
    print a.dot(b)