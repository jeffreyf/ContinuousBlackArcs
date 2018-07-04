function [x, fval, output] = fitness1(xytilde, edge, alpha, theta, gamma)
% This function uses to evaluate the fitness function

[x, y] = csvread('data/map_1.csv');

n_v = length(x);
n_e = length(theta);
xtilde = xytilde(1:n_v);
ytilde = xytilde((n_v+1):(2*n_v));

% compute theta
thetatilde = zeros(size(edge));
for i = 1:n_e
    node1 = edge(i);
    node2 = edge(i+1);
    thetatilde(i) = atan((xtilde(node2)-xtilde(node1))/(ytilde(node2))-xtilde(node1));
end

% compute fitness function
for i = 1:n_v
    fitness = fitness + alpha*((xtilde(i)-x(i))^2 + (ytilde(i)-y(i))^2);
end

for j = 1:n_e
    fitness = fitness + beta*(theta(j) - thetatilde(j))^2;
    fitness = fitness + gamma*(sin(8*thetatilde(j)))^2;
end

options = optimset('Display', 'iter');
[x, fval, output] = fminsearch(@fitness, xytilde, options);

end