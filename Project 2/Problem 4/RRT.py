from quad_tree import *
import tkinter as tk
from util import *
import math

class RRT:
	def __init__(self, space, limit, arm, obstacles, start, goal, precision): 
		self.space = space
		self.start = VectorN(RobotArm.inverseKinematics(start.to_tuple(), arm.l))
		self.goal = VectorN(RobotArm.inverseKinematics(goal.to_tuple(), arm.l))
		self.worldGoal = goal
		self.obstacles = obstacles
		self.qt = QuadTree(space, limit, obstacles, self.start, self.goal)
		self.worldTree = Tree(start, precision)
		self.configTree =  Tree(self.start, precision)
		self.arm = arm
		self.pathFound = False
		self.path = []
		self.closest = float('inf')
		self.goalApproximation = (1, 1, 0.1)

	def grow_baseline(self, step, goalDirected):
		p, c = self.qt.samplePoint(step, goalDirected)
		if p and c:
			if not self.arm.ArmCollisionCheck(p.components, self.obstacles): 
				# print(p)
				self.qt.addPoint(p)
				new = self.arm.getEnd()
				old = self.arm.setQ(c.components).getEnd()
				self.worldTree.add(new, old)
				self.configTree.add(p, c)
				self.arm.setQ(p)
				return self.worldTree.V[-1], self.worldTree.E[-1]
		return None, None

	def goalNear(self, p): 
		print([ (d, t) for d, t in zip(p - self.worldGoal, self.goalApproximation)])
		print([ (abs(d) < t) for d, t in zip(p - self.worldGoal, self.goalApproximation)])
		print(p, self.worldGoal)
		dist = (p - self.worldGoal).magnitude()
		if dist < self.closest:
			self.closest = dist
			print(dist)
		if not any(abs(d) > t for d, t in zip(p - self.worldGoal, self.goalApproximation)):
			# self.configTree.add(self.goal, p)
			# self.path = self.configTree(self.goal)
			return True
		return False

obstacles = [CircleObstacle(200,225,100)]#, CircleObstacle(150,600,120)]
# obstacles = [RectangleObstacle(200, 220, 1.57, 100, 100)]
# obstacles = []
space = ((-2*math.pi,)*3, (4*math.pi,)*3)
rrt = RRT(space, 0.00001, RobotArm((200, 200, 100)), obstacles, VectorN((260, 130, 1)), VectorN((-140, 160, 2*math.pi-2)), 8 )

xOffset = 500
yOffset = 300
yMax = 700

class App:
	def __init__(self, master, rrt, w, h):
		self.w = w
		self.h = h
		self.master = master
		frame = tk.Frame(master)
		frame.pack()
		self.canvas = tk.Canvas(master, width=w, height=h)
		self.canvas.pack()
		for obstacle in obstacles: 
			self.draw_obstacle(obstacle)
		self.master.after(1000, self.animate_search)
		self.canvas.create_line(xOffset, 0, xOffset, w)
		self.canvas.create_line(0, yOffset, 1000, yOffset)
		self.draw_arm(rrt.arm.setQ(rrt.start), "red")
		self.draw_arm(rrt.arm.setQ(rrt.goal), "green")
		self.draw_arm(rrt.arm.setQ(rrt.goal), "green")
		print(rrt.goal)

	def draw_dot(self, x, y, r): 
		self.canvas.create_oval(x-r + xOffset, y-r + yOffset, x+r + xOffset, y + r + yOffset)

	def draw_line(self, p1, p2):
		self.canvas.create_line(p1[0] + xOffset, p1[1] + yOffset, p2[0] + xOffset, p2[1] + yOffset)

	def draw_obstacle(self, obstacle): 
		if isinstance(obstacle, CircleObstacle):
			r = obstacle.r
			self.canvas.create_oval(obstacle.x-r + xOffset, obstacle.y-r + yOffset , obstacle.x+r + xOffset, obstacle.y+r + yOffset)
		elif isinstance(obstacle, PolygonObstacle):
			points = [VectorN( (xOffset + x.x, yOffset + x.y) ).to_tuple() for x in obstacle.points]
			self.canvas.create_polygon(points);
		elif isinstance(obstacle, RectangleObstacle):
			self.draw_obstacle(obstacle.wrapped)

	def draw_arm(self, arm, color): 
		x = arm.a1[0] + xOffset, arm.a2[0] + xOffset, arm.a3[0] + xOffset
		y = arm.a1[1] + yOffset, arm.a2[1] + yOffset, arm.a3[1] + yOffset
		arm.armLines[0] = self.canvas.create_line(xOffset, yOffset, x[0], y[0], fill=color)
		arm.armLines[1] = self.canvas.create_line(x[0], y[0], x[1], y[1], fill=color)
		arm.armLines[2] = self.canvas.create_line(x[1], y[1], x[2], y[2], fill=color)

	def deleteArm(self, arm): 
		for line in arm.armLines:
			self.canvas.delete(line) 

	def animate_search(self): 
		p, e = rrt.grow_baseline(0.2, True)
		# print(p)
		if p:
			self.draw_dot(p.value[0], p.value[1], 1)
			self.draw_line(e.l.value, e.r.value)
			self.deleteArm(rrt.arm)
			self.draw_arm(rrt.arm, "blue")

		if len(rrt.worldTree.V) < 3000 and (not p or not rrt.goalNear(p.value)): 
			self.master.after(10, self.animate_search)

	def draw_tree(self, tree): 
		for p in tree.V: 
			self.draw_dot(p.x,p.y,1) 
		for e in tree.E: 
			self.canvas.create_line(e.l.x + xOffset, yMax - (e.l.y + yOffset), e.r.x + xOffset, yMax - (e.r.y + yOffset))

root = tk.Tk()
app = App(root, rrt, 1024, 768)
root.mainloop()
