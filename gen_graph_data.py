import numpy as np
import json

def gen_graph_data(filepath):    
    with open(filepath) as file:
        data = json.load(file)
    
    edges_dict = data['edges']
    verts_dict = data['vertices']
    n_e = len(edges_dict)
    n_v = len(verts_dict)
    
    edges = np.array([(edge['v1'], edge['v2']) for edge in edges_dict])
    x = np.array([vert['x'] for vert in verts_dict]).reshape(n_v,1)
    y = np.array([vert['y'] for vert in verts_dict]).reshape(n_v,1)

    graph_data = {'edges': edges, 'x': x, 'y': y}

    return graph_data
