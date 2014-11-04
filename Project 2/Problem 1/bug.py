import util

class BugAlgorithm:

    def __init__(self, startPosition, goalPosition, moveSpeed, obstacles):
        self.start = startPosition
        self.bugPosition = startPosition
        self.movementSpeed = moveSpeed
        self.goal = goalPosition
        self.obstacles = obstacles
        self.path = []

    def run(self):
        
        if self.atGoal()
            return True

        currentPosition = self.bugPosition
        currentDirection = (self.goal - currentPosition).norm()
        remainingMovement = movementSpeed
        movement = [currentPosition]
        while True:
            while True:
                obstacle, point = self.raycast(currentPosition, currentDirection * remaningMovement)
                remainingMovement -= (currentPosition - point).magnitude()
                currentPosition = point
                movement += [currentPosition]
                if obstacle == None:
                    if (self.goal - currentPosition).magnitude() <= remainingMovement:
                        currentPosition = self.goal
                    else:
                        currentPosition += (self.goal - currentPosition).norm() * remainingMovement
                    movement += [currentPosition]
                    break
                elif remainingMovement <= 0:
                    break
                else
                    currentDirection = obstacle.tangent(point)

            self.bugPosition = currentPosition
            if self.atGoal() or remainingMovement <= 0:
                break;
            currentDirection = (self.goal - currentPosition).norm() #next raycast needs to be facing the goal
        movement = tuple(movement)
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
                return obstacle
        return None

    def raycast(self, start, ray):
        raise NotImplementedError()
    
class Bug1:
