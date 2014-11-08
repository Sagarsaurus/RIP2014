from util import *
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

    def run(self, bug = 1):
        bugPos = self.start
        self.path = [bugPos]
        muLine = Line(self.start, self.goal)
        currentDirection = (self.goal - bugPos) #.norm()
        while not self.atGoal(bugPos):
            hitPoints = raycast(bugPos, currentDirection, self.obstacles, limitedRay = True)
            bugPos = hitPoints[0][0] #Get closest point hit by ray
            self.path += [bugPos]
            if self.atGoal(bugPos):
                break
            obstacle = hitPoints[0][1]
            if bug == 1:
                bugPos, additionalPoints = obstacle.collisionPointSet(bugPos, self.goal)
            elif bug == 2:
                bugPos, additionalPoints = obstacle.collisionPointSetBug2(bugPos, muLine)
            currentDirection = (self.goal - bugPos)
            bugPos += currentDirection / 1000 #inch the bug off of the obstacle to avoid raycasting into the obstacle again
            currentDirection = (self.goal - bugPos)
            self.path += additionalPoints 



def main():


    # Define some colors
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    bug_x = [0,0  , 40, 40,5  ,5  ,35 ,35 ,5  ,5 ,35,35,5 ,5 ,35,35 ,5,5 ,35,35,5 ,5,75,75,20,20,75,75,20,20,75,75,20,20 ,75 ,75 ,20 ,20 ,80 ,80]
    bug_y = [0,147,147,140,140,119,119,112,112,91,91,84,84,63,63,56,56,35,35,28,28,7,7 ,42,42,49,49,70,70,77,77,98,98,105,105,126,126,133,133,0 ]
    bug_points = []
    for i in zip(bug_x, bug_y):
        bug_points += [Vector2(i[0], i[1])]

    #Initialize
    start_position = Vector2(10, 60)
    goal_position = Vector2(210, 75)
    obstacles = [ CircleObstacle(50, 60, 20), CircleObstacle(150, 75, 35) ]
    angle_change = 45

    domain1 = BugAlgorithm(start_position, goal_position, obstacles, angle_change)

    start_position = Vector2(25,157)
    goal_position = Vector2(25,17)
    obstacles = [ PolygonObstacle(bug_points) ]
    angle_change = 45

    domain2 = BugAlgorithm(start_position, goal_position, obstacles, angle_change)

    bug = domain2

    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (640, 480)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Bug")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Run bug 
    bug.run(bug = 1)

    path_to_tuples = []

    for v in bug.path:
        path_to_tuples.append(v.to_tuple())
        print v

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

        pygame.draw.lines(screen, GREEN, False, path_to_tuples)

        # Draw obstacles
        if obstacles:
            for obstacle in obstacles:
                if isinstance(obstacle, RectangleObstacle):
                    pygame.draw.rect(screen, BLACK, pygame.Rect(obstacle.get_position(), obstacle.get_dimensions()))
                elif isinstance(obstacle, CircleObstacle):
                    pygame.draw.circle(screen, BLACK, obstacle.get_position(), obstacle.get_radius(), 0)

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