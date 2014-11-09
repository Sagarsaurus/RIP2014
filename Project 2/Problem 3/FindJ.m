l = [2 2 1];
q = sym('q', [1 3]);
x = sym('x', [1 3]);
c = cos(q);
s = sin(q);
f = [l(1)*cos(q(1)) + l(2) * cos(q(1) + q(2)) + l(3) * cos(q(1) + q(2) + q(3));
     l(1)*sin(q(1)) + l(2) * sin(q(1) + q(2)) + l(3) * sin(q(1) + q(2) + q(3));
               q(1) +                    q(2) +                           q(3)]
    
J = jacobian(f, q)


x_i =  [2.6, 1.3,  1.0];
x_f = [-1.4 1.6, -2.0];

%Inverse Kinematics of initial configuration
X2 = x_i(1) - l(3) * cos(x_i(3));      %X2 = X - l3cos(theta)
Y2 = x_i(2) - l(3) * sin(x_i(3));      %Y2 = Y - l3cos(theta)
det = X2^2 + Y2^2;                   %det = X2 ^ 2 + Y2 ^ 2
Q1 = acos(X2/sqrt(det)) + acos((l(1)^2 - l(2)^2 + det) / (2 * l(1) * sqrt(det)));
Q2 = pi + acos((l(1)^2 + l(2)^2 - det)/(2 * l(1) * l(2)));
Q3 = x_i(3) - Q1 - Q2;                  %theta3 = theta - theta1 - theta2

qV = [Q1, Q2, Q3]      %Calculate q_i from x_i

qV * 180 / (pi)
double(subs(f, q, qV))

delta_x = x_f - x_i;
timeSteps = 1000;
dX = delta_x / timeSteps;
dq = zeros(timeSteps, 3);
X = zeros(timeSteps, 3);
for i = 1 : timeSteps
    jV = double(subs(J, q, qV));
    invJ = inv(jV);
    dq(i,:) = invJ * dX';
    qV = qV + dq(i,:);
    X(i,:)= double(subs(f, q, qV));
end

double(subs(f, q, qV))

figure
axis([-2, 3, 0, 3])
plot(X(:,1), X(:,2))