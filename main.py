from funciones.GRASP import grasp
from funciones.auxiliary import getDataInstance
from funciones.graph import graficarTres
import pandas as pd
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":

    instances = [r'./pruebas/inst_10.txt', r'./pruebas/inst_20.txt', r'./pruebas/inst_100.txt', r'./pruebas/inst_200.txt', r'./pruebas/inst_500.txt']
    """
    solucion de 11 ejecucion
    los tiempos de cada ejecucion
    11 errores de ejecución
    lista de soluciones en cada iteracion las 11 ejecuciones en una unica lista
    """

    for instance in instances:
        
        timesInstance = [0] * 11
        errorsInstance = [0] * 11
        benefitsInstance = [0] * 11

        capacity, opt, benefits, weights = getDataInstance(instance)

        print(len(weights))

        for i in range(11):
            print(len(weights), i + 1)
            start = time.time()
            solution, benefit, iterations = grasp(benefits, weights, capacity)
            
            timesInstance[i] = time.time() - start
            benefitsInstance[i] = benefit
            errorsInstance[i] = abs(benefit - opt) / opt
        
        graficarTres(benefitsInstance, timesInstance, errorsInstance)
        plt.savefig(str(len(weights))+"_GRASP")
    plt.show()