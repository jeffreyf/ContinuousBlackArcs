from numpy import *
from math import *
from scipy import *

def fitness_function1(xytilde,args):
    # Evaluate fitness function

    x = args[0]
    y = args[1]
    edges = args[2]
    theta = args[3]
    alpha = args[4]
    beta = args[5]
    gamma = args[6]

    # Extract sizes and sub-arrays
    n_v = size(x)
    n_e = size(theta)
    xtilde = xytilde[0:n_v]
    ytilde = xytilde[n_v:]

    # Compute theta's associated with new coordinates
    thetatilde = zeros(n_e)
    for i in range(n_e) :
        node1 = edges[i,0]
        node2 = edges[i,1]
        thetatilde[i] = arctan2(xtilde[node2]-xtilde[node1],ytilde[node2]-ytilde[node1])

    # Evaluate fitness function
    fitness = 0.0
    for i in range(n_v):
        fitness += alpha*((xtilde[i]-x[i])**2 + (ytilde[i]-y[i])**2)
    for j in range(n_e):
        fitness += beta*(thetatilde[j]-theta[j])**2
        fitness += gamma*(sin(8*thetatilde[j]))**2

    return fitness
    
    
    
    
def main():
    # Routine to run as test

    # total guess at weights
    alpha = 1.0
    beta = 2.0
    gamma = 3.0

    # Create test data
    x = array([1,2,3,4,5,6])
    y = array([2,3,4,5,6,7])
    n_v = size(x)

    edges = array([[0,1],[1,2],[2,3],[3,4],[4,5]])
    n_e = shape(edges)[0]
    theta = zeros(n_e)
    for j in range(n_e):
        node1 = edges[j,0]
        node2 = edges[j,1]
        theta[j] = arctan2(x[node2]-x[node1],y[node2]-y[node1])

    # Create test array as initial data
    xy = concatenate((x,y))
    # Move something
    xy[3] = 3

    # Evaluate fitness function
    test = fitness_function1(xy,[x,y,edges,theta,alpha,beta,gamma])
    print('fitness = ', test)

    #optimize.minimize

if __name__ == "__main__":
    main()
