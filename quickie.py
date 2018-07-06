# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 08:29:45 2018

@author: codej
"""
from fitness import get_initial_arguments
from numpy import *

x, y, theta, xy, n_v, n_e, args = get_initial_arguments(vertices, edges, alpha, beta, gamma, cb)

# Postprocess and compute new theta's
thetatilde = zeros(n_e)
for j in range(n_e):
    node1 = edges[j,0]
    node2 = edges[j,1]
    thetatilde[j] = arctan2(xtilde[node2]-xtilde[node1],ytilde[node2]-ytilde[node1])

fitness1 = []
for i in range(n_v):
    fitness1.append(alpha*((xtilde[i]-x[i])**2 + (ytilde[i]-y[i])**2))
fitness2 = []
fitness3 = []
for j in range(n_e):
    fitness2.append(beta*(thetatilde[j]-theta[j])**2)
    fitness3.append(gamma*(sin(8*thetatilde[j]))**2)
    
print('fitness functional term1 = ',sum(fitness1),', term2 = ',sum(fitness2),', term3 = ',sum(fitness3))