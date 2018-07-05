# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:32:00 2018

@author: codej
"""

import numpy as np
from deap import base, creator, benchmarks, cma, tools, algorithms
from fitness import fitness_function1, get_initial_arguments, pre_process_data, post_optimization_plotting
from data_processing import vertices_from_tilde

def make_fitness_function(args):
    
    def fitness(xytilde):
        return (fitness_function1(xytilde, args),)
    
    return fitness


def run_cma(vertices, edges, alpha, beta, gamma, cb):
    """
    Runs a CMA-ES
    """
    
    ### SETUP
    x, y, theta, xy, n_v, n_e, args = get_initial_arguments(vertices, edges, alpha, beta, gamma, cb)
    
    fitness_function = make_fitness_function(args)
    
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    
    toolbox = base.Toolbox()
    toolbox.register("evaluate", fitness_function)

    ### RUNNING
    np.random.seed(128)
    N = len(xy)
    
    strategy = cma.Strategy(centroid=[0.5] * N, sigma=5.0, lambda_=20*N)
    toolbox.register("generate", strategy.generate, creator.Individual)
    toolbox.register("update", strategy.update)
    
    hof = tools.HallOfFame(1)
    
    stats = tools.Statistics(lambda ind : ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    algorithms.eaGenerateUpdate(toolbox, ngen=250, stats=stats, halloffame=hof)
    
    return hof
    
if __name__ == "__main__":
    filename = 'data/map_1.json'
    
    # total guess at weights
    alpha = 1.0e-7
    beta = 1.0e-3
    gamma = 1.0
    
    vertices, edges, original_json_object = pre_process_data(filename, False)
    cb = None# make_plot_callback(vertices, edges)#None #plot_and_save_vertices_edges
    hof = run_cma(vertices, edges, alpha, beta, gamma, cb)
    
    # Extract solution
    n_v = int(len(hof.items[0]) / 2)
    xtilde = hof.items[0][0:n_v]
    ytilde = hof.items[0][n_v:]
    
    new_vertices = vertices_from_tilde(xtilde, ytilde)
    
    post_optimization_plotting(None, vertices, edges, new_vertices)