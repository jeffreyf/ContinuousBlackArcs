function [result] = fitness1(vertices, edge, alpha, beta, gamma, xytilde)
% This function uses to evaluate the fitness function
% compute theta
x = vertices(:,1);
y = vertices(:,2);
n_v = length(x);
n_e = length(edge);
xtilde = xytilde(1:size(x));
ytilde = xytilde(size(x)+1:end);

theta = zeros(size(n_e));

for i = 1:n_e
    node1 = edge(i,1)+1;
    node2 = edge(i,2)+1;
    theta(i) = atan((xtilde(node2)-xtilde(node1))/(ytilde(node2))-xtilde(node1));
end

% compute fitness function
result = 0;
for i = 1:n_v
    result = result + alpha*((xtilde(i)-x(i))^2 + (ytilde(i)-y(i))^2);
end

for j = 1:n_e
    result = result + beta*(theta(j) - theta(j))^2 + gamma*(sin(8*theta(j)))^2;
end


end