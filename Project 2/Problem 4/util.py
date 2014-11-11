import math

def inRange(a, b, c, inclusive = False):
    if inclusive:
        return a >= b and a <= c
    else:
        return a > b and a < c

def raycast(startPoint, direction, obstacles, limitedRay = False):
    allCollisions = []
    # if limitedRay:
    #     allCollisions.append((startPoint + direction, None))
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

    def angle(self):
        return math.atan2(self.y, self.x)

    def to_tuple(self):
        return int(self.x), int(self.y)

class VectorN:

    def __init__(self, components):
        self.components = [float(x) for x in components]
        self.n = len(components)

    def __add__(self, other):
        if self.n == other.n:
            comp = [0 for x in self.components]
            for i in range(self.n):
                comp[i] = self.components[i] + other.components[i]
            return VectorN(comp)
        else:
            raise Exception()

    def __sub__(self, other):
        if self.n == other.n:
            comp = [0 for x in self.components]
            for i in range(self.n):
                comp[i] = self.components[i] - other.components[i]
            return VectorN(comp)
        else:
            raise Exception()

    def __mul__(self, other):
        return VectorN([x * other for x in self.components])

    def __div__(self, other):
        return VectorN([x / other for x in self.components])

    def __truediv__(self, other):
        return self.__div__(other)

    def __eq__(self, other):
        if self.n == other.n:
            for i in range(self.n):
                if self.components[i] != other.components[i]:
                    return False
            return True
        else:
            return False

    def __str__(self):
        return str(self.to_tuple())

    def __repr__(self): 
        return self.__str__()

    def __hash__(self):
        return  hash(self.to_tuple())

    def dot(self, other):
        if self.n == other.n:
            comp = [0 for x in self.components]
            for i in range(self.n):
                comp[i] = self.components[i] * other.components[i]
            return sum(comp)
        else: 
            raise Exception()

    def to_tuple(self):
        return tuple(self.components)

    def magnitude(self):
        return math.sqrt(sum([x ** 2 for x in self.components]))

    def norm(self):
        return self / self.magnitude()

class Line:

    def __init__(self, start, finish):
        print("A",start, finish)
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
                return q + s * u
            else:
                return None

    def pointProjection(self, point):
        a = point - self.start
        b = self.move
        bNorm = b.norm()

        proj = bNorm * a.dot(bNorm) + self.start
        dist = (point - proj).magnitude()

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
        if hitLine == None:
            closest = float("inf")
            closestPoint = pointStart
            for line in self.lines:
                dist, point = line.pointProjection(pointStart)
                if dist < closest:
                    closest = dist
                    hitLine = line
                    closestPoint = point
            pointStart = closestPoint
        points = []
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

    def collisionPointSetBug2(self, pointStart, muLine, direction = False):
        hitLine = None
        muStart = muLine.start
        goal = muLine.finish
        muMove = muLine.move
        muNorm = muMove.norm()
        for line in self.lines:
            if line.isOn(pointStart):
                hitLine = line
        if hitLine == None:
            closest = float("inf")
            closestPoint = pointStart
            for line in self.lines:
                dist, point = line.pointProjection(pointStart)
                if dist < closest:
                    closest = dist
                    hitLine = line
                    closestPoint = point
            pointStart = closestPoint
        dist = (goal - pointStart).magnitude()
        points = []
        closestPos = pointStart
        lineIndex = self.lines.index(hitLine)
        while True:
            line = self.lines[lineIndex]
            rayHit = line.rayCollision(muStart, muMove)
            if rayHit is not None and self.sidedCheck(rayHit, goal) and (goal - rayHit).magnitude() < dist:
                closestPos = rayHit
                points.append(rayHit)
                break
            else:
                points.append(line.start if direction else line.finish)
            lineIndex += -1 if direction else 1
            if lineIndex >= len(self.lines):
                lineIndex = 0
        return closestPos, points

    def sidedCheck(self, rayHit, goal):
        delta = (goal - rayHit).norm() / 10
        toward = self.collisionCheck(rayHit + delta)
        away = self.collisionCheck(rayHit - delta)
        return not toward and away


class RectangleObstacle(Obstacle):

    def __init__(self, cX, cY, orientation, width, height):
        orth = orientation + math.pi / 2
        C = Vector2(cX, cY)
        orientV = Vector2(math.cos(orientation), math.sin(orientation)) * (height / 2) 
        orthV = Vector2(math.cos(orth), math.sin(orth)) * (width / 2)
        points = [C + orthV + orientV, C + orthV - orientV, C - orthV - orientV, C - orthV + orientV]
        self.wrapped = PolygonObstacle(points)

    def collisionCheck(self, point):
        return self.wrapped.collisionCheck(point)

    def raycast(self, start, direction, limitedRay = False):
        return self.wrapped.raycast(start, direction, limitedRay)

class CircleObstacle(Obstacle):

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.c = Vector2(x, y)
        self.r = r

    def collisionPointSet(self, pointStart, goal):
        radPer1Unit = 1.0 / float(self.r)
        startAngle = (pointStart  - self.c).angle()
        angle = startAngle
        points = []
        minDist = float("inf")
        goalDist = (goal - Vector2(self.x, self.y))
        closestAngle = goalDist.angle()
        closestPoint = self.c + goalDist.norm() * self.r
        while angle < startAngle + 2 * math.pi:
            angle += radPer1Unit
            points.append(self.c + Vector2(math.cos(angle), math.sin(angle)) * self.r)
        pointsCopy = points[:]
        angle = startAngle + radPer1Unit
        if closestAngle < angle:
            closestAngle += 2 * math.pi
        i = 0
        while angle + i * radPer1Unit < closestAngle:
            if angle + (i + 1) * radPer1Unit >= closestAngle:
                pointsCopy.append(closestPoint)
                break
            else:
                pointsCopy.append(points[i])
            i += 1
        return closestPoint, pointsCopy

    def collisionPointSetBug2(self, pointStart, muLine):
        radPer1Unit = 1.0 / float(self.r)
        startAngle = (pointStart  - self.c).angle()
        muStart = muLine.start
        goal = muLine.finish
        muMove = muLine.move
        hitPoints = self.raycast(muStart, muMove, limitedRay = True)
        closestPoint = pointStart
        closestAngle = startAngle
        if hitPoints is None or len(hitPoints) <= 0:
            raise Exception()
        elif len(hitPoints) == 1:
            closestPoint = hitPoints[0]
        else:
            d1 = (goal - hitPoints[0]).magnitude()
            d2 = (goal - hitPoints[1]).magnitude()
            closestPoint = hitPoints[0] if d1 < d2 else hitPoints[1]
        closestAngle = (closestPoint - self.c).angle()
        angle = startAngle
        points = []
        if closestAngle < angle:
            closestAngle += 2 * math.pi
        while angle < closestAngle:
            angle += radPer1Unit
            if angle >= closestAngle:
                points.append(closestPoint)
                break
            else:
                points.append(self.c + Vector2(math.cos(angle), math.sin(angle)) * self.r)
        return closestPoint, points

    def raycast(self, start, direction, limitedRay = False):
        E = start
        L = start + direction
        C = self.c
        r = self.r

        d = direction
        f = E - C

        a = d.dot(d)
        b = 2*f.dot(d)
        c = f.dot(f) - r ** 2

        disc = b ** 2 - 4*a*c

        if a <= 0 or disc < 0:
            return []
        elif disc == 0:
            t = -b / (2 * b)
            if t >= 0 and (not limitedRay or t <= 1):
                return [E + d *t]
            else:
                return []
        else:
            t1 = (-b + math.sqrt(disc)) / (2 * a)
            t2 = (-b - math.sqrt(disc)) / (2 * a)

            returnValues = []
            if t1 >= 0 and (not limitedRay or t1 <= 1):
                returnValues.append(E + d * t1)
            if t2 >= 0 and (not limitedRay or t2 <= 1):
                returnValues.append(E + d * t2)

            return returnValues


    def collisionCheck(self, point):
        return (point - Vector(self.x, self.y)).magnitude() < self.r

    def get_position(self):
        return int(self.x), int(self.y)

    def get_radius(self):
        return int(self.r)