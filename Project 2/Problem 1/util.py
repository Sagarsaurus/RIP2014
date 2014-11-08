import math

def inRange(a, b, c, inclusive = False):
    if inclusive:
        return a >= b and a <= c
    else:
        return a > b and a < c

def raycast(startPoint, direction, obstacles, limitedRay = False):
    allCollisions = []
    if limitedRay:
        allCollisions.append((startPoint + direction, None))
    for obstacle in obstacles:
        pointsHit = obstacle.raycast(startPoint, direction, limitedRay)
        allCollisions += [(x, obstacle) for x in pointsHit]
    allCollisions = sorted(allCollisions, key = lambda x: (startPoint - x[0]).magnitude())
    return allCollisions

class Vector2:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

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

    def cross(self, other):
        return self.x * other.y - self.y * other.x

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
        cross = ab.cross(ac)
        if abs(cross) > tolerance:
            return False
        dot = ac.dot(ab)
        if dot < 0:
            return False
        lengthSq = self.move.x ** 2 + self.move.y ** 2
        if dot > lengthSq:
            return False
        return True

    def rayCollision(self, rayStart, rayDirection, limitedRay = False):
        q = self.start
        s = self.move

        p = rayStart
        r = rayDirection

        rXs = r.cross(s)
        sXr = s.cross(r)

        if rXs == 0 or sXr == 0: #line and ray are collinear
            return None
        else: 
            t = (q - p).cross(s) / rXs
            u = (p - q).cross(r) / sXr
            if t >= 0 and  (not limitedRay or t <= 1) and u >=0 and u <= 1:
                #print "q ", q
                #print "s ", s
                #print "p ", p
                #print "r ", r
                #print "t ", t
                #print "u ", u
                #print "qsu ", q + s * u 
                #print "prt ", p + r * t
                return q + s * u
            else:
                return None

    def pointProjection(self, point):
        a = point - self.start
        b = self.move
        bNorm = b.norm()

        proj = bNorm * a.dot(bNorm) + self.start
        dist = (point - proj).magnitude()

        #print "start ", self.start
        #print "finish ", self.finish
        #print "point ", point
        #print "a ", a
        #print "b ", b
        #print "proj ", proj
        #print "dot ", (a - (proj - self.start)).dot(b)

        assert (a - (proj - self.start)).dot(b) == 0 

        if self.isOn(proj):
            return dist, proj
        else:
            startDis = (point - self.start).magnitude()
            finishDis = (point - self.finish).magnitude()
            if finishDis < startDis:
                return finishDis, self.finish
            else:
                return startDis, self.start


    def getPoints(self, startLength, step, stop = -1, intersectionStop = None, intersectionStep = 10):
        direction = self.move.norm()
        currentPoint = self.start + direction * startLength
        points = [currentPoint]
        minorStep = step / intersectionStep 
        found = False
        if stop < 0:
            remainingLength = self.length - startLength
        else:
            remainingLength = stop - startLength
        while remainingLength >= step:
            currentPoint += direction * step
            remainingLength -= step
            points.append(currentPoint)
            currentMinorStep = currentPoint
            if intersectionStop != None:
                for i in range(intersectionStep):
                    currentMinorStep += direction * (i * minorStep)
                    if intersectionStop.isOn(currentMinorStep):
                        found = True
                        break
                if found:
                    break
            print currentPoint
        if intersectionStop == None:
            return points, remainingLength
        else:
            return found, points, remainingLength



class Obstacle:

    def collisionCheck(self, point):
        raise NotImplementedError()

    def collisionPointSet(self, pointStart, goal):
        raise NotImplementedError()

    def raycast(self, start, direction, limitedRay = False):
        raise NotImplementedError();

class PolygonObstacle(Obstacle):

    def __init__(self, points):
        self.points = points
        self.lines = []
        for i in range(-1, len(points) - 1):
            self.lines.append(Line(points[i], points[i + 1]))
        assert len(points) == len(self.lines)

    def collisionCheck(self, point):
        pointsHit = len(self.raycast(point, Vector2(1,0)))
        return (pointsHit % 2) != 0

    def raycast(self, start, direction, limitedRay = False):
        pointsHit = []
        for line in self.lines:
            collision = line.rayCollision(start, direction, limitedRay)
            if collision is not None:
                pointsHit.append(collision)
        pointsHit = sorted(pointsHit, key = lambda x: (start - x).magnitude())
        return pointsHit


    def collisionPointSet(self, pointStart, goal, direction = False):
        hitLine = None
        for line in self.lines:
            if line.isOn(pointStart):
                hitLine = line
                print line.start
                print line.finish
        if hitLine == None:
            print point
            closest = float("inf")
            closestPoint = pointStart
            for line in self.lines:
                dist, point = line.pointProjection(pointStart)
                if dist < closest:
                    closest = dist
                    hitLine = line
                    closestPoint = point
            pointStart = closestPoint
        points = [pointStart]
        lineIndex = self.lines.index(hitLine)
        closest = float("inf")
        closestLine = hitLine
        closestPos = pointStart
        seq =  range(lineIndex, lineIndex - len(self.lines), -1) if direction else range(lineIndex - len(self.lines), lineIndex)
        for i in seq:
            point = self.lines[i].start if direction else self.lines[i].finish
            points.append(self.lines[i].start if direction else self.lines[i].finish)
            dist, point = self.lines[i].pointProjection(goal)
            if dist < closest:
                closest = dist
                closestLine = i
                closestPos = point
        points.append(pointStart)
        for i in seq:
            if i == closestLine:
                points += [closestPos]
                break
            else:
                points.append(self.lines[i].start if direction else self.lines[i].finish)
        return closestPos, points

    def collisionPointSetBug2(self, pointStart, muLine):
        hitLine = None
        print pointStart
        for line in self.lines:
            if line.isOn(pointStart):
                hitLine = line
        if hitLine == None:
            raise Exception()
        else:
            points = [pointStart]
            startLength = (pointStart - hitLine.start).magnitude()
            remainingLength = startLength - 1
            lineIndex = self.lines.index(hitLine)
            found = False
            while True:
                found, additionalPoints, remainingLength = self.lines[lineIndex].getPoints(remainingLength, 1, intersectionStop = muLine)
                points += additionalPoints
                lineIndex = lineIndex + 1 if lineIndex + 1 < len(self.lines) else 0
                if found:
                    return points[-1], points


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
            points.append(point)
            print point
        pointsCopy = points[:]
        for i in points:
            pointsCopy.append(i)
            if i != closestPos:
                break
            print i
        return closestPos, pointsCopy

    def collisionPointSetBug2(self, pointStart, muLine):
        radPer1Unit = 1.0 / float(self.r)
        startAngle = math.atan2(pointStart.y - self.y, pointStart.x - self.x)
        muLineNorm = muLine.move.norm()
        angle = startAngle
        points = [pointStart]
        minDist = float("inf")
        closestPos = Vector2(0.0,0.0)
        while True:
            angle += radPer1Unit
            point = Vector2(self.r * math.cos(angle) + self.x, self.r * math.sin(angle) + self.y)
            points.append(point)
            print point
            tempAngle = angle
            found = False
            while tempAngle < angle + radPer1Unit:
                point = Vector2(self.r * math.cos(tempAngle) + self.x, self.r * math.sin(tempAngle) + self.y)
                if muLine.isOn(point):
                    found = True
                    points.append(point)
                    print point
                    break
                tempAngle += radPer1Unit / 1000
            if found:
                break
        return points[-1], points

    def collisionCheck(self, point):
        return (point - Vector2(self.x, self.y)).magnitude() < self.r

    def get_position(self):
        return int(self.x), int(self.y)

    def get_radius(self):
        return int(self.r)