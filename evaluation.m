function [fval] = evaluation()
alpha = 1;
beta = 2;
gamma = 3;

vertices = csvread('map1_vertices.csv');
edge = csvread('map1_edges.csv');

x = vertices(:,1);
y = vertices(:,2);

n_v = length(x);
n_e = length(edge);

theta = zeros(size(n_e));

for i = 1:n_e
    node1 = edge(i,1)+1;
    node2 = edge(i,2)+1;
    theta(i) = atan((x(node2)-x(node1))/(y(node2))-(y(node1)));
end


xytilde = cat(1, x, y);


% print original function value
fun = @(xytilde)fitness1(vertices, edge, alpha, beta, gamma, xytilde);
%result = fitness1(vertices, edge, alpha, beta, gamma, xytilde);
%options = optimset('Display', 'iter');
[x, fval, ~] = fminsearch(fun, xytilde);
%fprintf('The original function value is %f', fval);
xtilde = x(1:n_v);
ytilde = x(n_v+1:end);

thetatilde = zeros(size(n_e));
for j = 1:n_e
    node1 = edge(j,1)+1;
    node2 = edge(j,2)+1;
    thetatilde(j) = atan( (xtilde(node2)-xtilde(node1))/(ytilde(node2)-ytilde(node1)) );
end
result1 = 0;
result2 = 0;
result3 = 0;
for i = 1:n_v
    result1 = result1 + alpha*((xtilde(i)-x(i))^2 + (ytilde(i)-y(i))^2);
end

for i = 1:n_e
    result2 = result2 +  beta*(theta(j) - thetatilde(j))^2;
    result3 = result3 + gamma*(sin(8*thetatilde(j)))^2;
end

%fprintf('fitness functional term1 = %f',result1,', term2 = %f',result2,', term3 = %f',result3);
%fprintf('fitness functional medians term1 = %f',median(result1),', term2 = %f',median(result2),', term3 = %f',median(result3));

end