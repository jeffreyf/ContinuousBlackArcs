# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 12:26:40 2018

@author: codej
"""
from import_data import get_vertices_edges
import numpy as np
import os

map1_vertices, map1_edges = get_vertices_edges('data/map_4_50_nodes.json')
map2_vertices, map2_edges = get_vertices_edges('data/map_5_100_nodes.json')
map3_vertices, map3_edges = get_vertices_edges('data/map_6_downtown.json')
#os.mkdir('data/csv')
np.savetxt('data/csv/map_4_50_nodes_vertices.csv', map1_vertices, delimiter=",")
np.savetxt('data/csv/map_5_100_nodes_vertices.csv', map2_vertices, delimiter=",")
np.savetxt('data/csv/map_6_downtown_vertices.csv', map3_vertices, delimiter=",")
np.savetxt('data/csv/map_4_50_nodes_edges.csv', map1_edges, delimiter=",")
np.savetxt('data/csv/map_5_100_nodes_edges.csv', map2_edges, delimiter=",")
np.savetxt('data/csv/map_6_downtown_edges.csv', map3_edges, delimiter=",")
np.savetxt('data/csv/map_4_50_nodes_edges.csv', map1_edges, "%d", delimiter=",")
np.savetxt('data/csv/map_5_100_nodes_edges.csv', map2_edges, "%d",delimiter=",")
np.savetxt('data/csv/map_6_downtown_edges.csv', map3_edges, "%d", delimiter=",")