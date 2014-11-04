import math

def inRange(a, b, c, inclusive = False):
    if inclusive:
        return a >= b and a <= c
    else
        return a > b and a < c

class Vector2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.x + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.x - other.y)

    def __mul__(self, other):
        if other is Vector2:
            return self.x * other.x + self.y * other.y
        else
            return Vector2(self.x * other, self.y * other)

    def __div__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __eq__(self, other):
        return (other is Vector2) and (self.x == other.x) and (self.y == other.y)

    def magnitude(self):
        return math.sqrt(self.x ^ 2 + self.y ^ 2)

    def norm(self):
        return self / self.magnitude()

class Line:

    def __init__(self, start, finish):
        self.start = start
        self.finish = finish

class Obstacle:

    def collisionCheck(self, point):
        raise NotImplementedError()

    def tangent(self, point):
        raise NotImplementedError()

class RectangleObstacle(Obstacle):

    def __init__(self, x, y, w, h):
        self.T = y
        self.B = y + h
        self.L = x
        self.R = x + w

    def collisionCheck(self. point):
        if not (point is Vector2):
            return False
        else
            return inRange(point.x, self.L, self.R) and
                    inRange(point.y, self.T, self.B)

    def tangent(self, point):
        if self.onEdge(point):
            return Vector(0,0)
        else:
            if point.x == self.L:
                if point.y == self.B:       #BL Corner
                    return Vector(1, 0)
                else:                       #L Edge
                    return Vector(0, -1)
            elif point.x == self.R: 
                if point.y == self.T:       #TR Corner
                    return Vector(-1, 0)
                else:                       #R Edge
                    return Vector(0, 1)
            else:
                if point.y == self.T:       #T Edge
                    return Vector(-1, 0)
                elif point.y == self.B      #B Edge
                    return Vector(1, 0)
                else:
                    return Vector(0, 0)

    def onEdge(self, point):
        return (point is Vector2) and
               (([self.L, self.R].contains(point.x) and inRange(point.y, self.T, self.B, True)) or
                ([self.T, self.B].contains(point.y) and inRange(point.x, self.L, self.R, True)))
                

class CircleObstacle(Obstacle):

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def collisionCheck(self. point):
        if not(point is Vector2):
            return False
        else
            return (point - Vector2(self.x, self.y)).magnitude() < r
