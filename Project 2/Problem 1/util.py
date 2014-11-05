import math

def inRange(a, b, c, inclusive = False):
    if inclusive:
        return a >= b and a <= c
    else:
        return a > b and a < c

class Vector2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __div__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y)

    def __hash__(self):
        return  hash(self.to_tuple())

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def norm(self):
        return self / self.magnitude()

    def to_tuple(self):
        return int(self.x), int(self.y)


class Line:

    def __init__(self, start, finish):
        self.start = start
        self.finish = finish
        self.move = finish - start
        self.length = self.move.magnitude()

    def isOn(self, point, tolerance = 0.1):
        ab = self.move
        ac = point - self.start
        cross = ac.y * ab.x - ac.x * ab.y
        if abs(cross) > tolerance:
            return False
        dot = ac.dot(ab)
        if dot < 0:
            return False
        lengthSq = self.move.x ** 2 + self.move.y ** 2
        if dot > lengthSq:
            return False
        return True

    def getPoints(self, startLength, step, stop = -1):
        direction = self.move.norm()
        currentPoint = self.start + direction * startLength
        points = [currentPoint]
        if stop < 0:
            remainingLength = self.length - startLength
        else:
            remainingLength = stop - startLength
        while remainingLength >= step:
            currentPoint += direction * step
            remainingLength -= step
            points += [currentPoint]
            print currentPoint
        return points, remainingLength



class Obstacle:

    def collisionCheck(self, point):
        raise NotImplementedError()

    def collisionPointSet(self, pointStart, goal):
        raise NotImplementedError()

class PolygonObstacle(Obstacle):

    def __init__(self, points):
        self.points = points
        self.lines = []
        for i in range(-1, len(points) - 1):
            self.lines += [Line(points[i], points[i + 1])]
        assert len(points) == len(self.lines)

    def collisionCheck(self, point):
        for line in self.lines:
            if line.isOn(point):
                return True
        return False

    def collisionPointSet(self, pointStart, goal):
        hitLine = None
        for line in self.lines:
            if line.isOn(pointStart):
                hitLine = line
        if hitLine == None:
            raise Exception()
        else:
            points = []
            startLength = (pointStart - hitLine.start).magnitude()
            remainingLength = startLength
            lineIndex = self.lines.index(hitLine)
            for i in range(lineIndex, len(self.lines)):
                additionalPoints, remainingLength = self.lines[i].getPoints(remainingLength, 1)
                points += additionalPoints
            for i in range(lineIndex):
                additionalPoints, remainingLength = self.lines[i].getPoints(remainingLength, 1)
                points += additionalPoints
            additionalPoints, remainingLength = hitLine.getPoints(remainingLength, 1, stop = startLength)
            points += additionalPoints
            pointsCopy = points[:]
            distances = [(goal - x).magnitude() for x in points]
            closestPos = pointsCopy[distances.index(min(distances))]
            for i in pointsCopy:
                points += [i]
                print i
                if i == closestPos:
                    break;
            return closestPos, points


class RectangleObstacle(Obstacle):

    def __init__(self, x, y, w, h):
        self.T = y
        self.B = y + h
        self.L = x
        self.R = x + w
        self.w = w
        self.h = h

    def collisionCheck(self, point):
            return inRange(point.x, self.L, self.R) and\
                    inRange(point.y, self.T, self.B)

    def onEdge(self, point):
        return (point is Vector2) and\
               (([self.L, self.R].contains(point.x) and inRange(point.y, self.T, self.B, True)) or
                ([self.T, self.B].contains(point.y) and inRange(point.x, self.L, self.R, True)))

    def get_position(self):
        return int(self.L), int(self.T)

    def get_dimensions(self):
        return int(self.w), int(self.h)


class CircleObstacle(Obstacle):

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def collisionPointSet(self, pointStart, goal):
        radPer1Unit = 1.0 / float(self.r)
        startAngle = math.atan2(pointStart.y - self.y, pointStart.x - self.x)
        angle = startAngle
        points = [pointStart]
        minDist = float("inf")
        closestPos = Vector2(0.0,0.0)
        while angle < startAngle + 2 * math.pi:
            angle += radPer1Unit
            point = Vector2(self.r * math.cos(angle) + self.x, self.r * math.sin(angle) + self.y)
            distance = (goal - point).magnitude()
            if distance < minDist:
                minDist = distance
                closestPos = point
            points += [point]
            print point
        pointsCopy = points[:]
        for i in points:
            pointsCopy += [i]
            if i != closestPos:
                break
            print i
        return closestPos, pointsCopy


    def collisionCheck(self, point):
        return (point - Vector2(self.x, self.y)).magnitude() < self.r

    def get_position(self):
        return int(self.x), int(self.y)

    def get_radius(self):
        return int(self.r)