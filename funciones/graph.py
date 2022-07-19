import matplotlib.pyplot as plt

def graficarTres(beneficios, tiempos, errores):
    plt.figure()
    plt.subplot(3, 1, 1)
    x = range(1,len(beneficios) + 1)
    plt.title(f'Mejores beneficios por ejecución')
    graficoMejores = plt.plot(x,beneficios)
    plt.xticks(x)
    plt.setp(graficoMejores,"linestyle","-","marker","o","color","b","markersize","3")
    plt.ylabel(f'Valor Objetivo')
    i = 1
    for valor in beneficios:
        plt.annotate(str(round(valor,2)), xy=(i, valor))
        i = i + 1
    plt.subplot(3, 1, 2)
    graficoTiempos = plt.plot(x,tiempos)
    plt.setp(graficoTiempos,"linestyle","-","marker","s","color","r","markersize","3")
    plt.xticks(x)
    plt.ylabel(u"Tiempo (s)")
    i = 1
    for valor in tiempos:
        plt.annotate(str(round(valor,2)), xy=(i, valor))
        i = i + 1
    plt.subplot(3, 1, 3)
    graficoErrores = plt.plot(x,errores)
    plt.setp(graficoErrores,"linestyle","-","marker","s","color","g","markersize","3")
    plt.xticks(x)
    plt.ylabel(u"Error (%)")
    i = 1
    for valor in errores:
        plt.annotate(str(round(valor,2)), xy=(i, valor))
        i = i + 1
    plt.xlabel(u"Número de ejecución")
    return True