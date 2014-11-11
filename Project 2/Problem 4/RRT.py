from quad_tree import *
import tkinter as tk
from util import *
import math

class RRT:
	def __init__(self, space, limit, arm, obstacles, start, goal): 
		self.space = space
		self.goal = goal
		self.obstacles = obstacles
		self.qt = QuadTree(space, limit, obstacles, start, goal)
		self.tree = Tree(start)
		self.arm = arm

	def grow_baseline(self):
		p, c = self.qt.samplePoint(0.1)
		print(p,c)
		if p and c:
			print(p, c)
			if not self.arm.ArmCollisionCheck(p.components, self.obstacles): 
				self.qt.addPoint(n)
				new = self.arm.a3
				self.arm.setQ(c.components)
				old = self.arm.a3
				self.tree.add(new, old)
				return self.tree.V[-1], self.tree.E[-1]
		return None, None

obstacles = [CircleObstacle(500,350,200), CircleObstacle(150,600,120)]
obstacles = []
space = (2*math.pi, 2*math.pi, 2*math.pi)
rrt = RRT(space, 16, RobotArm((10, 10, 20)), obstacles, NPoint((0, 0, 0)), NPoint((3, 3, 3)))

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

	def draw_dot(self, x, y, r): 
		self.canvas.create_oval(x-r, y-r , x+r, y+r)

	def draw_obstacle(self, obstacle): 
		r = obstacle.r
		self.canvas.create_oval(obstacle.x-r, obstacle.y-r , obstacle.x+r, obstacle.y+r)

	def animate_search(self): 
		p, e = rrt.grow_baseline()
		print(p)
		if p:
			self.draw_dot(p.components[0], p.components[1], 1)
			self.canvas.create_line(e.l.components[0], e.l.components[1], e.r.components[0], e.r.components[1])
		if len(rrt.tree.V) < 2000: 
			self.master.after(1000, self.animate_search)

	def draw_tree(self, tree): 
		for p in tree.V: 
			self.draw_dot(p.x,p.y,1) 
		for e in tree.E: 
			self.canvas.create_line(e.l.x, e.l.y, e.r.x, e.r.y)

root = tk.Tk()
app = App(root, rrt, 1024, 768)
root.mainloop()