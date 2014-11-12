import math
from util import *

class RobotArm:

	def __init__(self, l, q=(0,0,0)):
		self.l = l
		self.setQ(q)
		self.armLines = [None]*len(q)

	def ArmMovementCollisionCheck(self, q1, q2, timeStep, obstacles):
		t = 0
		cQ = q
		while t < 1:
			for i in len(q1):
				cQ[i] = lerp(q1[i], q2[i], t)
			if self.ArmCollisionCheck(cQ, obstacles):
				return True
			t += timeStep
		return False

	def ArmCollisionCheck(self, q, obstacles):
		self.setQ(q)

		r1 = raycast(Vector2(self.link1.start[0], self.link1.start[1]), Vector2(self.link1.move[0], self.link1.move[1]) , obstacles, limitedRay = True)
		r2 = raycast(Vector2(self.link2.start[0], self.link2.start[1]), Vector2(self.link2.move[0], self.link2.move[1]) , obstacles, limitedRay = True)
		r3 = raycast(Vector2(self.link3.start[0], self.link3.start[1]), Vector2(self.link3.move[0], self.link3.move[1]) , obstacles, limitedRay = True)
		r = r1 + r2 + r3
		return len(r) != 0

	def setQ(self, q):
		self.q  = q 
		self.a1 = VectorN( (self.l[0] * math.cos(q[0]), self.l[0] * math.sin(q[0])) )
		self.a2 = self.a1 + VectorN( (self.l[1] * math.cos(q[0] + q[1]), self.l[1] * math.sin(q[0] + q[1])) )
		self.a3 = self.a2 + VectorN( (self.l[2] * math.cos(q[0] + q[1] + q[2]), self.l[2] * math.sin(q[0] + q[1] + q[2])) )
		self.link1 = Line(VectorN( (0.0, 0.0) ), self.a1)
		self.link2 = Line(self.a1, self.a2)
		self.link3 = Line(self.a2, self.a3)
		self.theta = math.fmod(sum(q), 2*math.pi)
		if self.theta < 0:
			self.theta = self.theta + 2*math.pi
		return self

	def inverseKinematics(x, l):
		X2 = x[0] - l[2] * math.cos(x[2])
		Y2 = x[1] - l[2] * math.sin(x[2])
		det = X2**2 + Y2**2
		Q1 = math.fmod(math.acos(X2 / math.sqrt(det)) + math.acos((l[0]**2 - l[1]**2 + det) / (2 * l[0] * math.sqrt(det))), 2*math.pi)
		Q2 = math.fmod(math.pi + math.acos((l[0]**2 + l[1]**2 - det)/(2 * l[0] * l[1])), 2*math.pi)
		Q3 = math.fmod(x[2] - Q1 - Q2, 2*math.pi)
		return Q1, Q2, Q3

	def getEnd(self):
		return VectorN( (self.a3[0], self.a3[1], self.theta) )
