from .util import constrain, map_range

class Vector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "x:{}, y:{}, z:{}".format(self.x, self.y, self.z)

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def __iadd__(self, v):
        return self.add(v)

    def __isub__(self, v):
        return self.sub(v)

    def __add__(self, v):
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)

    def reset(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        return self

    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        return self

    def add(self, v):
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self

    def sub(self, v):
        self.x -= v.x
        self.y -= v.y
        self.z -= v.z
        return self

    def multiply(self, f):
        self.x *= f
        self.y *= f
        self.z *= f
        return self

    def mag_sq(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def bounded(self, size):
        return -size <= self.x <= size and -size <= self.y <= size and -size <= self.z <= size

    def normalize_with(self, low, high):
        self.x = constrain(map_range(self.x, low.x, high.x, -1.0, 1.0), -1.0, 1.0)
        self.y = constrain(map_range(self.y, low.y, high.y, -1.0, 1.0), -1.0, 1.0)
        self.z = constrain(map_range(self.z, low.z, high.z, -1.0, 1.0), -1.0, 1.0)
        return self
