import math

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

class Obstacle:

    def collisionCheck(self, point):
        raise NotImplementedError()

class RectangleObstacle(Obstacle):

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def collisionCheck(self. point):
        if not (point is Vector2):
            return False
        else
            return point.x >= self.x and point.x <= self.x + self.w and
                    point.y >= self.y  and point.x <= self.y + self.h

class CircleObstacle(Obstacle):

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def collisionCheck(self. point):
        if not(point is Vector2):
            return False
        else
            return (point - Vector2(self.x, self.y)).magnitude() <= r
