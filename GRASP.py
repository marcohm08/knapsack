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

def grasp(benefits, weights, capacity, maxIterations = 10000, coef = 0.7):

    maxBenefit = -1
    iterations = 0

    while maxIterations != iterations:

        iterations += 1
        auxSol = greedyRandomized(benefits, weights, capacity, coef)
        auxSol, auxBenefit = localSearch(auxSol, benefits, weights, capacity)

        if auxBenefit > maxBenefit:
            solution = auxSol[:]
            maxBenefit = auxBenefit

    return solution, maxBenefit, iterations

def getDataInstance(testName):

    testName = repr(testName).replace("'", "")
    benefits = []
    weights = []

    with open(testName) as file:

        firstLine = True
        
        for line in file.readlines():
            
            data = line.split(" ")
            
            if firstLine:
                firstLine = False
                n = int(data[0])
                capacity = int(data[1])
                opt = int(data[2])            
            elif n > 0:
                n -= 1
                benefits = benefits + [int(data[0])]
                weights = weights + [int(data[1])]

    return capacity, opt, benefits, weights

if __name__ == "__main__":

    instances = ['../pruebas/inst_10.txt', '../pruebas/inst_20.txt', '../pruebas/inst_100.txt', '../pruebas/inst_200.txt', '../pruebas/inst_500.txt']
    """
    solucion de 11 ejecucion
    los tiempos de cada ejecucion
    11 errores de ejecución
    lista de soluciones en cada iteracion las 11 ejecuciones en una unica lista
    """

    for instance in instances:
        capacity, opt, benefits, weights = getDataInstance(instance)
        solution, benefit, iterations = grasp(benefits, weights, capacity)
