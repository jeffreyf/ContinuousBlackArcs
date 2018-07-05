# -*- coding: utf-8 -*-
"""
Data processing functions
"""

from numpy import *
import matplotlib.pyplot as plt
from import_data import get_vertices_edges, from_json_file, save_json_file, convert_edges, convert_vertices


def rotate_vertices(vertices, theta):
    rotation = matrix([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
    rotated = matmul(rotation, vertices.transpose())
    vertices = array(rotated.transpose())
    return vertices
    
def calculate_desired_theta(vertices, edges):
    """
    Experimental
    """
    h = plot_thetas(vertices, edges)
    plt.show()
    top_indices = flip(argsort(h[0]), axis=0)[:1]
    avg = average(h[1][top_indices], weights=h[0][top_indices])
    theta = pi / 2 - avg
    theta = -theta
    return theta

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
