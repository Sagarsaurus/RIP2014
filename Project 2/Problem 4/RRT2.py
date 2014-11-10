from quad_tree import *
import tkinter as tk

class RRT:
	def __init__(self, w, h, limit): 
		self.w = w
		self.h = h
		self.qt = QuadTree(w, h, limit)

	def baseline(self, n):
		return (self.qt.samplePoint() for x in range(n))

rrt = RRT(256, 256, 16)
bl = list(rrt.baseline(10))

class App:
	def __init__(self, master, rrt):
		frame = tk.Frame(master)
		frame.pack()
		self.canvas = tk.Canvas(master, width=rrt.w, height=rrt.h)
		self.canvas.pack()
		self.draw_tree(rrt.qt.tree)

	def draw_dot(self, x, y, r): 
		self.canvas.create_oval(x-r, y-r , x+r, y+r)

	def draw_tree(self, tree): 
		for p in tree.V: 
			self.draw_dot(p.x,p.y,1) 
		for e in tree.E: 
			self.canvas.create_line(e.l.x, e.l.y, e.r.x, e.r.y)

root = tk.Tk()
app = App(root, rrt)
root.mainloop()