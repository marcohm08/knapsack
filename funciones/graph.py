import matplotlib.pyplot as plt

def graficar(listaMejores, mejorObjetivo, algoritmo, cantidad):
    plt.figure(figsize=(7,5))
    graficoMejores = plt.plot(listaMejores)
    plt.setp(graficoMejores,"linestyle","-","marker","s","color","b","markersize","2")
    plt.title(u"Curva de convergencia Knapsack 0-1 "+algoritmo+' '+cantidad+' elementos') 
    plt.ylabel(u"Valor objetivo") 
    plt.xlabel(('Mejor beneficio encontrado : ' + str(mejorObjetivo)))
    return True

def graficarTres(beneficios, tiempos, errores, algoritmo,cantidad):
    plt.figure(figsize=(8,5))
    plt.subplot(3, 1, 1)
    x = range(1,len(beneficios) + 1)
    plt.title(u'Resultados '+algoritmo+' '+cantidad+' elementos')
    graficoMejores = plt.plot(x,beneficios)
    plt.xticks(x)
    plt.setp(graficoMejores,"linestyle","-","marker","o","color","b","markersize","3")
    plt.ylabel(u'Valor Objetivo')
    i = 1
    for valor in beneficios:
        plt.annotate(str(round(valor,2)), xy=(i, valor))
        i = i + 1
    plt.subplot(3, 1, 2)
    graficoTiempos = plt.plot(x,tiempos)
    plt.setp(graficoTiempos,"linestyle","-","marker","s","color","r","markersize","3")
    plt.xticks(x)
    plt.ylabel("Tiempo (s)")
    i = 1
    for valor in tiempos:
        plt.annotate(str(round(valor,2)), xy=(i, valor))
        i = i + 1
    plt.subplot(3, 1, 3)
    graficoErrores = plt.plot(x,errores)
    plt.setp(graficoErrores,"linestyle","-","marker","s","color","g","markersize","3")
    plt.xticks(x)
    plt.ylabel("Error (%)")
    i = 1
    for valor in errores:
        plt.annotate(str(round(valor,2)), xy=(i, valor))
        i = i + 1
    plt.xlabel("Ejecución")
    return True