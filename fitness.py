from numpy import *
from math import *
from import_data import get_vertices_edges, from_json_file, save_json_file
import scipy.optimize as opt

def fitness_function1(xytilde,args):
    # Evaluate fitness function

    if shape(args)[0] == 1:
        args = args[0]
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
    alpha = 10.0
    beta = 2.0
    gamma = 3.0

    # Import some data
    filename = 'data/map_1.json'
    vertices, edges = get_vertices_edges(filename)

    # Re-arrange data
    x = vertices[:, 0]
    y = vertices[:, 1]
    n_v = size(x)
    
    n_e = shape(edges)[0]
    theta = zeros(n_e)
    for j in range(n_e):
        node1 = edges[j,0]
        node2 = edges[j,1]
        theta[j] = arctan2(x[node2]-x[node1],y[node2]-y[node1])

    # Create test array as initial data
    xy = concatenate((x,y))

    print('Original function value is ',fitness_function1(xy,[x,y,edges,theta,alpha,beta,gamma]))
    # Optimize call
    #res = opt.minimize(fitness_function1,xy,args=[x,y,edges,theta,alpha,beta,gamma], method='Powell', options={'disp':True})
    # Try basinhopping
    #res = opt.basinhopping(fitness_function1,xy,minimizer_kwargs={"method":"Powell","args":[x,y,edges,theta,alpha,beta,gamma],"options":{'disp':False}},disp=True,stepsize=2.0)
    # Try Differential Evolution
    bounds = zeros((size(xy),2))
    for i in range(size(xy)):
        bounds[i] = (xy[i]-10,xy[i]+10)
    res = opt.differential_evolution(fitness_function1,bounds,args=[[x,y,edges,theta,alpha,beta,gamma]], disp=True)
    
    
    # Extract solution
    xtilde = res.x[0:n_v]
    ytilde = res.x[n_v:]


    # Postprocess and compute new theta's
    thetatilde = zeros(n_e)
    for j in range(n_e):
        node1 = edges[j,0]
        node2 = edges[j,1]
        thetatilde[j] = arctan2(xtilde[node2]-xtilde[node1],ytilde[node2]-ytilde[node1])

    # Compute terms of fitness functional
    fitness1 = 0.0
    for i in range(n_v):
        fitness1 += alpha*((xtilde[i]-x[i])**2 + (ytilde[i]-y[i])**2)
    fitness2 = 0.0
    fitness3 = 0.0
    for j in range(n_e):
        fitness2 += beta*(thetatilde[j]-theta[j])**2
        fitness3 += gamma*(sin(8*thetatilde[j]))**2
        
    print('Movement of nodes:')
    print(xtilde-x)
    print(ytilde-y)

    print('Original angles, followed by new angles:')
    print(theta)
    print(thetatilde)

    print('fitness functional term1 = ',fitness1,', term2 = ',fitness2,', term3 = ',fitness3)


    # Put it into a dictionary
    vertices = []
    for xtilde, ytilde in zip(xtilde, ytilde):
        vertices.append({'x' : xtilde, 'y' : ytilde})
    
    # Hack: All we need to do is replace the vertices from the original file
    json_object = from_json_file(filename)
    json_object['vertices'] = vertices
    
    #print(json_object)
    save_json_file(json_object, "optimized.json")


if __name__ == "__main__":
    main()
