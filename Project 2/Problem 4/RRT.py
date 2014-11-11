from quad_tree import *
import tkinter as tk
from util import *
import math

class RRT:
	def __init__(self, space, limit, arm, obstacles, start, goal): 
		self.space = space
		self.start = RobotArm.inverseKinematics(start.to_tuple(), arm.l)
		self.goal = RobotArm.inverseKinematics(goal.to_tuple(), arm.l)
		self.obstacles = obstacles
		self.qt = QuadTree(space, limit, obstacles, NPoint(self.start), NPoint(self.goal))
		self.tree = Tree(start)
		self.arm = arm

	def grow_baseline(self):
		p, c = self.qt.samplePoint(0.02)
		print(p,c)
		if p and c:
			if not self.arm.ArmCollisionCheck(p.components, self.obstacles): 
				self.qt.addPoint(p)
				new = self.arm.a3
				print(self.arm.a3)
				self.arm.setQ(c.components)
				old = self.arm.a3
				self.tree.add(new, old)
				return self.tree.V[-1], self.tree.E[-1]
		return None, None

#obstacles = [CircleObstacle(200,225,100)]#, CircleObstacle(150,600,120)]
#obstacles = [RectangleObstacle(0, 130, 1.57, 200, 500)]
obstacles = []

space = ((-math.pi,)*3, (2*math.pi,)*3)
rrt = RRT(space, 16, RobotArm((200, 200, 100)), obstacles, NPoint((260, 130, 1)), NPoint((-140, 160, -2)))

xOffset = 100
yOffset = 100
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
		self.canvas.create_line(xOffset, 0, xOffset, 1000)
		self.canvas.create_line(0, yMax - yOffset, 1000, yMax - yOffset)

	def draw_dot(self, x, y, r): 
		self.canvas.create_oval(x-r + xOffset, yMax - (y-r + yOffset), x+r + xOffset, yMax-(y + r + yOffset))

	def draw_obstacle(self, obstacle): 
		if isinstance(obstacle, CircleObstacle):
			r = obstacle.r
			self.canvas.create_oval(obstacle.x-r + xOffset, yMax - (obstacle.y-r + yOffset) , obstacle.x+r + xOffset, yMax - (obstacle.y+r + yOffset))
		elif isinstance(obstacle, PolygonObstacle):
			points = [Vector2(xOffset + x.y, yMax - (yOffset + x.y) ).to_tuple() for x in obstacle.points]
			self.canvas.create_polygon(points);
		elif isinstance(obstacle, RectangleObstacle):
			self.draw_obstacle(obstacle.wrapped)

	def animate_search(self): 
		p, e = rrt.grow_baseline()
		#print(p)
		if p:
			self.draw_dot(p.x + xOffset, p.x + yOffset, 1)
			self.canvas.create_line(e.l.x + xOffset, yMax -(e.l.y + yOffset), e.r.x  + xOffset, yMax -(e.r.y + yOffset))
			x = rrt.arm.a1.x + xOffset, rrt.arm.a2.x + xOffset, rrt.arm.a3.x + xOffset
			y = rrt.arm.a1.x + yOffset, rrt.arm.a2.x + yOffset, rrt.arm.a3.x + yOffset
			# self.canvas.create_line(0, 0, x[0], y[0])
			# self.canvas.create_line(x[0], y[0], x[1], y[1])
			# self.canvas.create_line(x[1], y[1], x[2], y[2])
		if len(rrt.tree.V) < 10000: 
			self.master.after(10, self.animate_search)

	def draw_tree(self, tree): 
		for p in tree.V: 
			pass#self.draw_dot(p.x,p.y,1) 
		for e in tree.E: 
			self.canvas.create_line(e.l.x + xOffset, yMax - (e.l.y + yOffset), e.r.x + xOffset, yMax - (e.r.y + yOffset))

root = tk.Tk()
app = App(root, rrt, 1024, 768)
root.mainloop()
