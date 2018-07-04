# -*- coding: utf-8 -*-
"""
Import generated data
"""

import json
from pathlib import Path
import numpy as np

def get_json_files_in_directory(directory):
    """
    Returns all the json files in the directory
    """
    path = Path(directory)
    json_files = [json_file for json_file in path.iterdir() if json_file.suffix == ".json"]
    
    return json_files

def from_json_string(string):
    """
    Returns an experiment's data from the given json string
    """
    return json.loads(string)
    
    
def from_json_file(path):
    """
    Returns the experiment data from the json file at the given path
    """
    with open(path) as file:
        data = json.load(file)
    return data
    

def from_directory(directory):
    """
    Returns a list of all experiment data in the given directory
    """
    data = []
    for file in get_json_files_in_directory(directory):
        data.append(from_json_string(file.read_text()))
        
    return data

def convert_vertices(json_object):
    vertices = []
    for vertex in json_object['vertices']:
        vertices.append([vertex['x'], vertex['y']])
    
    return np.array(vertices)

def convert_edges(json_object):
    vertices = []
    for vertex in json_object['edges']:
        vertices.append([vertex['v1'], vertex['v2']])
    
    return np.array(vertices)
    

def get_vertices_edges(filepath):
    """
    Returns the vertices and edges in the json file found at filepath
    """
    json_object = from_json_file(filepath)
    
    return convert_vertices(json_object), convert_edges(json_object)

def save_json_file(json_object, filename):
    """
    Saves the json object to filename
    """
    with open(filename, 'w') as file:
        json.dump(json_object, file)