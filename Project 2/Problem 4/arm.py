import math
from util import *

class RobotArm:

	def __init__(self, l, q=(0,0,0)):
		self.l = l
		self.setQ(q)

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
		r1 = raycast(self.link1.start, self.link1.move, obstacles, limitedRay = True)
		r2 = raycast(self.link2.start, self.link2.move, obstacles, limitedRay = True)
		r3 = raycast(self.link3.start, self.link3.move, obstacles, limitedRay = True)
		r = r1 + r2 + r3
		return len(r) != 0

	def setQ(self, q):
		self.q  = q 
		self.a1 = VectorN( (self.l[0] * math.cos(q[0]), self.l[0] * math.sin(q[0]) ) )
		self.a2 = self.a1 + VectorN(( self.l[1] * math.cos(q[0] + q[1]), self.l[1] * math.sin(q[0] + q[1])))
		self.a3 = self.a2 + VectorN(( self.l[2] * math.cos(q[0] + q[1] + q[2]), self.l[2] * math.sin(q[0] + q[1] + q[2])))
		self.link1 = Line(VectorN((0.0, 0.0)), self.a1)
		self.link2 = Line(self.a1, self.a2)
		self.link3 = Line(self.a2, self.a3)

	def inverseKinematics(x, l):
		X2 = x[0] - l[2] * math.cos(x[2])
		Y2 = x[1] - l[2] * math.sin(x[2])
		det = X2**2 + Y2**2
		Q1 = math.acos(X2 / math.sqrt(det)) + math.acos((l[0]**2 - l[1]**2 + det) / (2 * l[0] * math.sqrt(det)))
		Q2 = math.pi + math.acos((l[0]**2 + l[1]**2 - det)/(2 * l[0] * l[1]))
		Q3 = x[2] - Q1 - Q2
		return Q1, Q2, Q3
