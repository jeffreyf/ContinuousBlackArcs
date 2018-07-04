from numpy import *
from math import *
from import_data import get_vertices_edges, from_json_file, save_json_file, convert_edges, convert_vertices
import scipy.optimize as opt
import matplotlib.pyplot as plt

def deviation(theta):
    # Compute maximum deviation from integer value

    # Take fractional part of theta/(pi/8)
    fractional_part = (theta*8/pi) % 1.0

    n_e = size(theta)
    dev_value = zeros(n_e)
    for i in range(n_e):
        dev_value[i] = min(fractional_part[i],1.0-fractional_part[i])
    
    plt.hist(dev_value, 30)
    plt.show()
    return max(dev_value)

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
    do_rotation = False
    filename = 'data/map_3.json'
    vertices, edges = get_vertices_edges(filename)
    # Grab the histogram data
    if do_rotation:
        h = plot_thetas(vertices, edges)
        plt.show()
        top_indices = flip(argsort(h[0]), axis=0)[:5]
        avg = average(h[1][top_indices], weights=h[0][top_indices])
        theta = pi / 2 - avg
        theta = -theta
        print("Rotating using theta {}".format(theta))
        # HARD CODED ROTATION
        rotation = matrix([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
        rotated = matmul(rotation, vertices.transpose())
        vertices = array(rotated.transpose())
        
    json_object = driver(filename, vertices=vertices, edges=edges)
    plot_map(json_object)
    plot_vertices_edges(vertices, edges, 'C1--')
    plt.show()
    
def driver(filename='data/map_1.json', vertices=None, edges=None):
    """
    Either pass in a jsonfilename, or vertices and edges
    """
    # Routine to run as test

    # total guess at weights
    alpha = 1.0e-5
    beta = 2.0
    gamma = 1.0

    # Import some data
    if vertices is None or edges is None:
        print("Getting vertices edges from file")
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
    res = opt.minimize(fitness_function1,xy,args=[x,y,edges,theta,alpha,beta,gamma], method='Powell', options={'disp':True})
    # Try basinhopping
    #res = opt.basinhopping(fitness_function1,xy,minimizer_kwargs={"method":"Powell","args":[x,y,edges,theta,alpha,beta,gamma],"options":{'disp':False}},disp=True,stepsize=2.0)
    # Try Differential Evolution
    """bounds = zeros((size(xy),2))
    for i in range(size(xy)):
        bounds[i] = (xy[i]-50,xy[i]+50)
    res = opt.differential_evolution(fitness_function1,bounds,args=[[x,y,edges,theta,alpha,beta,gamma]], disp=True)
    """
    
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
    fitness1 = []
    for i in range(n_v):
        fitness1.append(alpha*((xtilde[i]-x[i])**2 + (ytilde[i]-y[i])**2))
    fitness2 = []
    fitness3 = []
    for j in range(n_e):
        fitness2.append(beta*(thetatilde[j]-theta[j])**2)
        fitness3.append(gamma*(sin(8*thetatilde[j]))**2)
        
    print('Max node movement is ',sqrt(max((xtilde-x)**2+(ytilde-y)**2)))

    print('Max deviation from multiple of pi/8 in original map is ',deviation(theta),' for optimized map is ',deviation(thetatilde))

    print('fitness functional term1 = ',sum(fitness1),', term2 = ',sum(fitness2),', term3 = ',sum(fitness3))
    print('fitness functional medians term1 = ',median(fitness1),', term2 = ',median(fitness2),', term3 = ',median(fitness3))


    # Put it into a dictionary
    vertices = []
    for xtilde, ytilde in zip(xtilde, ytilde):
        vertices.append({'x' : xtilde, 'y' : ytilde})
    
    # Hack: All we need to do is replace the vertices from the original file
    json_object = from_json_file(filename)
    json_object['vertices'] = vertices
    
    #print(json_object)
    save_json_file(json_object, "optimized.json")

    return json_object

def vertices_into_json(vertices, filename):
    
    # Hack: All we need to do is replace the vertices from the original file
    json_object = from_json_file(filename)
    json_object['vertices'] = vertices
    
    return json_object

def plot_vertices_edges(vertices, edges, plot_arg='C0-o'):
    for edge in edges:
        vertex1 = vertices[edge[0]]
        vertex2 = vertices[edge[1]]
        plt.plot([vertex1[0], vertex2[0]], [vertex1[1], vertex2[1]], plot_arg)

def plot_map(json_object, plot_arg='C0-o'):
    vertices = convert_vertices(json_object)
    edges = convert_edges(json_object)
    for edge in edges:
        vertex1 = vertices[edge[0]]
        vertex2 = vertices[edge[1]]
        plt.plot([vertex1[0], vertex2[0]], [vertex1[1], vertex2[1]], plot_arg)


def get_thetas(vertices, edges):
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
        
    return theta

def plot_thetas_from_filename(filename, bins=20):
    vertices, edges = get_vertices_edges(filename)
    return plot_thetas(vertices, edges, bins)

def plot_thetas(vertices, edges, bins=20):
    theta = get_thetas(vertices, edges)
    return plt.hist(theta % (pi / 2), bins)


if __name__ == "__main__":
    main()
