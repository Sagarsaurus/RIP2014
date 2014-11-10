from quad_tree import *
import tkinter as tk
from util import *

class RRT:
	def __init__(self, w, h, limit, obstacles): 
		self.w = w
		self.h = h
		self.qt = QuadTree(w, h, limit, obstacles)
		self.tree = None

	def start(self, start): 
		self.tree = Tree(start)
		self.qt.addPoint(start)

	def grow_baseline(self):
		p, c = self.qt.samplePoint()
		self.tree.add(p, c)
		return self.tree.V[-1], self.tree.E[-1]

obstacles = [CircleObstacle(700,500,150),CircleObstacle(150,75,35)]
rrt = RRT(1024, 768, 16, obstacles)
rrt.start(Point(500, 350))

class App:
	def __init__(self, master, rrt):
		self.master = master
		frame = tk.Frame(master)
		frame.pack()
		self.canvas = tk.Canvas(master, width=rrt.w, height=rrt.h)
		self.canvas.pack()
		for obstacle in obstacles: 
			self.draw_obstacle(obstacle)
		self.master.after(1000, self.animate_search)
		# self.draw_tree(rrt.qt.tree)

	def draw_dot(self, x, y, r): 
		self.canvas.create_oval(x-r, y-r , x+r, y+r)

	def draw_obstacle(self, obstacle): 
		r = obstacle.r
		self.canvas.create_oval(obstacle.x-r, obstacle.y-r , obstacle.x+r, obstacle.y+r)

	def animate_search(self): 
		p, e = rrt.grow_baseline()
		print(p)
		if p:
			self.draw_dot(p.x,p.y,1)
			self.canvas.create_line(e.l.x, e.l.y, e.r.x, e.r.y)
		self.master.after(10, self.animate_search)

	def draw_tree(self, tree): 
		for p in tree.V: 
			self.draw_dot(p.x,p.y,1) 
		for e in tree.E: 
			self.canvas.create_line(e.l.x, e.l.y, e.r.x, e.r.y)

root = tk.Tk()
app = App(root, rrt)
root.mainloop()