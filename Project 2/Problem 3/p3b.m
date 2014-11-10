l = [2 2 1];
q = sym('q', [1 3]);
x = sym('x', [1 3]);
y = sym('y', [1 2]);
c = cos(q);
s = sin(q);

C = [2, 2.25];
R = 1;

kp = 0.5;
alt = 1.4

fx1(q) = l(1)*cos(q(1)); 
fy1(q) = l(1)*sin(q(1));
fx2(q) = fx1 + l(2) * cos(q(1) + q(2));
fy2(q) = fy1 + l(2) * sin(q(1) + q(2));
fx3(q) = fx2 + l(3) * cos(q(1) + q(2) + q(3));
fy3(q) = fy2 + l(3) * sin(q(1) + q(2) + q(3));
ft(q) = q(1) + q(2) +  q(3);
f(q) = [fx3; fy3; ft];
    
J = jacobian(f, q);


x_i = [ 2.6, 1.3,  1.0];
x_f = [-1.4, 1.6, -2.0];

xV = x_i;

dist(y) = sqrt((x_f(1) - y(1))^2 + (x_f(2) - y(2))^2);
fieldPot(y) = sqrt((C(1) - y(1))^2 + (C(2) - y(2))^2)
angle(y) = atan2(C(2) - y(2), C(1) - y(1));

qVi = InverseKinematics(x_i, l);

timeSteps = 1000;
qV = qVi;
dq = zeros(timeSteps, 3);
X1 = zeros(timeSteps, 2);
X2 = zeros(timeSteps, 2);
X3 = zeros(timeSteps, 2);
figure
for i = 1 : timeSteps
    i;
    jV = double(J(qV(1), qV(2), qV(3)));
    dX = ((x_f - xV) / (timeSteps - i + 1))';
    invJ = inv(jV);
    x1 = double([fx1(qV(1), qV(2), qV(3)), fy1(qV(1), qV(2), qV(3))]);
    x2 = double([fx2(qV(1), qV(2), qV(3)), fy2(qV(1), qV(2), qV(3))]);
    x3 = double([fx3(qV(1), qV(2), qV(3)), fy3(qV(1), qV(2), qV(3))]);
    d = double(dist(x3(1), x3(2)));
    Xs = [x1; x2; x3];
    add = [0 0 0];
    for j = 1 : 3
        x = Xs(j,:);
        fx = 0;
        fy = 0;
        fp = double(fieldPot(x(1), x(2)));
        ang = double(angle(x(1), x(2)));
        if fp < R
            fx = -sign(cos(ang)) * Inf;
            fy = -sign(sin(ang)) * Inf;
        elseif fp < alt * R
             fx = -0.1 * (alt * R - fp) * cos(ang);
             fy = -0.1 * (alt * R - fp) * sin(ang);
        end
        add(j) = kp * sqrt(fx^2 + fy^2) * (x_f(j) - xV(j));
    end
    dq(i,:) = invJ * dX;
    dq(i,:) = dq(i,:) + add;
    qV = qV + dq(i,:);
    X1(i,:) = x1;
    X2(i,:) = x2;
    X3(i,:) = x3;
    xV = [X3(i,:), sum(qV)]
    X = [zeros(timeSteps, 1), X1(:,1), X2(:,1), X3(:,1)];
    Y = [zeros(timeSteps, 1), X1(:,2), X2(:,2), X3(:,2)];
    
    clf
    plot(X3(:,1), X3(:,2), 'Color', 'green')
    line(X(i,:), Y(i,:));
    viscircles(C,R);
    axis manual
    axis([-2, 3, 0, 3]);
end
double(subs(f, q, qV))

while 1
    for i = 1 : timeSteps
        clf
        plot(X3(:,1), X3(:,2), 'Color', 'green')
        line(X(i,:), Y(i,:));
        viscircles(C,R);
        axis manual
        axis([-2, 3, 0, 3]);
        pause(1/600);
    end
end