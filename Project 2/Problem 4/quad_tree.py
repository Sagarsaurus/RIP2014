import random
from util import *
from functools import reduce
import itertools
import operator
from arm import *

def prod(iterable):
    return reduce(operator.mul, iterable, 1)

class NRect: 
	def __init__(self, pos, size): 
		self.pos = pos
		self.size = size

	def area(self): 
		return prod(self.size)

	def split(self): 
		size = list(s / 2 for s in self.size)
		permutions = itertools.product((0,1), repeat=len(self.pos))
		newPos = (tuple(x+d*s for d, x, s in zip(p, self.pos, size)) for p in permutions)
		quads = [NRect(pos, size) for pos in newPos]
		return quads

	def __str__(self):
		return "{ (" +  ", ".join("{:.1f}".format(x) for x in self.pos) + "), (" +  ", ".join("{:.1f}".format(x) for x in self.size) + ") }"

	def __repr__(self): 
		return self.__str__()

	def sample(self):
		return VectorN(tuple(x + s * random.random() for x, s in zip(self.pos, self.size)))

	def quad(self, point): 
		coord = tuple(p >= x + s / 2 for p, x, s in zip(point.components, self.pos, self.size))
		quad = sum(x * 2 ** i for i, x in enumerate(reversed(coord)))
		return quad

class Node: 
	def __init__(self, value, parent=None):
		self.value = value
		self.parent = parent
	def __str__(self):
		return str(self.value)
	def __repr__(self): 
		return self.__str__()

class Edge:
	def __init__(self, l, r): 
		self.l = l
		self.r = r
	def __str__(self):
		return "{" +  str(self.l) + " <--> " + str(self.r) + "}"
	def __repr__(self): 
		return self.__str__()

class Tree: 
	def __init__(self, r, precision):
		r = r.round(precision)
		self.precision = precision
		rNode = Node(r)
		self.V = [rNode]
		self.E = []
		self.dict = {r : rNode}
	def add(self, n, p):
		n = n.round(self.precision)
		p = p.round(self.precision)
		pNode = self.dict[p]
		nNode = Node(n, pNode)
		self.V += [pNode]
		self.E += [Edge(pNode,nNode)]
		self.dict[n] = nNode
	def pathToStart(self, n):
		n = n.round(self.precision)
		currentNode = self.dict[n]
		path = []
		while currentNode is not None:
			path = [currentNode.value] + path
			currentNode = currentNode.parent
		return path

class QuadNode(Node): 
	def __init__(self, rect): 
		self.quads = None
		self.rect = rect
		self.points = []
		self.samples = 0
		self.goal = None

	def goalNode(self, goal):
		self.goal = goal

	def getQuad(self, p):
		quad = self.rect.quad(p)
		return self.quads[quad]

	def addPoint(self, p, limit): 
		if self.points and self.rect.area() > limit: 
			self.split(limit)
		if self.quads: 
			self.getQuad(p).addPoint(p, limit)
		self.points += [p]

	def getQuads(self, p):
		if self.quads: 
			return self.getQuad(p).getQuads(p) + [self]
		else: return [self]

	def split(self, limit):
		self.quads = [QuadNode(q) for q in self.rect.split()]
		if self.goal:
			goalquad = self.rect.quad(self.goal)
			self.quads[goalquad].goalNode(self.goal)
		quad = self.rect.quad(self.points[0])
		self.quads[quad].addPoint(self.points[0], limit)

	def remove(self, p): 
		self.points.remove(p)

	def __str__(self):
		return str(self.rect)
	def __repr__(self): 
		return self.__str__()

	def weight(self, quad):
		# print(self.goal)
		if quad.goal: 
			return -1000
		return 1000
		return not self.goal#quad.samples 

	def samplePoint(self, limit, collision):
		sample, closest, quads = None, None, None
		if self.rect.area() < limit or not self.points: 
			sample, closest, quads = self.rect.sample(), None, [self]
		else: 
			if not self.quads and self.points: 
				self.split(limit)
			small = min(self.weight(quad) for quad in self.quads)
			mins = list(idx for (idx, quad) in enumerate(self.quads) if self.weight(quad) == small)
			# print("mins", small, mins, [self.weight(quad) for quad in self.quads])
			quad = self.quads[random.choice(mins)]
			sample, closest, quads = quad.samplePoint(limit, collision)
			if sample:
				quads += [self]
				if not closest: 
					val, closest = min(((sample - p).magnitude(), p) for p in self.points)
		self.samples += 1
		return sample, closest, quads

class QuadTree(): 
	def __init__(self, space, limit, obstacles, start, goal): 
		self.root = QuadNode(NRect( space[0] , space[1] ))
		self.root.goalNode(goal)
		self.limit = limit
		self.obstacles = obstacles
		self.addPoint(start)
		self.start = start
		self.goal = goal
		self.path = []
		print(self.root)

	def addPoint(self, p):
		# self.root.addPoint(p, self.limit)
		# print(p)
		for quad in self.getQuads(p):
			if len(quad.points) == 1:
				quad.addPoint(p, self.limit)
			else: quad.points += [p]

	def getQuads(self, p): 
		return self.root.getQuads(p)

	def collision(self, p, c=None): 
		if c:
			for obstacle in self.obstacles: 
				if obstacle.raycast(p, c - p, limitedRay = True):
					return True
		else: 
			for obstacle in self.obstacles: 
				if obstacle.collisionCheck(p): 
					return True
		return False

	def samplePoint(self, step): 
		p, c, quads = self.root.samplePoint(self.limit, lambda p, c=None: self.collision(p, c))
		# print(self.getQuads(VectorN( (6,0,0) )) )
		if p: 
			if (p-c).magnitude() > step: 
				n = c + (p - c).norm() * step
			else: n = p
			return n, c
		return None, None
