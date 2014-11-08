stepSize = 2 * pi / 100;
syms q1 q2 q3 l1 l2 l3
c1 = cos(q1);
c2 = cos(q2);
c3 = cos(q3);
s1 = sin(q1);
s2 = sin(q2);
s3 = sin(q3);
T1 = [c1, -s1,    0; s1, c1, 0; 0, 0, 1];
T2 = [c2, -s2, l1; s2, c2, 0; 0, 0, 1];
T3 = [c2, -s2, l2; s2, c2, 0; 0, 0, 1];
T4 = [ 1,   0, l3;  0,  2, 0; 0, 0, 1];
f  = T1 * T2 * T3 * T4;
J = jacobian(f, [q1, q2, q3]);
