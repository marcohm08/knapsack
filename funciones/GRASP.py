"""
Pep 2 Optimización en Ingeniería
Autor:
    > Marco Hernández
    > Alexis Quintana
Profesor:
    > Mario Inostroza
Ayudante:
    > Cristian Sepulveda
Metaheuristicas:
    > GRASP
    > 
"""

from distutils.log import error
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from pip import main
from importlib.resources import path
import pandas as pd

def evaluateSol(sol, benefits, weights):
    
    n = len(weights)
    weight = 0
    benefit = 0

    for i in range(n):
        benefit += benefits[i] * sol[i]
        weight += weights[i] * sol[i]
    
    return benefit, weight

def greedyRandomized(benefits, weights, capacity, coef):

    n = len(weights)
    sol = [0] * n
    ratio = [0] * n
    changeTheSol = True
    benefit = 0

    for i in range(n):
        ratio[i] = benefits[i] / weights[i]
    
    while changeTheSol:

        objects = []
        criterion = max(ratio) * coef

        for i in range(n):
            
            if ratio[i] >= criterion and weights[i] <= capacity:
                objects.append(i)
            
        if len(objects) == 0:
            changeTheSol = False
        else:
            choice = random.choice(objects)
            ratio[choice] = 0
            sol[choice] = 1
            benefit += benefits[choice]
            capacity -= weights[choice]

    return sol

def localSearch(initialSol, benefits, weights, capacity):

    n = len(weights)
    aux = initialSol[:]
    initialBenefit, initialWeight = evaluateSol(initialSol, benefits, weights)
    maxBenefit = initialBenefit
    maxWeight = initialWeight
    solution = initialSol[:]
    
    for i in range(n):

        benefitAux = maxBenefit
        weightAux = maxWeight
        
        if aux[i] == 0:
            aux[i] = 1
            benefitAux = initialBenefit + benefits[i]
            weightAux = initialWeight + weights[i]       
        elif aux[i] == 1:
            aux[i] = 0
            benefitAux = initialBenefit - benefits[i]
            weightAux = initialWeight - weights[i]

        if weightAux <= capacity and benefitAux > maxBenefit:
            maxBenefit = benefitAux
            maxWeight = weightAux
            solution = aux[:]
            
        
        aux[i] = int(not aux[i])


    return solution, maxBenefit

def grasp(benefits, weights, capacity, maxIterations = 10000, coef = 0.6):

    maxBenefit = -1
    iterations = 0
    benefitsIterations =  []
    noImprovement = len(weights) * coef

    while maxIterations != iterations and noImprovement > 0:

        iterations += 1
        auxSol = greedyRandomized(benefits, weights, capacity, coef)
        auxSol, auxBenefit = localSearch(auxSol, benefits, weights, capacity)

        if auxBenefit > maxBenefit:
            noImprovement = len(weights) * coef
            solution = auxSol[:]
            maxBenefit = auxBenefit
        else:
            noImprovement -= 1

        benefitsIterations.append(maxBenefit)
    return solution, maxBenefit, iterations, benefitsIterations

# if __name__ == "__main__":

#     instances = [r'./pruebas/inst_10.txt', r'./pruebas/inst_20.txt', r'./pruebas/inst_100.txt', r'./pruebas/inst_200.txt', r'./pruebas/inst_500.txt']
#     """
#     solucion de 11 ejecucion
#     los tiempos de cada ejecucion
#     11 errores de ejecución
#     lista de soluciones en cada iteracion las 11 ejecuciones en una unica lista
#     """

#     for instance in instances:
        
#         timesInstance = [0] * 11
#         errorsInstance = [0] * 11
#         benefitsInstance = [0] * 11

#         capacity, opt, benefits, weights = getDataInstance(instance)

#         print(len(weights))

#         for i in range(11):
#             print(len(weights), i + 1)
#             start = time.time()
#             solution, benefit, iterations = grasp(benefits, weights, capacity)
            
#             timesInstance[i] = time.time() - start
#             benefitsInstance[i] = benefit
#             errorsInstance[i] = abs(benefit - opt) / opt
        
#         graficarTres(benefitsInstance, timesInstance, errorsInstance)
#         plt.savefig(str(len(weights))+"_GRASP")
#         plt.show()
#         plt.close()