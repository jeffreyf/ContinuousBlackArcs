from numpy import *
from math import *
from import_data import get_vertices_edges, from_json_file, save_json_file, convert_edges, convert_vertices
import scipy.optimize as opt
import matplotlib.pyplot as plt
from data_processing import *
import time

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
    
    if len(args) > 7:
        cb = args[7]
    else:
        cb = None

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
        fitness += gamma*((sin(8*thetatilde[j]))**2+(sin(2*thetatilde[j]))**2)
        
    if cb is not None:
        # The call back takes arguments vertices, edges, frequency
        cb(vertices_from_tilde(xtilde, ytilde), edges)

    return fitness    

def pre_process_data(filename='data/map_1.json', do_rotation=True):
    clear_gif_staging()
    original_json_object = from_json_file(filename)
    vertices, edges = convert_vertices(original_json_object), convert_edges(original_json_object)
    # Grab the histogram data
    if do_rotation:
        theta = calculate_desired_theta(vertices, edges)
        print("Rotating using theta {}".format(theta))
        # HARD CODED ROTATION
        vertices = rotate_vertices(vertices, theta)
        
        original_json_object = set_json_vertices(original_json_object, vertices)
        save_json_file(original_json_object, "original_rotated.json")
        
    
    return vertices, edges, original_json_object

def post_optimization_plotting(json_object, vertices, edges, new_vertices=None):
    if json_object is not None:
        plot_map(json_object)
    elif new_vertices is not None:
        plot_vertices_edges(new_vertices, edges, 'C0-o')
    plot_vertices_edges(vertices, edges, 'C1--')
    plt.show()
    

def main():
    filename = 'data/map_2.json'
    vertices, edges, original_json_object = pre_process_data(filename, True)
    cb = None# make_plot_callback(vertices, edges)#None #plot_and_save_vertices_edges
    json_object = driver(filename, vertices=vertices, edges=edges,
                         cb=cb)
    
    post_optimization_plotting(json_object, vertices, edges)
    
    
def get_initial_arguments(vertices, edges, alpha, beta, gamma, cb):
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
    
    return x, y, theta, xy, n_v, n_e, [x,y,edges,theta,alpha,beta,gamma, cb]

def driver(filename='data/map_1.json', vertices=None, edges=None, cb=None):
    """
    Either pass in a jsonfilename, or vertices and edges
    """
    # Routine to run as test
    # Import some data
    if vertices is None or edges is None:
        print("Getting vertices edges from file")
        vertices, edges = get_vertices_edges(filename)

    # total guess at weights
    alpha = 1.0e-5
    beta = 1.0e-1
    gamma = 1.0
    
    x, y, theta, xy, n_v, n_e, args = get_initial_arguments(vertices, edges, alpha, beta, gamma, cb)

    start_time = time.time()

    print('Original function value is ',fitness_function1(xy,args),' map has ',n_v,' vertices and ',n_e,' edges')
    # Optimize call
    res = opt.minimize(fitness_function1,xy,args=args, method='Powell', options={'disp':True})
    # Try basinhopping
    #res = opt.basinhopping(fitness_function1,xy,minimizer_kwargs={"method":"Powell","args":[x,y,edges,theta,alpha,beta,gamma],"options":{'disp':False}},disp=True,stepsize=2.0)
    # Try Differential Evolution
    """bounds = zeros((size(xy),2))
    for i in range(size(xy)):
        bounds[i] = (xy[i]-50,xy[i]+50)
    res = opt.differential_evolution(fitness_function1,bounds,args=[[x,y,edges,theta,alpha,beta,gamma]], disp=True)
    """

    end_time = time.time()
    print('Elapsed time is ',end_time-start_time)
    
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

    #print('fitness functional term1 = ',sum(fitness1),', term2 = ',sum(fitness2),', term3 = ',sum(fitness3))
    #print('fitness functional medians term1 = ',median(fitness1),', term2 = ',median(fitness2),', term3 = ',median(fitness3))

    #print('final fitness',fitness_function1(res.x), args)    
    # Put it into a dictionary
    vertices = []
    for xtilde_, ytilde_ in zip(xtilde, ytilde):
        vertices.append({'x' : xtilde_, 'y' : ytilde_})
    
    # Hack: All we need to do is replace the vertices from the original file
    json_object = from_json_file(filename)
    json_object['vertices'] = vertices
    
    #print(json_object)
    save_json_file(json_object, "optimized.json")
    
    if cb is not None:
        cb(vertices_from_tilde(xtilde, ytilde), edges, frequency=1)

    return json_object



if __name__ == "__main__":
    main()
