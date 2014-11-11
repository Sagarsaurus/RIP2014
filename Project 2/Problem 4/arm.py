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
			for i in len(q[0]):
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
		self.a1 = VectorN( (self.l[0] * math.cos(q[0]), self.l[0] * math.sin(q[0])) )
		self.a2 = self.a1 + VectorN( (self.l[1] * math.cos(q[0] + q[1]), self.l[1] * math.sin(q[0] + q[1])) )
		self.a3 = self.a2 + VectorN( (self.l[2] * math.cos(q[0] + q[1] + q[2]), self.l[2] * math.sin(q[0] + q[1] + q[2])) )
		self.link1 = Line(VectorN( (0.0, 0.0) ), self.a1)
		self.link2 = Line(self.a1, self.a2)
		self.link3 = Line(self.a2, self.a3)
		self.theta = sum(q)
		return self

	def inverseKinematics(x, l):
		X2 = x[0] - l[2] * math.cos(x[2])
		Y2 = x[1] - l[2] * math.sin(x[2])
		det = X2**2 + Y2**2
		q = [0] * 3
		q[0] = math.acos(X2 / math.sqrt(det)) + math.acos((l[0]**2 - l[1]**2 + det) / (2 * l[0] * math.sqrt(det)))
		q[1] = math.pi + math.acos((l[0]**2 + l[1]**2 - det)/(2 * l[0] * l[1]))
		q[2] = x[2] - q[0] - q[1]
		return q[0], q[1], q[2]

	def inverseJacobian(dx, q, l):
		cos = math.cos
		sin = math.sin
		q1, q2, q3 = q
		dx1, dx2, dx3 = dx
		dq1  = dx1 * (-cos(q1 + q2)/(2*(cos(q1 + q2)*sin(q1) - sin(q1 + q2)*cos(q1))))            + dx2 * (-sin(q1 + q2)/(2*(cos(q1 + q2)*sin(q1) - sin(q1 + q2)*cos(q1))))            + dx3 * ((cos(q1 + q2 + q3)*sin(q1 + q2) - sin(q1 + q2 + q3)*cos(q1 + q2))/(2*(cos(q1 + q2)*sin(q1) - sin(q1 + q2)*cos(q1))))
		dq2  = dx1 * ((cos(q1 + q2) + cos(q1))/(2*(cos(q1 + q2)*sin(q1) - sin(q1 + q2)*cos(q1)))) + dx2 * ((sin(q1 + q2) + sin(q1))/(2*(cos(q1 + q2)*sin(q1) - sin(q1 + q2)*cos(q1)))) + dx3 * (-(cos(q1 + q2 + q3)*sin(q1 + q2) - sin(q1 + q2 + q3)*cos(q1 + q2) + cos(q1 + q2 + q3)*sin(q1) - sin(q1 + q2 + q3)*cos(q1))/(2*(cos(q1 + q2)*sin(q1) - sin(q1 + q2)*cos(q1))))
		dq3 = dx1 (-cos(q1)/(2*(cos(q1 + q2)*sin(q1) - sin(q1 + q2)*cos(q1))))                + dx2 * (-sin(q1)/(2*(cos(q1 + q2)*sin(q1) - sin(q1 + q2)*cos(q1))))                 + dx3 * ((cos(q1 + q2 + q3)*sin(q1) - sin(q1 + q2 + q3)*cos(q1) + 2*cos(q1 + q2)*sin(q1) - 2*sin(q1 + q2)*cos(q1))/(2*(cos(q1 + q2)*sin(q1) - sin(q1 + q2)*cos(q1))))
		return (dq1, dq2, dq3)

	def getEnd(self):
		return VectorN( (self.a3[0], self.a3[1], self.theta) )
