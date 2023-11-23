import math

class Vector2D:
    def __init__(self, x, y):
        self.vec = (x, y)

    def __add__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector2D(self.vec[0] + other, self.vec[1] + other)
        elif type(other) == tuple or type(other) == list:
            res = Vector2D(self.vec[0] + other[0], self.vec[1] + other[1])
        elif type(other) == Vector2D:
            res = Vector2D(self.vec[0] + other.vec[0], self.vec[1] + other.vec[1])
        return res

    def __sub__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector2D(self.vec[0] - other, self.vec[1] - other)
        elif type(other) == tuple or type(other) == list:
            res = Vector2D(self.vec[0] - other[0], self.vec[1] - other[1])
        elif type(other) == Vector2D:
            res = Vector2D(self.vec[0] - other.vec[0], self.vec[1] - other.vec[1])
        return res

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector2D(self.vec[0] * other, self.vec[1] * other)
        elif type(other) == tuple or type(other) == list:
            res = Vector2D(self.vec[0] * other[0], self.vec[1] * other[1])
        elif type(other) == Vector2D:
            res = Vector2D(self.vec[0] * other.vec[0], self.vec[1] * other.vec[1])
        return res

    def __truediv__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector2D(self.vec[0] / other, self.vec[1] / other)
        elif type(other) == tuple or type(other) == list:
            res = Vector2D(self.vec[0] / other[0], self.vec[1] / other[1])
        elif type(other) == Vector2D:
            res = Vector2D(self.vec[0] / other.vec[0], self.vec[1] / other.vec[1])
        return res

    def __iadd__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector2D(self.vec[0] + other, self.vec[1] + other)
        elif type(other) == tuple or type(other) == list:
            res = Vector2D(self.vec[0] + other[0], self.vec[1] + other[1])
        elif type(other) == Vector2D:
            res = Vector2D(self.vec[0] + other.vec[0], self.vec[1] + other.vec[1])
        
        if res != None:
            self.vec = res.vec
        return res

    def __isub__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector2D(self.vec[0] - other, self.vec[1] - other)
        elif type(other) == tuple or type(other) == list:
            res = Vector2D(self.vec[0] - other[0], self.vec[1] - other[1])
        elif type(other) == Vector2D:
            res = Vector2D(self.vec[0] - other.vec[0], self.vec[1] - other.vec[1])
        
        if res != None:
            self.vec = res.vec
        return res

    def __imul__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector2D(self.vec[0] * other, self.vec[1] * other)
        elif type(other) == tuple or type(other) == list:
            res = Vector2D(self.vec[0] * other[0], self.vec[1] * other[1])
        elif type(other) == Vector2D:
            res = Vector2D(self.vec[0] * other.vec[0], self.vec[1] * other.vec[1])
        
        if res != None:
            self.vec = res.vec
        return res

    def __itruediv__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector2D(self.vec[0] / other, self.vec[1] / other)
        elif type(other) == tuple or type(other) == list:
            res = Vector2D(self.vec[0] / other[0], self.vec[1] / other[1])
        elif type(other) == Vector2D:
            res = Vector2D(self.vec[0] / other.vec[0], self.vec[1] / other.vec[1])
        
        if res != None:

            self = res
        return res

    def len(self):
        return math.sqrt(self.vec[0]**2+self.vec[1]**2)

    def Normalise(self):
        l = self.len()
        if l == 0:
            return Vector2D(0, 0)
        return Vector2D(self.vec[0]/l, self.vec[1]/l)

    def dot(self, otherVec):
        if type(otherVec) == tuple or type(otherVec) == list:
            return self.vec[0] * otherVec[0] + self.vec[1] * otherVec[1]
        if type(otherVec) == Vector2D:
            return self.vec[0] * otherVec.vec[0] + self.vec[1] * otherVec.vec[1]

    def __tuple__(self):
        return self.vec

    def __round__(self):
        return Vector2D(round(self.vec[0]), round(self.vec[1]))
    
    def __str__(self):
        return f"vector2D: {self.vec}"

    def __ne__(self, other):
        if type(other) == tuple or type(other) == list:
            if self.vec[0] != other[0] and self.vec[1] != other[1]:
                return True
        elif type(other) == Vector2D:
            if self.vec[0] != other.vec[0] and self.vec[1] != other.vec[1]:
                return True
        elif type(other) == Vector3D:
            if self.vec[0] != other.vec[0] and self.vec[1] != other.vec[1]:
                return True
        return False

    def __eq__(self, other):
        if type(other) == tuple or type(other) == list:
            if self.vec[0] == other[0] and self.vec[1] == other[1]:
                return True
        elif type(other) == Vector2D:
            if self.vec[0] == other.vec[0] and self.vec[1] == other.vec[1]:
                return True
        elif type(other) == Vector3D:
            if self.vec[0] == other.vec[0] and self.vec[1] == other.vec[1]:
                return True
        return False

    def __lt__(self, other):
        if type(other) == tuple or type(other) == list:
            if self.vec[0] < other[0] and self.vec[1] < other[1]:
                return True
        elif type(other) == Vector2D:
            if self.vec[0] < other.vec[0] and self.vec[1] < other.vec[1]:
                return True
        elif type(other) == Vector3D:
            if self.vec[0] < other.vec[0] and self.vec[1] < other.vec[1]:
                return True
        return False

    def __gt__(self, other):
        if type(other) == tuple or type(other) == list:
            if self.vec[0] > other[0] and self.vec[1] > other[1]:
                return True
        elif type(other) == Vector2D:
            if self.vec[0] > other.vec[0] and self.vec[1] > other.vec[1]:
                return True
        elif type(other) == Vector3D:
            if self.vec[0] > other.vec[0] and self.vec[1] > other.vec[1]:
                return True
        return False

    def __le__(self, other):
        if type(other) == tuple or type(other) == list:
            if self.vec[0] <= other[0] and self.vec[1] <= other[1]:
                return True
        elif type(other) == Vector2D:
            if self.vec[0] <= other.vec[0] and self.vec[1] <= other.vec[1]:
                return True
        elif type(other) == Vector3D:
            if self.vec[0] <= other.vec[0] and self.vec[1] <= other.vec[1]:
                return True
        return False

    def __ge__(self, other):
        if type(other) == tuple or type(other) == list:
            if self.vec[0] >= other[0] and self.vec[1] >= other[1]:
                return True
        elif type(other) == Vector2D:
            if self.vec[0] >= other.vec[0] and self.vec[1] >= other.vec[1]:
                return True
        elif type(other) == Vector3D:
            if self.vec[0] >= other.vec[0] and self.vec[1] >= other.vec[1]:
                return True
        return False

    def toJSON(self):
        return self.vec

    def fromJSON(self, data):
        self.vec = data


    def __neg__(self):
        return Vector2D(-self.vec[0], -self.vec[1])




class Vector3D:
    def __init__(self, x, y, z):
        self.vec = (x, y, z)

    def __add__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector3D(self.vec[0] + other, self.vec[1] + other, self.vec[2] + other)
        elif type(other) == tuple or type(other) == list:
            res = Vector3D(self.vec[0] + other[0], self.vec[1] + other[1], self.vec[2] + other[2])
        elif type(other) == Vector3D:
            res = Vector3D(self.vec[0] + other.vec[0], self.vec[1] + other.vec[1], self.vec[2] + other.vec[2])
        return res

    def __sub__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector3D(self.vec[0] - other, self.vec[1] - other, self.vec[2] - other)
        elif type(other) == tuple or type(other) == list:
            res = Vector3D(self.vec[0] - other[0], self.vec[1] - other[1], self.vec[2] - other[2])
        elif type(other) == Vector3D:
            res = Vector3D(self.vec[0] - other.vec[0], self.vec[1] - other.vec[1], self.vec[2] - other.vec[2])
        return res

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector3D(self.vec[0] * other, self.vec[1] * other, self.vec[2] * other)
        elif type(other) == tuple or type(other) == list:
            res = Vector3D(self.vec[0] * other[0], self.vec[1] * other[1], self.vec[2] * other[2])
        elif type(other) == Vector3D:
            res = Vector3D(self.vec[0] * other.vec[0], self.vec[1] * other.vec[1], self.vec[2] * other.vec[2])
        return res

    def __truediv__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector3D(self.vec[0] / other, self.vec[1] / other, self.vec[2] / other)
        elif type(other) == tuple or type(other) == list:
            res = Vector3D(self.vec[0] / other[0], self.vec[1] / other[1], self.vec[2] / other[2])
        elif type(other) == Vector3D:
            res = Vector3D(self.vec[0] / other.vec[0], self.vec[1] / other.vec[1], self.vec[2] / other.vec[2])
        return res

    def __iadd__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector3D(self.vec[0] + other, self.vec[1] + other, self.vec[2] + other)
        elif type(other) == tuple or type(other) == list:
            res = Vector3D(self.vec[0] + other[0], self.vec[1] + other[1], self.vec[2] + other[2])
        elif type(other) == Vector3D:
            res = Vector3D(self.vec[0] + other.vec[0], self.vec[1] + other.vec[1], self.vec[2] + other.vec[2])
        return res
        
        if res != None:
            self.vec = res.vec
        return res

    def __isub__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector3D(self.vec[0] - other, self.vec[1] - other, self.vec[2] - other)
        elif type(other) == tuple or type(other) == list:
            res = Vector3D(self.vec[0] - other[0], self.vec[1] - other[1], self.vec[2] - other[2])
        elif type(other) == Vector3D:
            res = Vector3D(self.vec[0] - other.vec[0], self.vec[1] - other.vec[1], self.vec[2] - other.vec[2])
        return res
        
        if res != None:
            self.vec = res.vec
        return res

    def __imul__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector3D(self.vec[0] * other, self.vec[1] * other, self.vec[2] * other)
        elif type(other) == tuple or type(other) == list:
            res = Vector3D(self.vec[0] * other[0], self.vec[1] * other[1], self.vec[2] * other[2])
        elif type(other) == Vector3D:
            res = Vector3D(self.vec[0] * other.vec[0], self.vec[1] * other.vec[1], self.vec[2] * other.vec[2])
        return res
        
        if res != None:
            self.vec = res.vec
        return res

    def __itruediv__(self, other):
        if type(other) == int or type(other) == float:
            res = Vector3D(self.vec[0] / other, self.vec[1] / other, self.vec[2] / other)
        elif type(other) == tuple or type(other) == list:
            res = Vector3D(self.vec[0] / other[0], self.vec[1] / other[1], self.vec[2] / other[2])
        elif type(other) == Vector3D:
            res = Vector3D(self.vec[0] / other.vec[0], self.vec[1] / other.vec[1], self.vec[2] / other.vec[2])
        return res
        
        if res != None:

            self = res
        return res

    def len(self):
        return math.sqrt(self.vec[0]**2+self.vec[1]**2+self.vec[2]**2)

    def Normalise(self):
        l = self.len()
        if l == 0:
            return Vector3D(0, 0, 0)
        return Vector3D(self.vec[0]/l, self.vec[1]/l, self.vec[2]/l)

    def dot(self, otherVec):
        if type(otherVec) == tuple or type(otherVec) == list:
            return self.vec[0] * otherVec[0] + self.vec[1] * otherVec[1] + self.vec[2] * otherVec[2]
        if type(otherVec) == Vector3D:
            return self.vec[0] * otherVec.vec[0] + self.vec[1] * otherVec.vec[1] + self.vec[2] * otherVec.vec[2]
    
    def __str__(self):
        return f"vector3D: {self.vec}"

    def __ne__(self, other):
        if type(other) == tuple or type(other) == list:
            if self.vec[0] != other[0] and self.vec[1] != other[1] and self.vec[2] != other[2]:
                return True
        elif type(other) == Vector3D:
            if self.vec[0] != other.vec[0] and self.vec[1] != other.vec[1] and self.vec[2] != other.vec[2]:
                return True
        return False
    
    def __neg__(self):
        return Vector3D(-self.vec[0], -self.vec[1], -self.vec[2])

    def __getitem__(self, key):
        return self.vec[key]

    def __setitem__(self, key, item):
        if key == 0:
            self.vec = (item, self.vec[1], self.vec[2])
        elif key == 1:
            self.vec = (self.vec[0], item, self.vec[2])
        elif key == 2:
            self.vec = (self.vec[0], self.vec[1], item)
        else:
            raise IndexError(self, key)

def cross(v_A: Vector3D, v_B: Vector3D):
    c_P = Vector3D(0, 0, 0)
    c_P[0] = v_A.vec[1] * v_B.vec[2] - v_A.vec[2] * v_B.vec[1]
    c_P[1] = -(v_A.vec[0] * v_B.vec[2] - v_A.vec[2] * v_B.vec[0])
    c_P[2] = v_A.vec[0] * v_B.vec[1] - v_A.vec[1] * v_B.vec[0]
    return c_P

if __name__ == "__main__":
    vec = Vector2D(2, 0).Normalise()
    vec1 = Vector2D(2, 2).Normalise()
    vec3D = Vector3D(1, 4, 1).Normalise()
    vec3D1 = Vector3D(1, -4, 1).Normalise()
    print(f"Vector1: {str(vec)}, Vector2: {str(vec1)}, Scalar Vectors2D: {str(vec.dot(vec1))}")
    print(f"Vector1: {vec3D}, Vector2:{vec3D1}, Scalar Vectors3D: {vec3D.dot(vec3D1)}")