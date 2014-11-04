import util
import math

class BugAlgorithm:

    def __init__(self, startPosition, goalPosition, moveSpeed, obstacles, angleChange):
        self.start = startPosition
        self.bugPosition = startPosition
        self.movementSpeed = moveSpeed
        self.goal = goalPosition
        self.obstacles = obstacles
        self.path = []
        self.angleChange = angleChange

    def timeStep(self):
        
        if self.atGoal():
            return True

        currentDirection = (self.goal - self.bugPosition).norm()
        angle = math.atan2(currentDirection.y, currentDirection.x)
        while True:
            discretizedMovement = Vector2(math.round(currentDirection.x), math.round(currentDirection.))
            if not self.collisionCheck(self.bugPosition + discretizedMovement)
                self.bugPosition += discretizedMovement
                break
            else:
                angle += self.angleChange
                currentDirection = Vector2(math.cos(angle), math.sin(angle))
        path += [self.bugPosition]
        return self.atGoal()

    def run(self, maxTimeSteps = 1000):
        for i in range(0, maxTimeSteps):
            if self.timeStep():
                return i, True
        return maxTimeSteps, False

    def atGoal(self):
        return self.bugPosition == self.goal

    def collisionCheck(self, point):
        for obstacle in self.obstacles:
            if obstacle.collisionCheck(point):
                return True
        return False
    
class Bug1:
