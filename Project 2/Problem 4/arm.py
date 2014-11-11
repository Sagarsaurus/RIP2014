import math
import util

class RobotArm:

	def __init__(self, l, q):
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
		self.a1 = Vector( self.l[0] * math.cos(q[0]), self.l[0] * math.sin(q[0]))
		self.a2 = a1 + Vector( self.l[1] * math.cos(q[0] + q[1]), self.l[1] * math.sin(q[0] + q[1]))
		self.a3 = a2 + Vector( self.l[2] * math.cos(q[0] + q[1] + q[2]), self.l[2] * math.sin(q[0] + q[1] + q[2]))
		self.link1 = Line(Vector(0.0, 0.0), a1)
		self.link2 = Line(a1, a2)
		self.link3 = Line(a2, a3)

	def inverseKinematics(self, x):
		X2 = x(1) - self.l(3) * math.cos(x(3));      																		#X2 = X - L3cos(theta)
	    Y2 = x(2) - self.l(3) * math.sin(x(3));           																	#Y2 = Y - L3cos(theta)
	    det = X2**2 + Y2**2;                      																			#det = X2 ^ 2 + Y2 ^ 2
	    Q1 = math.acos(X2/sqrt(det)) + math.acos((self.l(1)**2 - self.l(2)**2 + det) / (2 * self.l(1) * math.sqrt(det)));  	#Law of Cosines
	    Q2 = pi + math.acos((self.l(1)**2 + self.l(2)**2 - det)/(2 * self.l(1) * self.l(2)));								#Law of Cosines
	    Q3 = x(3) - Q1 - Q2;                  														 						#theta3 = theta - theta1 - theta2
	    return [Q1, Q2, Q3];      			  																				#CaLcuLate q_i from X