function [ Q ] = InverseKinematics( X, L)
    X2 = X(1) - L(3) * cos(X(3));      %X2 = X - L3cos(theta)
    Y2 = X(2) - L(3) * sin(X(3));      %Y2 = Y - L3cos(theta)
    det = X2^2 + Y2^2;                   %det = X2 ^ 2 + Y2 ^ 2
    Q1 = acos(X2/sqrt(det)) + acos((L(1)^2 - L(2)^2 + det) / (2 * L(1) * sqrt(det)));
    Q2 = pi + acos((L(1)^2 + L(2)^2 - det)/(2 * L(1) * L(2)));
    Q3 = X(3) - Q1 - Q2;                  %theta3 = theta - theta1 - theta2
    Q = [Q1, Q2, Q3];      %CaLcuLate q_i from X
end

