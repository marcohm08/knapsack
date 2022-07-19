import time
import numpy
import matplotlib.pyplot as plt
import random
import pandas as pd
import sys

# Funci�n que lee el archivo con los datos
def leeArchivo(nombre):
    archivo = open(nombre,'r')
    matriz = []
    fila = []
    for linea in archivo:
        fila = linea.split()
        filaInt = []
        for elemento in fila:
            filaInt.append(int(elemento))
        matriz.append(filaInt)
    archivo.close()
    return matriz

# Funci�n que construye una soluci�n inicial aleatoria 
def solucionInicialAleatoria(elementos,matriz):
    #solucionInicial =  [random.randint(0,1) for b in range(1,elementos+1)]
    solucion = []
    peso = 0
    for i in range(elementos):
        valor = random.randint(0,1)
        if valor == 1:
            if peso + matriz[i][1] <=  matriz[0][1]:
                solucion.append(valor)
                peso = peso + matriz[i][1]
            else:
                solucion.append(0)
        else:
            solucion.append(valor)
    return solucion

def calcularPesoMochila(solucion,matriz):
    peso = 0
    for i in range(1,matriz[0][0] + 1):
        peso = peso + matriz[i][1] * solucion[i - 1]
    return peso

def solucionValida(solucion,matriz):
    peso = 0
    for i in range(1,matriz[0][0] + 1):
        peso = peso + matriz[i][1] * solucion[i - 1]
    if peso > matriz[0][1]:
        return False
    else:
        return True

def generaSolucionesIniciales(numero, matriz):
    soluciones = []
    while len(soluciones) != numero:
        solucion = solucionInicialAleatoria(matriz[0][0],matriz)
        if solucionValida(solucion,matriz):
            soluciones.append(solucion)
    return soluciones


def funcionObjetivo(matriz,solucion):
    valor = 0
    for i in range(1,matriz[0][0] + 1):
        valor = valor + matriz[i][0] * solucion[i - 1]
    return valor

def evaluacionSoluciones(soluciones,matriz):
    valores = []
    for solucion in soluciones:
        valor = funcionObjetivo(matriz,solucion)
        valores.append(valor)
    return valores

def obtenerMejorValor(soluciones,valores):
    mayorBeneficio = max(valores)
    indiceMejor = valores.index(mayorBeneficio)
    mejorSolucion = soluciones[indiceMejor]
    return mejorSolucion,mayorBeneficio

def cruzamiento(conjunto):
    punto = int(len(conjunto[0]) / 2)
    listaMitades = []
    nuevasSoluciones = []
    for sol in conjunto:
        mitades = []
        parte1 = sol[:punto]
        parte2 = sol[punto:]
        mitades.append(parte1)
        mitades.append(parte2)
        listaMitades.append(mitades)   
    sol1 = listaMitades[0][0] + listaMitades[1][1]
    sol2 = listaMitades[0][1] + listaMitades[1][0]
    nuevasSoluciones.append(sol1)
    nuevasSoluciones.append(sol2)    
    return nuevasSoluciones

def mutacion(sol,probabilidad):
    nuevaSol = []
    for i in range(0,len(sol)):
        numeroAleatorio = random.random()

        if numeroAleatorio > probabilidad:
            if sol[i] == 1:
                valor = 0
            else:
                valor = 1
        else: 
            valor = sol[i]

        nuevaSol.append(valor)

    return nuevaSol

def correccionPeso(solucion, matriz):
    indices = [index for index, element in enumerate(solucion) if element == 1]
    peso = calcularPesoMochila(solucion,matriz)
    while peso > matriz[0][1]:
        indice =  random.choice(indices)
        solucion[indice] = 0
        peso = calcularPesoMochila(solucion,matriz)
        indices = [index for index, element in enumerate(solucion) if element == 1]
    return solucion
        

def nuevaPoblacion(soluciones, valores, matriz):
    valoresCopia = valores.copy()
    mejorValor1 = max(valores)
    indiceMejor = valores.index(mejorValor1)
    mejorSol1 = soluciones[indiceMejor]
    valoresCopia.remove(mejorValor1)
    mejorValor2 = max(valoresCopia)
    indiceSegundoMejor = valores.index(mejorValor2)
    mejorSol2 = soluciones[indiceSegundoMejor]
    padres = [mejorSol1,mejorSol2]
    hijos = cruzamiento(padres)
    hijosMutados = []
    i = 0
    while len(hijosMutados) < 2:
        mutado = mutacion(hijos[i],0.8)
        if solucionValida(mutado,matriz):
            hijosMutados.append(mutado)
            i = i + 1
        else:
            mutado = correccionPeso(mutado,matriz)
            hijosMutados.append(mutado)
            i = i + 1
    nuevoConjunto = padres + hijosMutados
    return nuevoConjunto

def busquedaLocal(solucion, matriz):
    agrega = True
    adicion = 0
    indiceObjeto = 0
    solAux = solucion.copy()
    while agrega:
        indices_0 = [index for index, element in enumerate(solAux) if element == 0]
        for indice in indices_0:
            solAux[indice] = 1
            if solucionValida(solAux,matriz):
                if(matriz[1 + indice][0] > adicion):
                    indiceObjeto = indice
                    adicion = matriz[1 + indice][0]
            solAux[indice] = 0    
        if adicion == 0:
            agrega = False
        else: 
            solAux[indiceObjeto] = 1
            adicion = 0
            indiceObjeto = 0  
        beneficio = funcionObjetivo(matriz,solAux)
    return solAux,beneficio



def algoritmo_genetico(matriz):
    soluciones = generaSolucionesIniciales(4,matriz)
    valores  = evaluacionSoluciones(soluciones,matriz)  
    mejorSolucion,mayorBeneficio = obtenerMejorValor(soluciones,valores)  
    listaMejores = [mejorSolucion]
    listaBeneficios = [mayorBeneficio]
    ciclosSinMejora = 0
    ciclos = 0
    while ciclosSinMejora < 1000 and ciclos < (2500 - matriz[0][0]):
        soluciones = nuevaPoblacion(soluciones,valores,matriz)
        valores  = evaluacionSoluciones(soluciones,matriz)               
        mejorSolucionCiclo,mayorBeneficioCiclo = obtenerMejorValor(soluciones,valores)       
        #print(f'Ciclo {ciclos}, mejor valor: {mayorBeneficio}, solucion ciclo: {mayorBeneficioCiclo}')
        if mayorBeneficioCiclo <= mayorBeneficio:
            ciclosSinMejora = ciclosSinMejora + 1
        else:
            mayorBeneficio = mayorBeneficioCiclo
            mejorSolucion = mejorSolucionCiclo
            ciclosSinMejora = 0
        listaMejores.append(mejorSolucion)
        listaBeneficios.append(mayorBeneficio)
        ciclos = ciclos + 1       
    mejorSolucion,mayorBeneficio = busquedaLocal(mejorSolucion,matriz)
    listaMejores.append(mejorSolucion)
    listaBeneficios.append(mayorBeneficio)   
    return listaBeneficios,listaMejores,mayorBeneficio,mejorSolucion

def ejecucionAlgoritmo(veces,matriz):
    beneficios = [] # Beneficios maximos de cada iteración
    tiempos = []
    todosBeneficios = [] # Beneficios de todas las iteraciones
    listaSoluciones = []
    todasSoluciones = []
    for i in range(veces):
        t0 = time.time()
        listaBeneficios,listaMejores,mayorBeneficio,mejorSolucion = algoritmo_genetico(matriz)
        t1 = time.time() - t0      
        beneficios.append(mayorBeneficio)
        tiempos.append(t1)
        listaSoluciones.append(mejorSolucion)
        todasSoluciones = todasSoluciones + listaMejores
        todosBeneficios = todosBeneficios + listaBeneficios
    return beneficios,tiempos,listaSoluciones,todasSoluciones,todosBeneficios

def errorPorcentual(lista, optimo):
    listaErrores = []
    for resultado in lista:
        error = abs(resultado - optimo)/optimo
        listaErrores.append(error)
    return listaErrores
    
    