import random

class Rect:
	TL = 0
	TR = 1
	BL = 2
	BR = 3
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	def area(self): 
		return self.w * self.h

	def split(self): 
		return [	Rect(self.x, self.y, self.w / 2, self.h / 2), 
					Rect(self.x + self.w / 2, self.y, self.w / 2, self.h / 2), 
					Rect(self.x, self.y + self.h / 2, self.w / 2, self.h / 2), 
					Rect(self.x + self.w / 2, self.y + self.h / 2, self.w / 2, self.h / 2) ]

	def quad(self, p): 
		return (p.x >= self.x + self.w / 2) + (p.y >= self.y + self.h / 2) * 2

	def sample(self):
		return Point(self.x + self.w * random.random(), self.y + self.h * random.random())

	def __str__(self):
		return "(" +  "{:.1f}".format(self.x) + ", " + "{:.1f}".format(self.y) + ", " + "{:.1f}".format(self.w) + ", " + "{:.1f}".format(self.h) + ")"

	def __repr__(self): 
		return self.__str__()

class Node: 
	def __init__(self): 
		x=5

class Edge:
	def __init__(self, l, r): 
		self.l = l
		self.r = r
	def __str__(self):
		return "{" +  str(self.l) + " <--> " + str(self.r) + "}"
	def __repr__(self): 
		return self.__str__()

class Tree: 
	def __init__(self, r):
		self.V = [r]
		self.E = []
	def add(self, n, p):
		self.V += [n]
		self.E += [Edge(p,n)]

class Point(Node): 
	def __init__(self, x, y): 
		self.x = x
		self.y = y
	def __str__(self):
		return "(" +  "{:.1f}".format(self.x) + ", " + "{:.1f}".format(self.y) + ")"
	def __repr__(self): 
		return self.__str__()

class QuadNode(Node): 
	def __init__(self, rect): 
		self.quads = None
		self.rect = rect
		self.points = []

	def addPoint(self, p, limit): 
		if self.points and self.rect.area() > limit: 
			self.split(limit)
			quad = self.rect.quad(p)
			quads[quad].addPoint(p)
		print(self.rect, p)
		self.points += [p]

	def split(self, limit):
		self.quads = [QuadNode(q) for q in self.rect.split()]
		quad = self.rect.quad(self.points[0])
		self.quads[quad].addPoint(self.points[0], limit)

	def distance(self, l, r): 
		return (l.x-r.x)**2 + (l.y-r.y)**2

	def samplePoint(self, limit):
		sample = None
		if self.rect.area() < limit or not self.points: 
			sample = self.rect.sample(), None
			print(self.rect, sample[0])
		else: 
			if len(self.points) == 1: 
				self.split(limit)
			small = min(len(quad.points) for quad in self.quads)
			mins = list(idx for (idx, quad) in enumerate(self.quads) if len(quad.points) == small)
			quad = random.choice(mins)
			sample = self.quads[quad].samplePoint(limit)
			if not sample[1]:
				val, closest = min((self.distance(sample[0], p), p) for p in self.points)
				print(closest)
				sample = sample[0], closest
		self.points += [sample[0]]
		return sample

class QuadTree(Tree): 
	def __init__(self, w, h, limit): 
		self.root = QuadNode(Rect(0, 0, w, h))
		self.limit = limit
		self.tree = None

	def addPoint(self, p):
		self.root.addPoint(p, self.limit)

	def samplePoint(self): 
		p, c = self.root.samplePoint(self.limit)
		if c: 
			self.tree.add(p, c)
		else:
			self.tree = Tree(p)
		return p
