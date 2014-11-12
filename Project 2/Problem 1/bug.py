from util import *
import tkinter as tk
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
            self.path += additionalPoints
            currentDirection = (self.goal - bugPos)
            bugPos += currentDirection / 1000 #inch the bug off of the obstacle to avoid raycasting into the obstacle again
            currentDirection = (self.goal - bugPos)

xOffset = 500
yOffset = 300
yMax = 700

class App:
    def __init__(self, master, bug, domain, w, h):
        self.w = w
        self.h = h
        self.master = master
        frame = tk.Frame(master)
        frame.pack()
        self.canvas = tk.Canvas(master, width=w, height=h)
        self.canvas.pack()

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

        bugAlg = domain1 if domain == 1 else domain2

        # Run bug 
        bugAlg.run(bug)
        print("hi")

        totalDistance = 0
        euclidieanDist = (bugAlg.goal - bugAlg.start).magnitude()
        bugPath = []
        for i in range(0, len(bugAlg.path) - 1):
            v1 = bugAlg.path[i]
            v2 = bugAlg.path[i + 1]
            mag = (v2 - v1).magnitude()
            norm = (v2 - v1).norm()
            bugPath.append(v1)
            i = 1
            while i < mag:
                bugPath.append(v1 + norm * i)
                i += 1
            bugPath.append(v2)
            totalDistance += mag

        print("Total Distance: ", totalDistance)
        print("Euclidiean Distance: ", euclidieanDist)
        print("Ratio: ", float(totalDistance) / float(euclidieanDist))

        self.path_to_tuples = []

        for v in bugPath:
            print(v)
            tupleV = v.to_tuple()
            tupleV = (xOffset + tupleV[0], yMax - (yOffset + tupleV[1]))
            self.path_to_tuples.append(tupleV)

        for obstacle in bugAlg.obstacles: 
            self.draw_obstacle(obstacle)
        self.p = 1
        self.canvas.create_line(xOffset, 0, xOffset, w)
        self.canvas.create_line(0, yMax - yOffset, 1000, yMax - yOffset)
        self.master.after(1000, self.animate_movement)
        self.line = None

    def animate_movement(self):
        self.canvas.delete(self.line)

        if self.p > len(self.path_to_tuples):
            self.p = 1

        self.p += 1

        drawn_path = self.path_to_tuples[0 : self.p]
        self.line = self.canvas.create_line(drawn_path, fill='green') 
        self.canvas.after(10, self.animate_movement)

    def draw_obstacle(self, obstacle):
        print("HI")
        if isinstance(obstacle, CircleObstacle):
            print("BYE")
            r = obstacle.r
            self.canvas.create_oval(obstacle.x-r + xOffset, yMax - (obstacle.y-r + yOffset), obstacle.x+r + xOffset, yMax -(obstacle.y+r + yOffset))
        elif isinstance(obstacle, PolygonObstacle):
            points = [Vector2(xOffset + x.x, yMax - (yOffset + x.y)).to_tuple() for x in obstacle.points]
            self.canvas.create_polygon(points, width='0.25');
        elif isinstance(obstacle, RectangleObstacle):
            self.draw_obstacle(obstacle.wrapped)

root = tk.Tk()
app = App(root, 2, 2, 1024, 768)
root.mainloop()
