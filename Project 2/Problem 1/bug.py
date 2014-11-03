import util

class BugAlgorithm:

    def __init__(self, startPosition, goalPosition, moveSpeed, obstacles):
        self.start = startPosition
        self.bugPosition = startPosition
        self.movementSpeed = moveSpeed
        self.goal = goalPosition
        self.obstacles = obstacles
        self.path = []

    def timeStep(self):
        
        if self.atGoal()
            return True
        
        directionToGoal = (self.goal - self.bugPosition).norm()
        directMovement = directionToGoal * movementSpeed
        endPosition = self.bugPosition
        movement = ()
        if collisionCheck(directMovement):
            #Need to fill the rest of this
        else:
            if (self.goal - self.bugPosition).magnitude() <= self.movementSpeed
                endPosition = self.goal
            else:
                endPosition = self.bugPosition + directMovement
            movement = (endPosition)
        self.bugPosition = endPosition
        self.path += [movement]
        return self.atGoal()
        

    def run(self, maxTimeSteps = 1000):
        for i in range(0, maxTimeSteps):
            if self.atGoal()
                return i, True
        return maxTimeSteps, False

    def atGoal(self):
        return self.bugPosition == self.goal

    def collisionCheck(self, point):
        for obstacle in self.obstacles:
            if obstacle.collisionCheck(point):
                return True
        return False

    def raycast(self, start, ray):
        raise NotImplementedError()
    
class Bug1:
