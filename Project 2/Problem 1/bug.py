from util import Vector2
import pygame
import math


class BugAlgorithm:

    def __init__(self, startPosition, goalPosition, obstacles, angleChange):
        self.start = startPosition
        self.goal = goalPosition
        self.obstacles = obstacles
        self.path = []
        self.angleChange = angleChange

    def run(self, maxTimeSteps = 1000):
        raise NotImplementedError()

    def atGoal(self, pos):
        return pos == self.goal

    def collisionCheck(self, point):
        for obstacle in self.obstacles:
            if obstacle.collisionCheck(point):
                return obstacle
        return None

class Bug1(BugAlgorithm):

    def run(self):
        bugPos = self.start
        self.path = [bugPos]
        while not self.atGoal(bugPos):
            currentDirection = (self.goal - bugPos).norm()
            while self.collisionCheck(bugPos + currentDirection) is None and not self.atGoal(bugPos):
                if (self.goal - bugPos).magnitude() < currentDirection.magnitude():
                    bugPos = self.goal
                    break
                else:
                    bugPos += currentDirection
                    self.path += [bugPos]
                    currentDirection = (self.goal - bugPos).norm()
            if self.atGoal(bugPos):
                break
            obstacle = self.collisionCheck(bugPos + currentDirection)
            hitPoint = bugPos
            pointDistances = {}
            bugPos += obstacle.tangent(bugPos)
            while bugPos != hitPoint and not self.atGoal(bugPos):
                print "hi"
                bugPos += obstacle.tangent(bugPos)
                pointDistances += {bugPos: (self.goal - bugPos).magnitude()}
                self.path += [bugPos]
            if self.atGoal(bugPos):
                break
            closestPos = min(pointDistances, key = pointDistances.get)
            while bugPos != closestPos and not self.atGoal(bugPos):
                bugPos += obstacle.tangent(bugPos)
                self.path += [bugPos]
                if self.atGoal(bugPos):
                    break


def main():

    # Define some colors
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

    #Initialize
    start_position = Vector2(1,1)
    goal_position = Vector2(300,100)
    obstacles = []
    angle_change = 45

    bug1 = Bug1(start_position, goal_position, obstacles, angle_change)

    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (640, 480)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Bug 1")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Run bug 1
    bug1.run()

    path_to_tuples = []

    for v in bug1.path:
        path_to_tuples.append(v.to_tuple())

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

        # --- Game logic should go here


        # --- Drawing code should go here

        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(WHITE)

        # print bug1.bugPosition.to_tuple()
        # Drawing other objects

        # Draw obstacles if they exist

        # Draw path for bug
        for position in path_to_tuples:
            pygame.draw.circle(screen, GREEN, position, 1, 0)


        # pygame.draw.circle(screen, GREEN, bug1.bugPosition.to_tuple(), 10, 0)


        # Draw goal for bug
        # pygame.draw.circle(screen, RED, bug1.goalPosition.to_tuple(), 10, 0)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()


if __name__ == "__main__":
    main()