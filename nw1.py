import cvxpy as cp
import numpy as np
import cplex
import docplex.mp.model as cpx


opt_model = cpx.Model(name="MIP Model")
set_k = []
set_i = []
set_j = []
set_h = []

w = [[[0 for x in range(24)] for x in range(2)] for x in range(3)]
for i in range(3):
    set_i.append(i)
    for j in range(2):
        set_j.append(j)
        for h in range(24):
            set_h.append(h)
            w[i][j][h] = i+j+h

m = [[[0 for x in range(24)] for x in range(2)] for x in range(3)]
for i in range(3):
    for j in range(2):
        for h in range(24):
            m[i][j][h] = i+j+h


l_dictionary = {}
for k in range(2):
    set_k.append(k)
    for h in range(24):
            l_dictionary[(k,h)] = opt_model.continuous_var(name="l_{0}_{1}".format(k,h))

nin = {}
for k in range(2):
        for h in range(24):
                nin[(k,h)] = opt_model.continuous_var(name="nin_{0}_{1}".format(k,h))

nout = {}
for k in range(2):
        for h in range(24):
                nout[(k,h)] = opt_model.continuous_var(name="nout_{0}_{1}".format(k,h))
g = {}
for i in range(3):
    for j in range(2):
        for h in range(24):
            g[(i,j,h)] = opt_model.continuous_var(name="g_{0}_{1}_{2}".format(i,j,h))

constraints = {h :
opt_model.add_constraint(
ct=opt_model.sum( w[i][j][h] for j in set_j for i in set_i) >= opt_model.sum( l_dictionary[k,h] for k in set_k),
ctname="constraint_{0}".format(h))
    for h in set_h}

objective = opt_model.sum(l_dictionary[k,h]
                          for k in set_k
                          for h in set_h)

opt_model.maximize(objective)

opt_model.solve()
for k in range(2):
    for h in range(24):
        print((l_dictionary[k,h]).solution_value)
