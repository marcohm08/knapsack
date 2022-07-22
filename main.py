from funciones.GRASP import grasp
from funciones.auxiliary import getDataInstance
from funciones.graph import graficar, graficarTres
from funciones.genetico import leeArchivo, ejecucionAlgoritmo, errorPorcentual
import numpy
import time
import sys
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    
    try:
        
        opcion = sys.argv[1]
    
    except IndexError:
        print('Instrucciones de uso:')
        print("python main.py <heurística a utilizar>")
        print("1: GRASP")
        print("2: Algoritmo genético")
        print("3: GRASP y Algoritmo genético")
        sys.exit(1)
        
    instances = [r'./pruebas/inst_10.txt',
                    r'./pruebas/inst_20.txt',
                    r'./pruebas/inst_100.txt',
                    r'./pruebas/inst_200.txt',
                    r'./pruebas/inst_500.txt']
    
    if opcion == '1' or opcion == '3':
        
        print("Ejecutando GRASP")

        for instance in instances:
            
            timesInstance = [0] * 11
            errorsInstance = [0] * 11
            benefitsInstance = [0] * 11
            allBenefits = []

            capacity, opt, benefits, weights = getDataInstance(instance)

            for i in range(11):

                start = time.time()
                solution, benefit, iterations, benefitsIterations = grasp(benefits, weights, capacity)
                timesInstance[i] = time.time() - start
                
                benefitsInstance[i] = benefit
                errorsInstance[i] = abs(benefit - opt) / opt
                allBenefits = allBenefits + benefitsIterations

            graficar(allBenefits, max(allBenefits), 'GRASP', str(len(weights)))
            plt.savefig('./graficos/grasp/convergencia'+str(len(weights))+"_GRASP")
            graficarTres(benefitsInstance, timesInstance, errorsInstance,'GRASP', str(len(weights)))
            plt.savefig('./graficos/grasp/'+str(len(weights))+"_GRASP")

            series = pd.Series(benefitsInstance)
            print('Estadísticas de '+str(len(weights)))
            print(series.describe())
            
        print("Ejecución GRASP terminada")
        print("gráficos guardados en ../graficos/grasp")
        
    if opcion  == '2' or opcion == '3':

        print("\nEjecutando Algoritmo genético")
        
        cantidad_elementos = ['10','20','100','200','500']
        i = 0
        for instance in instances:
        
            matriz = numpy.array(leeArchivo(instance),dtype=object)
            optimo = matriz[0][2]
            
            beneficios,tiempos,listaSoluciones,todasSoluciones,todosBeneficios = ejecucionAlgoritmo(11,matriz)
            listeErrores = errorPorcentual(beneficios,optimo)
            
            graficar(todosBeneficios,max(todosBeneficios),'AG', cantidad_elementos[i])# en este se coloca la lista para la convergencia
            plt.savefig('./graficos/genetico/convergencia'+cantidad_elementos[i]+"_AG")
            graficarTres(beneficios, tiempos, listeErrores, 'AG', cantidad_elementos[i])
            plt.savefig('./graficos/genetico/'+cantidad_elementos[i]+"_AG")
            
            series = pd.Series(beneficios)
            print('Estadísticas de '+cantidad_elementos[i])
            print(series.describe())
            
            i = i + 1
        
        print("Ejecución Algoritmo genético terminada")
        print("gráficos guardados en ../graficos/genetico")

    if opcion != '1' and opcion != '2' and opcion != '3':
        print('Instrucciones de uso:')
        print("python main.py <heurística a utilizar>")
        print("1: GRASP")
        print("2: Algoritmo genético")
        print("3: GRASP y Algoritmo genético")
    
